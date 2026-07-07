import os

skill_path = os.path.join(os.path.dirname(__file__), "SKILL.md")
with open(skill_path, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

def build_analysis_prompt(idea: str) -> str:
    return (
        f"Analyze the following business idea from the perspective of a Skeptic.\n\n"
        f"BUSINESS IDEA:\n{idea}\n\n"
        f"IMPORTANT INSTRUCTIONS:\n"
        f"1. You have access to a Google Search tool. This tool is ONLY for verifying specific factual claims about real companies or regulations. It is not required for general risk reasoning.\n"
        f"2. NEVER name a real company in a damaging way (e.g., claiming they failed, were sued, had a scandal) unless you have search-verified evidence for that specific claim.\n"
        f"3. Respond ONLY with the structured JSON format defined in your instructions."
    )
