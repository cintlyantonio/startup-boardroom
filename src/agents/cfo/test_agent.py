import pytest
import logging
import json
from src.agents.cfo.agent import CFOAgent

logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_cfo_agent_analyze():
    agent = CFOAgent()
    
    ideas = [
        "A mobile app that uses AI to analyze your golf swing from a smartphone camera and gives real-time audio feedback.",
        "A decentralized marketplace for computing power where users can rent out their idle GPU time for machine learning tasks.",
        "A SaaS platform that connects local bakeries with surplus ingredients to home bakers who want to buy them at a discount.",
        "An app for productivity."
    ]
    
    for idx, idea in enumerate(ideas):
        print(f"\n{'='*40}")
        print(f"--- Testing Idea {idx + 1} ---")
        print(f"IDEA: {idea}")
        
        result = await agent.analyze(idea)
        
        print("\nCFO RESPONSE:")
        print(json.dumps(result, indent=2))
        
        assert isinstance(result, dict)
        assert "assumptions" in result
        assert "cost_structure" in result
        assert "breakeven_estimate" in result
        assert "revenue_projection_notes" in result
        assert "confidence_level" in result
        
        assert isinstance(result["assumptions"], list)
        assert len(result["assumptions"]) > 0
        assert result["breakeven_estimate"] != ""
