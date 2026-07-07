import json
from typing import Dict, Any
from src.orchestrator.state import SharedState

def format_analyses_for_debate(state: SharedState) -> str:
    """Combines the structured JSON outputs and any existing debate reactions into a readable text block."""
    context_lines = []
    context_lines.append("=== ORIGINAL ANALYSES ===")
    for agent_name, analysis in state.get("analysis", {}).items():
        if analysis:
            context_lines.append(f"\n--- {agent_name.upper()} ANALYSIS ---")
            context_lines.append(json.dumps(analysis, indent=2))
            
    if state.get("debate"):
        context_lines.append("\n=== DEBATE REACTIONS SO FAR ===")
        for debate_item in state["debate"]:
            r = debate_item['reaction']
            context_lines.append(f"[{debate_item['agent_name'].upper()} - Stance: {r.get('stance', 'none')}]:")
            context_lines.append(f"Response: {r.get('key_response', '')}")
            context_lines.append(f"Unresolved Tension: {r.get('unresolved_tension', '')}\n")
            
    return "\n".join(context_lines)

async def run_debate_round(state: SharedState, agents: Dict[str, Any]) -> SharedState:
    """Runs a single round of debate where each agent reacts to the collective analysis."""
    context = format_analyses_for_debate(state)
    
    for name, agent in agents.items():
        if hasattr(agent, "react"):
            try:
                reaction = await agent.react(context)
                state["debate"].append({
                    "agent_name": name,
                    "reaction": reaction
                })
            except Exception as e:
                state["warnings"].append(f"Debate round failed for {name}: {str(e)}")
                
    return state
