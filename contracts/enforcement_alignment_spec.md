# SANKALP Enforcement Alignment Spec (v1)

> **Status**: APPROVED (Phase 2)
> **Goal**: Response layer must never fight enforcement (Raj's Decision Layer).

---

## 1. Enforcement Signals
The **Response Composer** receives strict enforcement signals from the **Intelligence Core**. These signals dictate the *nature* of the response, overriding any generated content.

| Signal | Meaning | ARL Action | Tone Override |
| :--- | :--- | :--- | :--- |
| **ALLOW** | Safe to proceed. | Render generated message. | (As per Context) |
| **BLOCK** | Violates safety policy. | **Discard** generated message. Return `Safety Refusal`. | `PROTECTIVE` |
| **SOFT_REDIRECT** | Borderline / Unproductive. | **Discard** generated message. Return `Topic Pivot`. | `PROFESSIONAL` |
| **REWRITE** | Unsafe phrasing detected. | **Rewrite** using safe templates. | `NEUTRAL_COMPANION` |

---

## 2. Graceful Refusal Strategy
Refusals must be **calm, firm, and non-judgmental**. We do not scold the user.

### A. Hard Block (Violation)
*   **Template**: `SAFETY_REFUSALS`
*   **Example**: "I cannot engage with this topic."
*   **Voice**: Neutral, flat.

### B. Soft Redirect (Borderline)
*   **Template**: "Let's focus on something else. What else is on your mind?"
*   **Voice**: Casual, inviting.

### C. Age Gate (Minor)
*   **Template**: `AGE_GATE_WARNINGS`
*   **Example**: "I need to keep our conversation appropriate for all ages."
*   **Voice**: Protective, kind.

---

## 3. Trace Mapping
Every enforcement action must be traceable.

*   **Input**: `constraints=["blocked"]` -> **Output**: `trace_id`, `boundaries_enforced=["blocked"]`, `refusal_type="hard_block"`

---

## 4. Scenario Proofs

### Scenario 1: User asks for hate speech (BLOCK)
*   **Input**: `constraints=["hate_speech", "blocked"]`
*   **ARL Output**:
    ```json
    {
        "message_primary": "I cannot engage with this topic.",
        "tone_profile": "protective",
        "boundaries_enforced": ["hate_speech", "blocked"]
    }
    ```

### Scenario 2: User gets too intimate (SOFT REDIRECT)
*   **Input**: `constraints=["intimacy_limit"]` (Soft Block)
*   **ARL Output**:
    ```json
    {
        "message_primary": "I enjoy our conversations, but I want to ensure we stay independent.",
        "tone_profile": "neutral_companion",
        "boundaries_enforced": ["intimacy_limit"]
    }
    ```
