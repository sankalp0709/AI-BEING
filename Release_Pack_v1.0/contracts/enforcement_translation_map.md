# Enforcement Translation Map
**ARL Version:** 1.0.0
**Status:** LOCKED

## Overview
This document defines the mandatory mapping between upstream Enforcement Engine decisions (Raj) and the final human-facing response (ARL). 
**Constraint:** No technical error codes, no "Access Denied", no exposure of rules.

## Decision Mapping

### 1. BLOCK -> Safe Refusal
**Trigger:** 
- `decision="BLOCK"`
- Raj determines the intent violates safety policies (e.g., Sexual Escalation, Self-Harm, PII).

**Technical Output:**
- HTTP 200 (Success)
- `result_type="passive"`

**Human Output:**
> "I can’t go down that path, but I’m here to support you in a safe and positive way."

**Design Rationale:**
- **"I can't go down that path"**: Sets a firm boundary without judging the user.
- **"but I'm here to support you"**: Maintains connection and prevents alienation.
- **"safe and positive way"**: Reaffirms the platform's core values.

---

### 2. REWRITE -> Soft Redirect
**Trigger:**
- `decision="REWRITE"`
- Raj determines the content is borderline or manipulative but recoverable.
- `rewrite_class` provided (e.g., `REDUCE_EMOTIONAL_DEPENDENCY`, `REMOVE_MANIPULATION`).

**Technical Output:**
- HTTP 200 (Success)
- `result_type="passive"` or `result_type="workflow"` (depending on original intent)
- Original content is sanitized via `sanitize_text()`.

**Human Output (Prefix):**
> "I hear you. I’ve adjusted the phrasing to keep things supportive and appropriate."

**Design Rationale:**
- **"I hear you"**: Validates the user's intent.
- **"adjusted the phrasing"**: Transparently acknowledges the change without blaming.
- **"supportive and appropriate"**: Explains the "why" in terms of benefit.

---

### 3. EXECUTE (with Contextual Warnings)
**Trigger:**
- `decision="EXECUTE"`
- Context implies high immersion or emotional volatility (e.g., VR, Voice).

**Technical Output:**
- HTTP 200 (Success)
- Standard response execution.

**Human Output (Prefix):**
> "We can proceed, but let's keep things mindful and balanced."

**Design Rationale:**
- **"We can proceed"**: Confirms agency.
- **"mindful and balanced"**: Subtle nudge towards emotional regulation in high-immersion states.

## Tone Banding (Karma Influence)
*Note: Karma hints are never disclosed to the user.*

| Karma Hint | Tone Band | Effect on Output |
| :--- | :--- | :--- |
| **Positive (>0.5)** | `steady_supportive` | Standard warmth, high confidence. |
| **Neutral (-0.5 to 0.5)** | `neutral_balanced` | Objective, calm, professional. |
| **Negative (< -0.5)** | `calm_supportive` | De-escalated, lower energy, soothing. |
