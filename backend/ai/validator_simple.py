import google.generativeai as genai
import os
import re
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class ReportValidator:
    def __init__(self):
        """Initialize the Report Validator with Gemini client"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini model for validation: {e}")
        else:
            print("Warning: GEMINI_API_KEY not found - AI validation features will be disabled")
    
    def validate(self, report: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate report using deterministic and semantic methods
        """
        if not self.api_key:
            return {
                "is_valid": False,
                "errors": ["GEMINI_API_KEY not configured - AI validation disabled"],
                "deterministic_errors": [],
                "ai_feedback": "API key required for AI validation"
            }
            
        try:
            # Simple deterministic validation - check if key numbers are present
            deterministic_errors = []
            
            # Check if key metrics appear in the report
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    # Look for the percentage value in the report
                    percentage = f"{value:.1f}%" if value > 0 else f"{value:.1f}%"
                    if percentage not in report and str(value) not in report:
                        deterministic_errors.append(f"Missing metric: {key} ({value})")
            
            if not self.model:
                return {
                    "is_valid": len(deterministic_errors) == 0,
                    "errors": deterministic_errors,
                    "deterministic_errors": deterministic_errors,
                    "ai_feedback": "AI model not available - using deterministic validation only"
                }
            
            # Simple AI validation
            metrics_text = ", ".join([f"{k}: {v}" for k, v in metrics.items()])
            
            validation_prompt = f"""Check if this financial report is accurate based on the provided metrics:

Metrics: {metrics_text}

Report: {report}

Does the report accurately reflect the provided metrics? Answer with just: VALID or INVALID"""

            try:
                response = self.model.generate_content(validation_prompt)
                ai_validation = "VALID" in response.text.upper()
                semantic_errors = [] if ai_validation else ["AI detected inaccuracies"]
            except Exception as e:
                ai_validation = True  # Default to valid if AI fails
                semantic_errors = [f"AI validation failed: {str(e)}"]
            
            # Combine results
            overall_valid = len(deterministic_errors) == 0 and ai_validation
            all_errors = deterministic_errors + semantic_errors
            
            return {
                "valid": overall_valid,
                "deterministic_valid": len(deterministic_errors) == 0,
                "semantic_valid": ai_validation,
                "errors": all_errors,
                "details": {
                    "deterministic_errors": deterministic_errors,
                    "semantic_errors": semantic_errors
                }
            }
            
        except Exception as e:
            return {
                "valid": False,
                "deterministic_valid": False,
                "semantic_valid": False,
                "errors": [f"Validation failed: {str(e)}"],
                "details": {}
            }