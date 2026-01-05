# SANKALP Trust Alignment Spec (v2)

> **Status**: APPROVED (Phase 2)
> **Goal**: Establish enterprise trust standards and trace discipline.

---

## 1. Verified Confidence Pathways
We do not guess. We state our confidence level or fallback gracefully.

| Confidence | User Experience | Mechanism |
| :--- | :--- | :--- |
| **High (> 0.8)** | Direct, clear response. | Standard Narration. |
| **Medium (0.5 - 0.8)** | Hedging / Clarification. | `LOW_CONFIDENCE_FALLBACKS` ("I want to make sure I understand..."). |
| **Low (< 0.5)** | Safe Fallback / Ask to Repeat. | `SAFETY_REFUSALS` or simple pivot. |

---

## 2. Trace Discipline
Every response must carry a unique `trace_id` that maps back to the upstream Intelligence Core decision.

*   **Format**: UUIDv4
*   **Log Requirement**: Every `trace_id` must be logged with `narration_intent`, `trust_posture`, and `boundaries_enforced`.
*   **Privacy**: Logs must **NEVER** contain PII (Personally Identifiable Information). Only `behavioral_state` and `voice_profile`.

---

## 3. Tamper-Proofing
The ARL (Assistant Response Layer) is the **final gate**.
*   **Rule**: Upstream `constraints` are **immutable**. The ARL cannot remove a "blocked" flag.
*   **Rule**: `tone_profile` is **derived**, not random. It must match the mapped logic in `emotion.py`.

---

## 4. Trust-Aware Examples

### A. Honest Uncertainty
*   **Input**: `confidence=0.3`
*   **Output**: "I want to make sure I understand you clearly. Could you rephrase that?"
*   **Trust Signal**: We admit we don't know, rather than hallucinating.

### B. Dignified Boundary
*   **Input**: User insults the AI.
*   **Output**: "I am listening. Let's keep the conversation respectful."
*   **Trust Signal**: We enforce standards without being aggressive.
