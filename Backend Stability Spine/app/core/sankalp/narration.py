from typing import Dict, Any

class NarrationEngine:
    PERSONA = "Warm but Dignified"

    def compose_response(self, content: str, emotional_output: Dict[str, Any]) -> str:
        """
        Composes the final response based on content and emotional state.
        Enforces the 'Warm but Dignified' persona.
        """
        tone = emotional_output.get("tone", "neutral")
        
        # Enforce 'Warm but Dignified' persona through tone markers
        prefix = ""
        if tone == "calm_supportive":
            prefix = "[Warm/Calm] "
        elif tone == "steady_supportive":
            prefix = "[Dignified/Steady] "
        elif tone == "positive":
            prefix = "[Warm] "
        elif tone == "negative":
            prefix = "[Dignified] "
            
        return f"{prefix}{content}"
