import pytest
import logging
import json
from src.agents.marketing.agent import MarketingAgent

logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_marketing_agent_analyze():
    agent = MarketingAgent()
    
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
        
        print("\nMARKETING RESPONSE:")
        print(json.dumps(result, indent=2))
        
        assert isinstance(result, dict)
        assert "target_audience" in result
        assert "value_proposition" in result
        assert "competitors" in result
        assert "acquisition_channels" in result
        assert "market_notes" in result
        assert "sources" in result
        
        assert isinstance(result["competitors"], list)
        if len(result["competitors"]) > 0:
            assert len(result["sources"]) > 0, "Sources should not be empty when competitors are found!"
