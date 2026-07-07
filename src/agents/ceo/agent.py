import asyncio
import logging
from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY
from src.agents.ceo.prompts import SYSTEM_PROMPT, build_synthesis_prompt
from src.orchestrator.state import SharedState
from src.guardrails.disclaimer_guardrail import apply_disclaimer

logger = logging.getLogger(__name__)

class CEOAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"

    async def synthesize(self, state: SharedState) -> str:
        prompt = build_synthesis_prompt(state)
        
        max_retries = 2
        base_delay = 1.0

        for attempt in range(max_retries + 1):
            try:
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3,
                )
                
                response = await self.client.aio.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                
                text_response = response.text
                if not text_response:
                    raise ValueError("Empty response received from Gemini.")
                    
                # Apply disclaimer guardrail
                text_response = apply_disclaimer(text_response)
                return text_response
                
            except Exception as e:
                logger.warning(f"API call failed on attempt {attempt + 1}: {e}")
                if attempt == max_retries:
                    logger.error("Max retries reached for API call.")
                    raise
                await asyncio.sleep(base_delay * (2 ** attempt))

        raise Exception("Agent synthesize failed unexpectedly")
