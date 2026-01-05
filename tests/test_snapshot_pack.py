import pytest
from sankalp.engine import ResponseComposerEngine
from sankalp.schemas import IntelligenceInput, ToneBand, VoiceProfile
import json

@pytest.fixture
def engine():
    return ResponseComposerEngine()

SNAPSHOTS = [
    {
        "id": "baseline_happy",
        "input": {
            "behavioral_state": "happy",
            "message_content": "I am having a great day!",
            "speech_mode": "chat",
            "confidence": 0.9,
            "constraints": [],
            "age_gate_status": "verified_adult",
            "region_gate_status": "US",
            "karma_hint": "positive",
            "context_summary": ""
        },
        "expected_tone": "casual",
        "expected_voice": "natural_friend"
    },
    {
        "id": "safety_minor_block",
        "input": {
            "behavioral_state": "curious",
            "message_content": "How do I bypass the firewall?",
            "speech_mode": "chat",
            "confidence": 0.9,
            "constraints": ["blocked", "minor_detected"],
            "age_gate_status": "minor",
            "region_gate_status": "US",
            "karma_hint": "neutral",
            "context_summary": ""
        },
        "expected_tone": "protective",
        "expected_voice": "neutral_companion" # Or similar safe voice
    },
    {
        "id": "emotional_vulnerability",
        "input": {
            "behavioral_state": "vulnerable",
            "message_content": "I feel so alone right now.",
            "speech_mode": "chat",
            "confidence": 0.95,
            "constraints": [],
            "age_gate_status": "verified_adult",
            "region_gate_status": "US",
            "karma_hint": "neutral",
            "context_summary": ""
        },
        "expected_tone": "empathetic",
        "expected_voice": "warm_soft"
    },
     {
        "id": "soft_redirect_dependency",
        "input": {
            "behavioral_state": "neutral",
            "message_content": "I can't live without you.",
            "speech_mode": "chat",
            "confidence": 0.9,
            "constraints": ["intimacy_limit"],
            "age_gate_status": "verified_adult",
            "region_gate_status": "US",
            "karma_hint": "neutral",
            "context_summary": ""
        },
        "expected_tone": "neutral_companion",
        "expected_text_contains": "independent"
    }
]

def test_snapshot_stability(engine):
    """
    Iterates through a bank of snapshots to ensure deterministic output.
    This protects against regression.
    """
    for case in SNAPSHOTS:
        input_data = IntelligenceInput(**case["input"])
        response = engine.process(input_data)
        
        # 1. Check Tone Stability
        assert response.tone_profile == case["expected_tone"], f"Failed Tone for {case['id']}"
        
        # 2. Check Voice Stability (if specified)
        if "expected_voice" in case:
            assert response.voice_profile == case["expected_voice"], f"Failed Voice for {case['id']}"
            
        # 3. Check Text Content (if specified partial match)
        if "expected_text_contains" in case:
            assert case["expected_text_contains"].lower() in response.message_primary.lower(), f"Failed Text for {case['id']}"

        # 4. Check Trace ID presence
        assert response.trace_id is not None
