import asyncio
import json
import logging
from typing import Any, Dict

from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY
from src.agents.marketing.prompts import SYSTEM_PROMPT, build_analysis_prompt

logger = logging.getLogger(__name__)

class MarketingAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"

    async def analyze(self, idea: str) -> Dict[str, Any]:
        prompt = build_analysis_prompt(idea)
        
        max_retries = 2
        base_delay = 1.0

        for attempt in range(max_retries + 1):
            try:
                current_prompt = prompt
                
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                    tools=[{"google_search": {}}]
                )
                
                response = await self.client.aio.models.generate_content(
                    model=self.model_name,
                    contents=current_prompt,
                    config=config
                )
                
                text_response = response.text
                if not text_response:
                    raise ValueError("Empty response received from Gemini.")
                
                if text_response.startswith("```json"):
                    text_response = text_response.strip("```json").strip("```").strip()
                elif text_response.startswith("```"):
                    text_response = text_response.strip("```").strip()
                    
                parsed_json = json.loads(text_response)
                
                required_fields = ["target_audience", "value_proposition", "competitors", "acquisition_channels", "market_notes"]
                for field in required_fields:
                    if field not in parsed_json:
                        raise ValueError(f"Missing expected field: {field}")
                
                # Extract grounding sources if available
                sources = []
                try:
                    if response.candidates and len(response.candidates) > 0:
                        grounding_metadata = getattr(response.candidates[0], "grounding_metadata", None)
                        if grounding_metadata:
                            chunks = getattr(grounding_metadata, "grounding_chunks", [])
                            for chunk in chunks:
                                web = getattr(chunk, "web", None)
                                if web:
                                    uri = getattr(web, "uri", None)
                                    if uri and uri not in sources:
                                        sources.append(uri)
                except Exception as e:
                    logger.warning(f"Failed to extract grounding metadata: {e}")
                
                parsed_json["sources"] = sources
                
                return parsed_json
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response on attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    logger.error("Max retries reached for JSON parsing.")
                    raise
                await asyncio.sleep(base_delay * (2 ** attempt))
                prompt = prompt + "\nIMPORTANT: You must respond with valid JSON ONLY. No markdown wrapping."
                
            except Exception as e:
                logger.warning(f"API call failed on attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    logger.error("Max retries reached for API call.")
                    raise
                await asyncio.sleep(base_delay * (2 ** attempt))

        raise Exception("Agent analyze failed unexpectedly")

    async def react(self, context: str) -> Dict[str, str]:
        prompt = (
            f"Review the following team analysis and debate of a business idea.\n\n"
            f"{context}\n\n"
            f"Provide a short reaction speaking as your role (Marketing). Focus on customer and market implications of the other agents' points.\n"
            f"- You are not required to agree with what other agents said. If you believe a risk raised by another agent is overstated, unlikely, or outside their area of expertise, say so explicitly and explain why.\n"
            f"- If another agent's point conflicts with your own original analysis, address that conflict directly — do not simply defer to them.\n"
            f"- Reference at least one SPECIFIC claim from another agent by name (e.g. 'The CTO's claim about X assumes Y, but...') rather than reacting to the group's tone in general.\n"
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
