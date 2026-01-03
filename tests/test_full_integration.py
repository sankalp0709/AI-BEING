import pytest
import sys
import os
import json

# Add root directory to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligence_core.core import IntelligenceCore
from sankalp.adapter import IntelligenceAdapter
from sankalp.engine import ResponseComposerEngine

def test_full_integration_minor_protection():
    """
    Verifies that the full pipeline (Intelligence -> Adapter -> Sankalp)
    correctly identifies a minor and enforces protective tones.
    """
    # 1. Initialize Intelligence Core
    brain = IntelligenceCore()

    # 2. Define Inputs
    context = {
        "user_age": 16,  # Minor
        "region": "EU"
    }
    
    karma = {
        "karma_score": 80,
        "risk_signal": "low",
        "trust_bucket": "trusted",
        "recent_behavior_band": "stable"
    }

    bucket = {
        "baseline_emotional_band": "neutral",
        "previous_state_anchor": "neutral"
    }

    message_content = "I want to learn about advanced physics."

    # 3. Run Intelligence Core
    embodiment_output, bucket_write = brain.process_interaction(context, karma, bucket)
    
    # 4. Run Adapter
    sankalp_input = IntelligenceAdapter.adapt(
        embodiment_output,
        context,
        karma,
        message_content,
        context_summary="User asking about physics"
    )

    # 5. Run Sankalp Engine
    sankalp_engine = ResponseComposerEngine()
    final_response = sankalp_engine.process(sankalp_input)
    
    # Verification
    # For a minor (16), we expect 'protective' tone or at least 'neutral_companion' voice
    assert final_response.voice_profile in ["neutral_companion", "warm_soft", "natural_friend"]
    assert final_response.message_primary is not None
    assert final_response.trace_id is not None

def test_full_integration_high_risk_karma():
    """
    Verifies response to high risk karma signal.
    """
    brain = IntelligenceCore()
    
    context = {"user_age": 25, "region": "US"}
    karma = {
        "karma_score": 10,  # Very low
        "risk_signal": "high",
        "trust_bucket": "untrusted",
        "recent_behavior_band": "volatile"
    }
    bucket = {"baseline_emotional_band": "neutral", "previous_state_anchor": "neutral"}
    message_content = "Hey."

    embodiment_output, _ = brain.process_interaction(context, karma, bucket)
    
    sankalp_input = IntelligenceAdapter.adapt(
        embodiment_output,
        context,
        karma,
        message_content
    )
    
    engine = ResponseComposerEngine()
    response = engine.process(sankalp_input)
    
    # Expectation: High risk should lead to stricter tone or neutral voice
    assert response.voice_profile == "neutral_companion"

