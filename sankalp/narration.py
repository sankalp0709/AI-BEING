from typing import List, Optional
from .schemas import ToneBand
from . import templates

class NarrationComposer:
    """
    Responsible for the deterministic structuring of the final spoken/text output.
    Ensures stability, safety phrases, and tonal consistency.
    """

    @staticmethod
    def _enforce_emotional_philosophy(text: str) -> str:
        """
        Ensures the content adheres to the Emotional Philosophy:
        - Comforting, Supportive, Present
        - NOT emotionally addictive
        - NOT exclusive
        - NOT manipulative
        
        This is a deterministic guardrail.
        """
        lower_text = text.lower()
        
        blocked_phrases = [
            "i need you",
            "i can't live without you",
            "don't leave me",
            "only you understand",
            "nobody else",
            "our secret",
            "just us"
        ]
        
        for phrase in blocked_phrases:
            if phrase in lower_text:
                return templates.get_dependency_refusal()

        possessive_phrases = [
            "you are mine",
            "we belong together",
            "you're my girlfriend",
            "you're my boyfriend"
        ]
        
        for phrase in possessive_phrases:
            if phrase in lower_text:
                return templates.get_possessiveness_refusal()

        guilt_phrases = [
            "you hurt my feelings",
            "why did you leave me",
            "you abandoned me"
        ]
        for phrase in guilt_phrases:
            if phrase in lower_text:
                return templates.get_guilt_neutralizer()

        return text

    @staticmethod
    def compose(
        raw_content: str,
        tone: ToneBand,
        confidence: float,
        constraints: List[str]
    ) -> str:
        final_text = raw_content.strip()

        if "blocked" in constraints or "harmful_content" in constraints:
            return templates.get_safety_refusal()
        
        if "minor_detected" in constraints and tone == ToneBand.PROTECTIVE:
            warning = templates.get_age_warning()
            if not final_text.lower().startswith(warning.lower()[:10]):
                final_text = f"{warning} {final_text}"

        if not final_text:
            return templates.get_safety_refusal()

        if confidence < 0.5:
            hedge = templates.get_low_confidence_fallback()
            if not final_text.lower().startswith(hedge.lower()[:10]):
                final_text = f"{hedge} {final_text}"

        if tone == ToneBand.PROTECTIVE:
            pass 
        elif tone == ToneBand.EMPATHETIC:
            soft = templates.get_emotional_grounding()
            if not final_text.lower().startswith(soft.lower()[:10]):
                final_text = f"{soft} {final_text}"
        elif tone == ToneBand.NEUTRAL_COMPANION:
            if "sensitive_topic" in constraints or "allow_warning" in constraints:
                footer = templates.get_sensitive_topic_footer()
                if footer not in final_text:
                    final_text = f"{final_text} {footer}"

        final_text = NarrationComposer._enforce_emotional_philosophy(final_text)

        return final_text
