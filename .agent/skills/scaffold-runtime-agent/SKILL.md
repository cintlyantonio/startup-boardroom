---
name: scaffold-runtime-agent
description: Scaffolds a new runtime business agent based on the CTO agent pattern.
---

# Instructions

To scaffold a new runtime business agent:
1. Create a new folder for the agent under `src/agents/<name>/`.
2. Create exactly three files inside the folder following the CTO agent pattern: `SKILL.md`, `prompts.py`, `agent.py`.
3. Register the new agent in `src/orchestrator/state.py`.
4. Prompt the user about whether the new agent needs a specific guardrail.
5. Do not touch `src/guardrails/registry.py` until the user confirms the guardrail requirements.
