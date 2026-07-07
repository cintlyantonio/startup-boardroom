import asyncio
import json
import logging
import re
from typing import Any, Dict

from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY
from src.agents.skeptic.prompts import SYSTEM_PROMPT, build_analysis_prompt

logger = logging.getLogger(__name__)

class SkepticAgent:
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
                
                required_fields = ["risks", "assumptions_challenged", "overall_verdict"]
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
                
                if sources:
                    logger.info(f"Google Search was invoked by the model and returned {len(sources)} sources.")
                else:
                    logger.info("Google Search was NOT invoked by the model during this run.")
                
                parsed_json["sources"] = sources
                
                # Lightweight Guardrail Check for ungrounded negative claims about companies
                negative_keywords = ["lawsuit", "sued", "failed", "scandal", "shut down", "bankrupt", "breach", "fraud"]
                flags = []
                
                # Regex looks for capitalized sequences of words (like Company Names)
                company_pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b"
                for company_match in re.finditer(company_pattern, text_response):
                    company = company_match.group(1)
                    start_idx = max(0, company_match.start() - 60)
                    end_idx = min(len(text_response), company_match.end() + 60)
                    context = text_response[start_idx:end_idx].lower()
                    
                    for keyword in negative_keywords:
                        if keyword in context:
                            # Verify if we actually have any search sources.
                            if not sources:
                                flags.append(f"{company} (near '{keyword}')")
                            break
                            
                if flags:
                    # Deduplicate
                    flags = list(set(flags))
                    logger.warning(f"GUARDRAIL WARNING: Agent made potentially negative claims about entities {flags} but provided NO grounding sources!")
                
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
            f"Provide a short reaction speaking as your role (Skeptic). Focus on how the other three agents reacted to your points or missed the big picture.\n"
            f"- Acknowledge if any of them raised a valid counter-point that mitigates a risk you raised.\n"
            f"- Push back firmly if their reactions felt like they didn't actually engage with the specific risks you raised, or if they are being too optimistic.\n"
            f"- Reference at least one SPECIFIC claim from another agent by name (e.g. 'The CTO's assumption that Y is easy ignores...').\n"
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
