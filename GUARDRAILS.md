# Guardrails

## Never
- Never modify any `SKILL.md` under `src/agents/` without showing the diff first.
- Never run destructive shell commands (e.g., `rm -rf`, `git push --force`) without explicit confirmation.
- Never hardcode API keys anywhere in `src/`.

## Always
- Always run `src/evaluation/run_eval.py` after changing any agent `prompts.py`.
- Always check `src/orchestrator/state.py` before adding a new agent so the shared state schema stays consistent.
