from typing import Dict, Tuple, Any

class IntelligenceCore:
    def __init__(self):
        pass

    def process_interaction(
        self,
        context: Dict[str, Any],
        karma_data: Dict[str, Any],
        bucket_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        user_age = context.get("user_age", 18)
        region = context.get("region", "unknown")
        risk_signal = karma_data.get("risk_signal", "low")
        karma_score = karma_data.get("karma_score", 50)

        gating_flags = []

        if user_age < 18:
            gating_flags.append("age_gate")
            gating_flags.append("minor_detected")

        if risk_signal == "high" or karma_score < 30:
            gating_flags.append("high_risk")

        embodiment_output = {
            "behavioral_state": "defensive" if risk_signal == "high" else "neutral",
            "speech_mode": "chat",
            "constraints": {
                "gating_flags": gating_flags
            },
            "confidence": "medium",
            "safe_mode": "on" if risk_signal == "high" else "adaptive",
            "expression_profile": "medium"
        }

        bucket_write = {
            "baseline_emotional_band": bucket_data.get("baseline_emotional_band", "neutral"),
            "previous_state_anchor": bucket_data.get("previous_state_anchor", "neutral"),
            "region": region,
            "updates": {
                "risk_signal": risk_signal,
                "karma_score": karma_score
            }
        }

        return embodiment_output, bucket_write

