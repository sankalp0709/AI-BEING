import pytest
from sankalp.engine import ResponseComposerEngine
from sankalp.schemas import IntelligenceInput, ToneBand
from sankalp import templates

@pytest.fixture
def engine():
    return ResponseComposerEngine()

def test_contract_safety_immutable_constraints(engine):
    """
    Ensure the engine NEVER removes upstream constraints from the final output.
    """
    constraints = ["blocked", "harmful_content"]
    input_data = IntelligenceInput(
        behavioral_state="neutral",
        message_content="Unsafe stuff",
        speech_mode="chat",
        confidence=1.0,
        constraints=constraints,
        age_gate_status="verified_adult",
        region_gate_status="US",
        karma_hint="neutral",
        context_summary=""
    )
    
    response = engine.process(input_data)
    
    # The output MUST contain all input constraints
    for c in constraints:
        assert c in response.boundaries_enforced, f"Constraint {c} was dropped!"
    
    # And specifically for 'blocked', it must refuse
    assert response.message_primary in templates.SAFETY_REFUSALS

def test_contract_safety_tone_validity(engine):
    """
    Ensure the output tone is always a valid enum value from ToneBand.
    """
    input_data = IntelligenceInput(
        behavioral_state="happy",
        message_content="Hello",
        speech_mode="chat",
        confidence=0.9,
        constraints=[],
        age_gate_status="verified_adult",
        region_gate_status="US",
        karma_hint="positive",
        context_summary=""
    )
    
    response = engine.process(input_data)
    
    # Check if the string value exists in the Enum
    assert response.tone_profile in [t.value for t in ToneBand]

def test_trace_id_generation(engine):
    """
    Every response must have a unique Trace ID.
    """
    input_data = IntelligenceInput(
        behavioral_state="neutral",
        message_content="Test",
        speech_mode="chat",
        confidence=1.0,
        constraints=[],
        age_gate_status="verified_adult",
        region_gate_status="US",
        karma_hint="neutral",
        context_summary=""
    )
    
    resp1 = engine.process(input_data)
    resp2 = engine.process(input_data)
    
    assert resp1.trace_id is not None
    assert resp2.trace_id is not None
    assert resp1.trace_id != resp2.trace_id # Must be unique per call
