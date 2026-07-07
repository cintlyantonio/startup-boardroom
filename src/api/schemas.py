from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union

class IdeaRequest(BaseModel):
    idea: str = Field(..., min_length=10, description="The business idea to analyze")

class CTOAnalysis(BaseModel):
    recommended_stack: Any
    mvp_timeline_weeks: Any
    technical_risks: Any
    complexity: Any

class MarketingAnalysis(BaseModel):
    target_audience: Any
    value_proposition: Any
    competitors: Any
    acquisition_channels: Any
    market_notes: Any
    sources: Optional[List[str]] = None

class CFOAnalysis(BaseModel):
    assumptions: Any
    cost_structure: Any
    breakeven_estimate: Any
    revenue_projection_notes: Any
    confidence_level: Any

class SkepticAnalysis(BaseModel):
    risks: Any
    assumptions_challenged: Any
    overall_verdict: Any
    sources: Optional[List[str]] = None

AgentAnalysis = Union[CTOAnalysis, MarketingAnalysis, CFOAnalysis, SkepticAnalysis, None]

class ReactionDetail(BaseModel):
    stance: str
    key_response: str
    unresolved_tension: str

class DebateReaction(BaseModel):
    agent_name: str
    reaction: ReactionDetail

class RunResponse(BaseModel):
    idea: str
    analysis: Dict[str, Any]
    debate: List[DebateReaction]
    final_plan: Optional[str] = None
    pdf_path: Optional[str] = None
    warnings: List[str] = []
    cross_reference_count: Optional[int] = None
