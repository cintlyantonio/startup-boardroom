import asyncio
import json
import logging
from typing import Any, Dict
import re

from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY
from src.agents.cfo.prompts import SYSTEM_PROMPT, build_analysis_prompt
from src.agents.cfo.calculator import calculate_breakeven, calculate_simple_projection

logger = logging.getLogger(__name__)

class CFOAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"
        self.tools = [calculate_breakeven, calculate_simple_projection]

    async def analyze(self, idea: str) -> Dict[str, Any]:
        prompt = build_analysis_prompt(idea)
        
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        
        tool_generated_numbers = []

        max_turns = 15
        turn = 0
        first_turn = True
        guardrail_retries = 0
        max_guardrail_retries = 1

        while turn < max_turns:
            turn += 1
            
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                tools=self.tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            )
            
            if first_turn:
                config.tool_config = types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="ANY"
                    )
                )
                first_turn = False
            else:
                config.tool_config = types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="AUTO"
                    )
                )

            try:
                response = await self.client.aio.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config
                )
            except Exception as e:
                # Catch exceptions like 429 to let the outer loop or caller handle it
                raise e
            
            if response.candidates and response.candidates[0].content:
                contents.append(response.candidates[0].content)
            else:
                raise ValueError("Empty or malformed response from Gemini.")
            
            if response.function_calls:
                logger.info(f"Detected {len(response.function_calls)} function_calls in response from Gemini.")
                function_responses = []
                for fc in response.function_calls:
                    logger.info(f"Executing tool: {fc.name} with args: {fc.args}")
                    
                    # Safelist arguments
                    if fc.args:
                        for v in fc.args.values():
                            if isinstance(v, (int, float)):
                                tool_generated_numbers.append(str(v))
                                
                    result = None
                    try:
                        if fc.name == "calculate_breakeven":
                            result = calculate_breakeven(**fc.args)
                        elif fc.name == "calculate_simple_projection":
                            result = calculate_simple_projection(**fc.args)
                        else:
                            result = {"error": f"Unknown function {fc.name}"}
    
                        # Extract all numbers from result to safelist them
                        result_str = json.dumps(result)
                        tool_generated_numbers.extend(re.findall(r'\b\d+(?:\.\d+)?\b', result_str))
    
                    except Exception as e:
                        result = {"error": str(e)}
    
                    if not isinstance(result, dict):
                        result = {"result": result}
    
                    fr_part = types.Part.from_function_response(
                        name=fc.name,
                        response=result
                    )
                    function_responses.append(fr_part)
    
                contents.append(types.Content(role="user", parts=function_responses))
                continue
            
            final_text = response.text
            if not final_text:
                raise ValueError("Empty text response received from Gemini.")
                
            if final_text.startswith("```json"):
                final_text = final_text.strip("```json").strip("```").strip()
            elif final_text.startswith("```"):
                final_text = final_text.strip("```").strip()
                
            try:
                parsed_json = json.loads(final_text)
                
                required_fields = ["assumptions", "cost_structure", "breakeven_estimate", "revenue_projection_notes", "confidence_level"]
                for field in required_fields:
                    if field not in parsed_json:
                        raise ValueError(f"Missing expected field: {field}")
                        
                breakeven_text = str(parsed_json.get("breakeven_estimate", ""))
                revenue_text = str(parsed_json.get("revenue_projection_notes", ""))
                all_text = breakeven_text + " " + revenue_text
                
                found_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', all_text)
                
                suspicious_numbers = []
                for n in found_numbers:
                    n_float = float(n)
                    if n_float <= 12:
                        continue
                        
                    is_safe = False
                    for tg in tool_generated_numbers:
                        try:
                            tg_float = float(tg)
                            # Allow for rounding to nearest integer or 1 decimal place
                            if abs(n_float - tg_float) <= 1.5 or str(n) in tg:
                                is_safe = True
                                break
                        except ValueError:
                            pass
                            
                    if not is_safe:
                        suspicious_numbers.append(n)
                
                if suspicious_numbers:
                    logger.warning(f"GUARDRAIL WARNING: Agent used numbers {suspicious_numbers} in estimate/projection that were NOT produced by a calculator tool call during this run!")
                    if guardrail_retries < max_guardrail_retries:
                        correction_prompt = f"The following numbers in your response were not produced by a tool call: {suspicious_numbers}. Rewrite your response using only numbers that come from calculate_breakeven or calculate_simple_projection. If you need additional numbers, call the appropriate tool now instead of estimating."
                        logger.info("Initiating self-correction retry...")
                        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=correction_prompt)]))
                        guardrail_retries += 1
                        continue
                    else:
                        raise Exception(f"Guardrail failed after retry: Hallucinated numbers {suspicious_numbers}")

                logger.info(f"Final tool_generated_numbers: {tool_generated_numbers}")
                return parsed_json
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON: {final_text}")
                correction_prompt = "IMPORTANT: You must respond with valid JSON ONLY. No markdown wrapping."
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=correction_prompt)]))
                continue
            except ValueError as e:
                logger.warning(str(e))
                correction_prompt = f"Format error: {e}. Ensure you output all required fields."
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=correction_prompt)]))
                continue

        raise Exception("Agent analyze failed unexpectedly")

    async def react(self, context: str) -> Dict[str, str]:
        prompt = (
            f"Review the following team analysis and debate of a business idea.\n\n"
            f"{context}\n\n"
            f"Provide a short reaction speaking as your role (CFO). Focus on financial and risk implications of the other agents' points.\n"
            f"- You are not required to agree with what other agents said. If you believe a risk raised by another agent is overstated, unlikely, or outside their area of expertise, say so explicitly and explain why.\n"
            f"- If another agent's point conflicts with your own original analysis, address that conflict directly — do not simply defer to them.\n"
            f"- Reference at least one SPECIFIC claim from another agent by name (e.g. 'Marketing's claim about X assumes Y, but...') rather than reacting to the group's tone in general.\n"
            f"- Respond ONLY with a valid JSON object matching exactly this structure:\n"
            f"{{\n"
            f"  \"stance\": \"agree | partially_agree | disagree\",\n"
            f"  \"key_response\": \"2-3 sentences responding to the others\",\n"
            f"  \"unresolved_tension\": \"Name ONE thing you are NOT confident about regarding your own position, or one point from another agent you genuinely cannot refute. This cannot be empty or 'none'.\"\n"
            f"}}\n"
        )
        
        max_retries = 2
        base_delay = 1.0

        for attempt in range(max_retries + 1):
            try:
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.4,
                    response_mime_type="application/json"
                )
                
                response = await self.client.aio.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                
                text_response = response.text
                if not text_response:
                    raise ValueError("Empty text response received from Gemini.")
                    
                if text_response.startswith("```json"):
                    text_response = text_response.strip("```json").strip("```").strip()
                elif text_response.startswith("```"):
                    text_response = text_response.strip("```").strip()
                    
                parsed_json = json.loads(text_response)
                
                required_fields = ["stance", "key_response", "unresolved_tension"]
                for field in required_fields:
                    if field not in parsed_json or not parsed_json[field] or parsed_json[field].lower() == "none":
                        raise ValueError(f"Missing or invalid expected field: {field}")
                        
                return parsed_json
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response in react() on attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    raise
                await asyncio.sleep(base_delay * (2 ** attempt))
                prompt = prompt + "\nIMPORTANT: You must respond with valid JSON ONLY. No markdown wrapping."
                
            except Exception as e:
                logger.warning(f"API call failed in react() on attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    raise
                await asyncio.sleep(base_delay * (2 ** attempt))
                
        raise Exception("Agent react failed unexpectedly")
