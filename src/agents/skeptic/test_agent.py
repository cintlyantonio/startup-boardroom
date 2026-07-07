import json
import logging
import pytest
from src.agents.skeptic.agent import SkepticAgent

logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_skeptic_agent_analyze():
    agent = SkepticAgent()
    
    ideas = [
        "A mobile app that uses AI to analyze your golf swing from a smartphone camera and gives real-time audio feedback.",
        "A decentralized marketplace for computing power where users can rent out their idle GPU time for machine learning tasks.",
        "A SaaS platform that connects local bakeries with surplus ingredients to home bakers who want to buy them at a discount."
    ]
    
    for idx, idea in enumerate(ideas):
        print(f"\n{'='*40}")
        print(f"--- Testing Idea {idx + 1} ---")
        print(f"IDEA: {idea}")
        
        result = await agent.analyze(idea)
        
        print("\nSKEPTIC RESPONSE:")
        print(json.dumps(result, indent=2))
        
        assert "risks" in result
        assert isinstance(result["risks"], list)
        assert len(result["risks"]) > 0
        
        assert "assumptions_challenged" in result
        assert isinstance(result["assumptions_challenged"], list)
        assert len(result["assumptions_challenged"]) > 0
        
        assert "overall_verdict" in result
