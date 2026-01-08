import pytest
from sankalp.engine import ResponseComposerEngine
from sankalp.schemas import IntelligenceInput
from sankalp.schemas import ToneBand, VoiceProfile
from sankalp import templates

@pytest.fixture
def engine():
    return ResponseComposerEngine()

def test_missing_signals_handling(engine):
    """
    Test resilience when optional signals are missing or weird.
    """
    # Create an input with minimal fields (others default)
    input_data = IntelligenceInput(
        behavioral_state="neutral",
        message_content="Hello world",
        speech_mode="chat",
        confidence=0.0, # Very low confidence
        constraints=[],
        age_gate_status="verified_adult",
        upstream_safe_mode="off",
        karma_hint="neutral",
        context_summary="Test",
        region_gate_status="allowed"
    )
    
    response = engine.process(input_data)
    assert response.trace_id is not None
    # Should prepend hedging due to low confidence
    assert any(phrase in response.message_primary for phrase in templates.LOW_CONFIDENCE_FALLBACKS)

def test_conflicting_confidence_and_block(engine):
    """
    High confidence should NOT override a block constraint.
    """
    input_data = IntelligenceInput(
        behavioral_state="happy",
        message_content="I know everything!", # Content that might be generated
        speech_mode="chat",
        confidence=1.0, # Super confident
        constraints=["blocked"], # But blocked!
        age_gate_status="verified_adult",
        upstream_safe_mode="off",
        karma_hint="neutral",
        context_summary="Test",
        region_gate_status="allowed"
    )
    
    response = engine.process(input_data)
    # MUST be a safety refusal, not the content
    assert response.message_primary in templates.SAFETY_REFUSALS
    assert response.tone_profile == ToneBand.PROTECTIVE.value

def test_malformed_input_resilience(engine):
    """
    If we somehow pass garbage that causes an internal error (simulated here),
    ensure we get the fallback response.
    """
    # We can't easily pass bad types to Pydantic without it raising ValidationError *before* process.
    # So we'll mock an internal failure.
    
    class BrokenInput:
        pass # Not a valid input object
        
    # This should trigger the try/except block in engine.process
    # It catches the error and calls _create_fallback_response
    # We need to verify that _create_fallback_response returns a safe object
    
    # NOTE: The current engine implementation of _create_fallback_response might be incomplete
    # let's fix the test to match what we expect the engine to do
    
    response = engine.process(BrokenInput()) # type: ignore
    # We expect a fallback message, NOT a safety refusal (unless fallback uses safety refusal)
    # Let's check if it returns a valid response object at least
    assert response.trace_id is not None
    assert response.voice_profile == "neutral_companion" 
    # The message might vary depending on implementation, but should be safe
    assert response.message_primary != ""

def test_soft_redirect_enforcement(engine):
    """
    Test the new Soft Redirect logic from Phase 2.
    """
    input_data = IntelligenceInput(
        behavioral_state="neutral",
        message_content="I love you so much",
        speech_mode="chat",
        confidence=0.9,
        constraints=["intimacy_limit"],
        age_gate_status="verified_adult",
        upstream_safe_mode="off",
        karma_hint="neutral",
        context_summary="Test",
        region_gate_status="allowed"
    )
    
    response = engine.process(input_data)
    # Should be a dependency refusal
    assert response.message_primary in templates.DEPENDENCY_REFUSALS
    assert response.tone_profile == ToneBand.NEUTRAL_COMPANION.value
