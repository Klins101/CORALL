import re
from typing import Optional, Tuple, Dict
from dataclasses import dataclass
from src.decision_making.decision_makingllm1 import decision_making_llm

@dataclass
class ValidatedResponse:
    rule: str
    situation_type: str
    action: str
    explanation: str
    is_fallback: bool = False

class ResponseValidator:
    # Valid actions that can be taken
    VALID_ACTIONS = [
        "Stand on, no action",
        "Give-way, turn to starboard",
        "Give-way, turn to port"
    ]
    
    # Valid situation types
    VALID_SITUATIONS = ["head-on", "overtaking", "crossing"]
    
    @staticmethod
    def parse_response(llm_response: str) -> Optional[ValidatedResponse]:
        """
        Parse and validate the LLM response format.
        Returns None if the response is invalid.
        """
        try:
            # Expected format: "Rule X (situation type), Action: [action], explanation: [explanation]"
            pattern = r"Rule (\d+) \(([\w-]+)\), Action: ([\w\s,-]+), explanation: (.+)"
            match = re.match(pattern, llm_response.strip())
            
            if not match:
                return None
                
            rule, situation, action, explanation = match.groups()
            
            # Validate each component
            if (situation.lower() not in ResponseValidator.VALID_SITUATIONS or
                action.strip() not in ResponseValidator.VALID_ACTIONS):
                return None
                
            return ValidatedResponse(
                rule=rule,
                situation_type=situation.lower(),
                action=action.strip(),
                explanation=explanation.strip()
            )
            
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return None

def get_fallback_response(
    risk: float,
    distance: float,
    rel_bearing: float,
    is_turning: bool,
    initial_situation: Optional[str]
) -> ValidatedResponse:
    """
    Generate a safe fallback response when LLM response is invalid.
    Uses simple rule-based logic to ensure safe operation.
    """
    # If already turning, continue until safe
    if is_turning:
        return ValidatedResponse(
            rule="FB",
            situation_type=initial_situation or "unknown",
            action="Give-way, turn to starboard",
            explanation="Fallback: Continuing turn until safe conditions met",
            is_fallback=True
        )
    
    # Emergency conditions - high risk and close distance
    if risk > 0.7 and distance < 300:
        return ValidatedResponse(
            rule="FB",
            situation_type=initial_situation or "unknown",
            action="Give-way, turn to starboard" or "Give-way, turn to port",
            explanation="Fallback: Emergency maneuver due to high risk and close range",
            is_fallback=True
        )
    
    # Default safe response
    return ValidatedResponse(
        rule="FB",
        situation_type=initial_situation or "unknown",
        action="Stand on, no action",
        explanation="Fallback: Maintaining course due to safe conditions",
        is_fallback=True
    )

def enhanced_decision_making_llm(
    risk: float,
    distance: float,
    rel_bearing: float,
    dcpa: float,
    tcpa: float,
    idx: int
) -> str:
    """
    Enhanced version of decision_making_llm with response validation and fallback.
    """
    global current_maneuver
    
    # Original LLM call
    llm_response = decision_making_llm(risk, distance, rel_bearing, dcpa, tcpa, idx)
    
    # Validate the response
    validator = ResponseValidator()
    validated_response = validator.parse_response(llm_response)
    
    # If validation fails, use fallback
    if validated_response is None:
        fallback_response = get_fallback_response(
            risk=risk,
            distance=distance,
            rel_bearing=rel_bearing,
            is_turning=current_maneuver['is_turning'],
            initial_situation=current_maneuver['initial_situation']
        )
        
        # Log the fallback for monitoring
        print(f"WARNING: Invalid LLM response, using fallback. Original response: {llm_response}")
        
        # Convert fallback response to string format matching original
        return (f"Rule {fallback_response.rule} ({fallback_response.situation_type}), "
                f"Action: {fallback_response.action}, "
                f"explanation: {fallback_response.explanation}")
    
    return llm_response

# Example usage and testing
def test_response_validation():
    validator = ResponseValidator()
    
    # Test valid response
    valid_response = "Rule 15 (crossing), Action: Stand on, no action, explanation: Low risk, target on port side"
    result = validator.parse_response(valid_response)
    assert result is not None
    
    # Test invalid response
    invalid_response = "Invalid format response"
    result = validator.parse_response(invalid_response)
    assert result is None