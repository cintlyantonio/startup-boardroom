import asyncio
import logging
from typing import Dict, Any

from src.orchestrator.state import SharedState
from src.orchestrator.debate import run_debate_round
from src.agents.cto.agent import CTOAgent
from src.agents.marketing.agent import MarketingAgent
from src.agents.cfo.agent import CFOAgent
from src.agents.skeptic.agent import SkepticAgent
from src.agents.ceo.agent import CEOAgent
from src.evaluation.debate_quality import count_specific_cross_references

class WarningCollector(logging.Handler):
    def __init__(self):
        super().__init__()
        self.warnings = []

    def emit(self, record):
        if record.levelno == logging.WARNING and "GUARDRAIL WARNING" in record.getMessage():
            self.warnings.append(record.getMessage())

async def run_pipeline(idea: str) -> SharedState:
    # Set up logging interceptor
    warning_collector = WarningCollector()
    warning_collector.setLevel(logging.WARNING)
    
    # Attach to root logger to catch all agents
    root_logger = logging.getLogger()
    root_logger.addHandler(warning_collector)
    
    try:
        state: SharedState = {
            "idea": idea,
            "analysis": {
                "cto": None,
                "marketing": None,
                "cfo": None,
                "skeptic": None
            },
            "debate": [],
            "final_plan": None,
            "warnings": []
        }
        
        agents = {
            "cto": CTOAgent(),
            "marketing": MarketingAgent(),
            "cfo": CFOAgent(),
            "skeptic": SkepticAgent()
        }
        
        # 1. Run specialist agents in parallel
        async def run_agent(name: str):
            try:
                result = await agents[name].analyze(idea)
                state["analysis"][name] = result
            except Exception as e:
                state["warnings"].append(f"{name} analysis failed: {str(e)}")
                
        await asyncio.gather(
            run_agent("cto"),
            run_agent("marketing"),
            run_agent("cfo"),
            run_agent("skeptic")
        )
        
        # 2. Run Debate Round
        state = await run_debate_round(state, agents)

        # Evaluate debate quality
        cross_ref_count = count_specific_cross_references(state["debate"])
        logging.info(f"Debate Quality - Cross Reference Count: {cross_ref_count}")
        
        # 3. Synthesize Final Plan
        ceo = CEOAgent()
        try:
            final_plan = await ceo.synthesize(state)
            state["final_plan"] = final_plan
        except Exception as e:
            state["warnings"].append(f"CEO synthesis failed: {str(e)}")
            
        # 4. Generate PDF
        if state.get("final_plan"):
            try:
                from src.output.pdf_generator import generate_pdf
                pdf_path = generate_pdf(state["final_plan"], idea)
                state["pdf_path"] = pdf_path
            except Exception as e:
                state["pdf_path"] = None
                state["warnings"].append(f"PDF generation failed: {str(e)}")
        else:
            state["pdf_path"] = None
            
        # 5. Collect Warnings
        state["warnings"].extend(warning_collector.warnings)
        
        return state
        
    finally:
        # Clean up logger
        root_logger.removeHandler(warning_collector)
