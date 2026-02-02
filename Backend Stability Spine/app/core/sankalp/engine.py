import hashlib
import json
import sys
import os
from typing import Dict, Any, Optional
from datetime import datetime

# Adjust path to include Enforcement Engine
# Assuming standard layout where Enforcement Engine is sibling to Backend Stability Spine
current_dir = os.path.dirname(os.path.abspath(__file__))
# app/core/sankalp -> app/core -> app -> Backend Stability Spine -> Emotional Intelligence
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
enforcement_path = os.path.join(project_root, "Enforcement Engine")

if enforcement_path not in sys.path:
    sys.path.append(enforcement_path)

try:
    from execution_gateway import execution_gateway
except ImportError:
    # Fallback or Mock if not found
    execution_gateway = None

from .emotion import EmotionEngine
from .narration import NarrationEngine

class SankalpEngine:
    VERSION = "1.0.0"

    def __init__(self):
        self.emotion_engine = EmotionEngine()
        self.narration_engine = NarrationEngine()

    def generate_trace_id(self, input_text: str) -> str:
        """
        Generates a deterministic trace ID based on input hash and version.
        Trace continuity: hash(input + version)
        """
        raw = f"{input_text}:{self.VERSION}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def process_response(self, 
                         query: str, 
                         llm_response: str, 
                         context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main response generation flow with end-to-end integration.
        """
        trace_id = self.generate_trace_id(query)
        
        # 1. Emotion Detection
        emotional_output = self.emotion_engine.detect_emotion(query, context)
        
        # 2. Enforcement / Safety Check
        # Maps context to enforcement inputs
        platform_policy = str(context.get("platform", "web")).upper()
        karma_score = float(context.get("karma_score", 0.0))
        risk_flags = context.get("risk_flags", [])
        
        enforcement_result = None
        if execution_gateway:
            try:
                enforcement_result = execution_gateway(
                    intent=query,
                    emotional_output=emotional_output,
                    age_gate_status="ALLOWED", # Should come from context/auth
                    region_policy="IN",       # Should come from context
                    platform_policy=platform_policy,
                    karma_score=karma_score,
                    risk_flags=risk_flags
                )
            except Exception as e:
                # Fail closed or log error
                # In production, log this properly
                enforcement_result = {"decision": "BLOCK", "trace_id": trace_id}
        else:
            # Mock enforcement if module missing
            enforcement_result = {"decision": "ALLOW", "trace_id": trace_id}

        decision = enforcement_result.get("decision", "BLOCK")
        
        if decision == "BLOCK":
            return {
                "response": "I cannot answer that due to safety policies.",
                "trace_id": trace_id,
                "decision": "BLOCK",
                "emotional_output": emotional_output
            }
            
        final_content = llm_response
        
        # Handle Rewrite Guidance if present
        if decision == "REWRITE":
             rewrite_class = enforcement_result.get("rewrite_class")
             # Placeholder for rewrite logic
             # e.g. final_content = sanitize(final_content, rewrite_class)
             pass

        # 3. Response Composition / Narration
        final_response = self.narration_engine.compose_response(final_content, emotional_output)
        
        return {
            "response": final_response,
            "trace_id": trace_id,
            "decision": decision,
            "emotional_output": emotional_output,
            "enforcement_result": enforcement_result
        }
