# Architecture Rules

- Every runtime agent must live in its own folder under `src/agents/<name>/` with exactly three files: `SKILL.md`, `prompts.py`, `agent.py`.
- Every guardrail must be a class in `src/guardrails/` implementing a `check(output)` method, registered in `src/guardrails/registry.py`.
- Shared state is only defined in `src/orchestrator/state.py` — no agent should define its own local state shape.
