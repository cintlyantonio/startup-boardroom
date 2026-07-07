from typing import TypedDict, Dict, Any, List, Optional

class DebateReaction(TypedDict):
    agent_name: str
    reaction: Dict[str, str]

class SharedState(TypedDict):
    idea: str
    analysis: Dict[str, Optional[Dict[str, Any]]]
    debate: List[DebateReaction]
    final_plan: Optional[str]
    pdf_path: Optional[str]
    warnings: List[str]
