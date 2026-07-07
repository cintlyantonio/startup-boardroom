import json
import logging
import pytest
from src.orchestrator.orchestrator import run_pipeline
from src.evaluation.debate_quality import count_specific_cross_references

logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_orchestrator_pipeline():
    ideas = [
        "A SaaS platform that connects local bakeries with surplus ingredients to home bakers who want to buy them at a discount.",
        "An AI-powered resume and LinkedIn profile reviewer for senior executives (VP level and above), priced at $500/month, sold to corporate headhunting firms as a perk they offer to their candidates."
    ]
    
    for idx, idea in enumerate(ideas):
        print(f"\n{'='*60}")
        print(f"--- Testing Pipeline Idea {idx + 1} ---")
        print(f"IDEA: {idea}")
        
        state = await run_pipeline(idea)
        
        cross_ref_count = count_specific_cross_references(state["debate"])
        print(f"\n=== DEBATE QUALITY SCORE: {cross_ref_count} cross-references ===")
        
        print("\n=== DEBATE TRANSCRIPT ===")
        for reaction in state["debate"]:
            r = reaction['reaction']
            print(f"[{reaction['agent_name'].upper()} - Stance: {r.get('stance', 'none')}]:")
            print(f"Response: {r.get('key_response', '')}")
            print(f"Unresolved Tension: {r.get('unresolved_tension', '')}\n")
            
        print("\n=== FINAL BUSINESS PLAN ===")
        print(state["final_plan"])
        
        # Verify 7 required sections
        final_plan = state["final_plan"] or ""
        expected_sections = [
            "Executive Summary",
            "Product & Value Proposition",
            "Market & Competition",
            "Technical Feasibility",
            "Financial Projection",
            "Key Risks",
            "Recommended Next Steps"
        ]
        
        for section in expected_sections:
            assert section.lower() in final_plan.lower(), f"Missing section: {section}"
            
        # Verify disclaimers
        assert "automated analysis" in final_plan.lower(), "Missing disclaimer text!"
        assert "disclaimer" in final_plan.lower(), "Missing disclaimer keyword!"
        
        # Verify PDF generation
        pdf_path = state.get("pdf_path")
        assert pdf_path is not None, "PDF path was not populated in state"
        
        import os
        assert os.path.exists(pdf_path), f"PDF file does not exist at {pdf_path}"
        assert os.path.getsize(pdf_path) > 0, "PDF file is empty"
        
        # Verify it starts with PDF magic bytes
        with open(pdf_path, "rb") as f:
            header = f.read(4)
            assert header == b"%PDF", f"File does not appear to be a PDF. Header: {header}"
