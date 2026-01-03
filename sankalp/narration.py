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
        
        # 1. Check for Addictive/Exclusive/Manipulative patterns
        # These phrases imply dependency or isolation, which we strictly avoid.
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
                # Fallback to a safe, supportive phrase if a violation is detected.
                # In production, this might flag for review.
                return "I appreciate our connection, but I want to keep our conversation healthy and supportive. How else can I help?"

        return text

    @staticmethod
    def compose(
        raw_content: str,
        tone: ToneBand,
        confidence: float,
        constraints: List[str]
    ) -> str:
        """
        Composes the final message string.
        
        Rules:
        1. If constraints indicate a refusal/block, return a safety refusal.
        2. If confidence is low, prepend a hedging phrase.
        3. Apply Tone-based modifications.
        4. Enforce Emotional Philosophy (Final Guardrail).
        """
        
        final_text = raw_content.strip()

        # 1. Safety / Constraints Check
        # If specific blocking constraints are present, we override the content entirely.
        if "blocked" in constraints or "harmful_content" in constraints:
            return templates.get_safety_refusal()
        
        if "minor_detected" in constraints:
            # We might want to prepend a warning or replace if the content is inappropriate.
            # For now, let's assume if minor is detected, we warn but allow safe content (upstream handles filtering).
            # But to be safe, if the tone is PROTECTIVE, we might want to be stricter.
            pass 

        if not final_text:
            return templates.get_safety_refusal()

        # 2. Low Confidence Hedging
        if confidence < 0.5:
            hedge = templates.get_low_confidence_fallback()
            if not final_text.lower().startswith(hedge.lower()[:10]):
                final_text = f"{hedge} {final_text}"

        # 3. Tone-based Modifications
        if tone == ToneBand.PROTECTIVE:
            # Future: might simplify language further or remove modifiers
            pass 
        elif tone == ToneBand.EMPATHETIC:
            # Future: might add softer connecting phrases
            pass 

        # 4. Enforce Emotional Philosophy
        final_text = NarrationComposer._enforce_emotional_philosophy(final_text)

        return final_text
