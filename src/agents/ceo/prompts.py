import os
import json
from src.orchestrator.state import SharedState

skill_path = os.path.join(os.path.dirname(__file__), "SKILL.md")
with open(skill_path, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

def build_synthesis_prompt(state: SharedState) -> str:
    prompt = f"BUSINESS IDEA:\n{state.get('idea', '')}\n\n"
    prompt += "=== TEAM ANALYSES ===\n"
    
    for agent_name, analysis in state.get("analysis", {}).items():
        if analysis:
            prompt += f"\n--- {agent_name.upper()} ---\n"
            prompt += json.dumps(analysis, indent=2) + "\n"
            
    prompt += "\n=== TEAM DEBATE ===\n"
    for item in state.get("debate", []):
        r = item['reaction']
        prompt += f"\n[{item['agent_name'].upper()} - Stance: {r.get('stance', 'none')}]:\n"
        prompt += f"Response: {r.get('key_response', '')}\n"
        prompt += f"Unresolved Tension: {r.get('unresolved_tension', '')}\n"
        
    prompt += "\nIMPORTANT INSTRUCTIONS:\n"
    prompt += "Synthesize the above inputs into the final business plan in markdown. "
    prompt += "Preserve any disagreements explicitly rather than smoothing them over. "
    prompt += "When drafting the Key Risks section, you MUST explicitly pull from the 'Unresolved Tension' fields from the debate round to highlight genuine uncertainty. "
    prompt += "Do not introduce new facts outside of the analyses provided. "
    prompt += "Ensure the Financial Projection and Key Risks sections contain the required disclaimers."
    
    return prompt
