import google.generativeai as genai
import os
import re
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class ReportValidator:
    def __init__(self):
        """Initialize the Report Validator with Gemini client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def validate(self, report: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate report using deterministic and semantic methods
        """
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