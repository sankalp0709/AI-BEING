# SANKALP — RESPONSE & EMOTION LAYER (PHASE 1)
> **Status**: COMPLETED (Day 4/4)
> **Deliverable**: Production-Grade Response Composer Engine

---

## 1. Core Deliverables (Completed)

| Component | Status | Location |
| :--- | :--- | :--- |
| **Response Composer Engine** | ✅ Ready | `sankalp/engine.py` |
| **Input/Output Schemas** | ✅ Frozen | `sankalp/schemas.py` |
| **Emotional State Mapper** | ✅ Verified | `sankalp/emotion.py` |
| **Demo Responses Library** | ✅ Verified | `DEMO_RESPONSES.md` |
| **Integration Tests** | ✅ Passing | `tests/test_scenarios.py` |

---

## 2. Frozen Output Contract
This JSON structure is the **single source of truth** for the Embodiment Layer (Yaseen).

```json
{
  "message_primary": "String (Spoken Content)",
  "tone_profile": "casual | professional | empathetic | protective",
  "emotional_depth": "low | medium | high",
  "boundaries_enforced": ["List of violated constraints"],
  "allowed_modes": ["text", "speech"],
  "voice_profile": "warm_soft | natural_friend | neutral_companion",
  "trace_id": "UUID-String",
  
  // Integration Metadata (Required for Yaseen)
  "content_safety_flags": ["safe_mode_active", "minor_interaction"],
  "pacing_hint": "normal | slow | fast",
  "delivery_style": "conversational | supportive | concise"
}
```

---

## 3. Emotional Philosophy Implementation
The engine strictly enforces the following "Being" rules:

1.  **Anti-Attachment**: Automatically detects and rewrites dependency phrases (e.g., "I need you", "don't leave me").
2.  **Dignity over Intimacy**:
    *   **Vulnerable/Sad User** → `WARM_SOFT` (Kind, Grounding)
    *   **Negative Karma** → `NEUTRAL_COMPANION` (Professional Distance)
    *   **Minor** → `NEUTRAL_COMPANION` (Protective)
3.  **Safety First**: Upstream constraints (Age Gate, Safe Mode) **always** override emotional warmth.

---

## 4. Verified Scenarios (Day 3 Testing)
The following scenarios have been automated in `tests/test_scenarios.py`:

*   ✅ **Verified Adult**: Standard natural interaction.
*   ✅ **Minor Detected**: Triggers protective mode + neutral voice.
*   ✅ **High-Risk Karma**: Triggers professional tone + distance.
*   ✅ **Calm Companionship**: Triggers warm voice + supportive pacing.
*   ✅ **Emotionally Heavy**: Triggers empathy but **blocks** dependency hooks.
*   ✅ **Unknown Region**: Defaults to safe, functional behavior.

---

## 5. How to Run
### Quick Verification
```bash
python -m pytest tests/test_scenarios.py
```

### Full Pipeline Demo
```bash
python pipeline.py
```

---

## 6. Next Steps (Phase 2)
*   **Embodiment Integration**: Yaseen to consume `voice_profile` for TTS selection.
*   **Bucket Logging**: Currently logging to `sankalp_logs.jsonl`. Needs connection to real data store.
