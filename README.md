# Startup Boardroom

A multi-agent system that simulates a startup leadership team — CEO, CTO,
Marketing, CFO, and a dedicated Skeptic — debating a business idea and
producing a real, disagreement-preserving business plan.

Built for the [Kaggle AI Agents: Intensive Vibe Coding Capstone](https://www.kaggle.com/competitions/vibecoding-agents-capstone-project)
— **Freestyle track**.

> Most business idea validation is either a friend saying "sounds cool" or a
> generic AI chatbot that agrees with whatever you type. This project
> simulates five specialized Gemini agents that analyze an idea
> independently, debate each other's conclusions, and synthesize a plan that
> preserves genuine disagreement instead of smoothing it over.

## Demo

- **Video:** https://youtu.be/Ep4E0QNpDVA


## Architecture

```
Business idea
      |
      v
 CEO agent (orchestrates)
      |
      +----------+----------+----------+
      v          v          v          v
    CTO      Marketing     CFO      Skeptic
 (feasibility) (market)  (finance)  (risks)
      |          |          |          |
      +----------+----------+----------+
      v
 Debate round
 (each agent declares a stance — agree / partially_agree / disagree —
  and a mandatory "unresolved tension" it cannot fully refute)
      |
      v
 CEO agent (final synthesis)
 (preserves disagreement, does not average it away)
      |
      v
 Business plan (7 sections, disclaimers, downloadable PDF)
```

Full write-up of the architecture, design decisions, and two debugging
deep-dives (a hidden Automatic Function Calling bug, and fixing shallow
multi-agent consensus) is in the [Kaggle Writeup](#) and `docs/`.

## Stack

- **Gemini API** (function calling) for all five agents
- **Google Search grounding** for the Marketing and Skeptic agents
- A real Python calculator (not the model) computes every financial figure
  the CFO agent states
- **FastAPI** backend
- **React + Tailwind** frontend
- **SKILL.md** files per agent defining persona, principles, and output
  schema
- Custom **guardrails** catching hallucinated numbers, missing disclaimers,
  and shallow debate consensus

## Project structure

```
startup-boardroom/
├── .agent/                  # Governs the coding assistant (Antigravity)
│   ├── rules/
│   ├── skills/
│   └── workflows/
├── GUARDRAILS.md             # Dev-process guardrails (for the coding agent)
├── AGENTS.md                 # General instructions for the coding agent
├── src/
│   ├── agents/                # Runtime business agents (ceo, cto, marketing, cfo, skeptic)
│   ├── guardrails/             # App-level guardrails (financial, disclaimer, etc.)
│   ├── orchestrator/            # Pipeline coordination + shared state + debate logic
│   ├── output/                  # Markdown -> PDF generation
│   └── api/                     # FastAPI app and routes
├── frontend/                 # React + Tailwind "boardroom" interface
└── requirements.txt
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Gemini API key](https://aistudio.google.com/apikey)

### Backend

```bash
git clone https://github.com/cintlyantonio/startup-boardroom.git
cd startup-boardroom

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set GEMINI_API_KEY=your_key_here

uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`. Check `GET /health` to
confirm it's running.

### Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at the local Vite dev URL (typically
`http://localhost:5173`).

## Usage

1. Open the frontend in your browser.
2. Enter a business idea.
3. Watch the CTO, Marketing, CFO, and Skeptic agents analyze it in parallel.
4. Review the structured debate round — each agent's stance and unresolved
   tensions.
5. Download the final synthesized business plan as a PDF.

A full run typically takes 45–75 seconds, since it involves multiple
sequential Gemini API calls (parallel analysis, debate, synthesis).

## Known limitations

- No persistent memory across sessions yet
- No live token-by-token streaming of the debate (single request/response
  with a staggered frontend reveal)
- Debate quality is currently validated through targeted manual test runs
  rather than an automated evaluation harness


