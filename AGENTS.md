# Startup Simulator

A multi-agent startup simulator built for a Kaggle AI Agents capstone project.
This system simulates a startup leadership team (CEO, CTO, Marketing, CFO, and Skeptic) debating a business idea and producing a final business plan.
It uses the Gemini API, a FastAPI backend, and a React frontend.

## Clarification on "Agents"
This project contains TWO distinct kinds of "agents":
1. **Runtime Business Agents**: Living in `src/agents/` (CEO, CTO, Marketing, CFO, Skeptic). These are part of the shipped application.
2. **Coding Agent**: You (the AI assistant) — governed by the rules in `.agent/rules/`.

These must never be confused. When I refer to "the CFO agent", I mean `src/agents/cfo/`, not you.

## Coding Conventions
- Python 3.11+
- Type hints required for all functions
- Use async/await for all Gemini API calls
- Use FastAPI for the backend
- No hardcoded secrets anywhere in the codebase.
