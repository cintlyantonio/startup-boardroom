import re
from typing import List, Dict

def count_specific_cross_references(debate: List[Dict]) -> int:
    """
    Counts how many reactions explicitly name another agent's role or claim.
    Returns the total count of cross-references found across all reactions.
    """
    count = 0
    # Roles to look for (case-insensitive)
    roles = ["cto", "marketing", "cfo", "skeptic"]
    
    for reaction_obj in debate:
        reaction_dict = reaction_obj.get("reaction", {})
        if not isinstance(reaction_dict, dict):
            continue
            
        text_to_check = reaction_dict.get("key_response", "") + " " + reaction_dict.get("unresolved_tension", "")
        text_lower = text_to_check.lower()
        
        current_agent = reaction_obj.get("agent_name", "").lower()
        
        for role in roles:
            if role != current_agent and role in text_lower:
                count += 1
                
        # Additionally, look for dollar amounts or percentages as a proxy for specific claims
        # e.g., "$500", "20%"
        if re.search(r'\$\d+', text_to_check) or re.search(r'\d+%', text_to_check):
             count += 1
             
    return count
