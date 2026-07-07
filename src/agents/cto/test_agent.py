import pytest
import logging
import json
from src.agents.cto.agent import CTOAgent

logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_cto_agent_analyze():
    agent = CTOAgent()
    
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
        
        print("\nCTO RESPONSE:")
        print(json.dumps(result, indent=2))
        
        assert isinstance(result, dict)
        assert "recommended_stack" in result
        assert "mvp_timeline_weeks" in result
        assert "technical_risks" in result
        assert "complexity" in result
