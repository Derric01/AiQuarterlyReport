import google.generativeai as genai
import os
import re
from typing import Dict, Any, List
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
        
        Args:
            report: Generated report text
            metrics: Original metrics used for generation
            
        Returns:
            dict: Validation results
        """
        try:
            # Deterministic validation
            deterministic_result = self._deterministic_validation(report, metrics)
            
            # Semantic validation using AI
            semantic_result = self._semantic_validation(report, metrics)
            
            # Combine results
            overall_valid = deterministic_result["valid"] and semantic_result["valid"]
            all_errors = deterministic_result["errors"] + semantic_result["errors"]
            
            return {
                "valid": overall_valid,
                "deterministic_valid": deterministic_result["valid"],
                "semantic_valid": semantic_result["valid"],
                "errors": all_errors,
                "details": {
                    "deterministic": deterministic_result,
                    "semantic": semantic_result
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
    
    def _deterministic_validation(self, report: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic numeric validation
        
        Checks if numbers in the report match the provided metrics
        """
        errors = []
        
        try:
            # Extract all numbers from the report (percentages and integers)
            numbers_in_report = self._extract_numbers(report)
            
            # Create list of expected numbers from metrics
            expected_numbers = []
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    expected_numbers.append(abs(value))  # Use absolute values for comparison
            
            # Check tolerance for floating point numbers (±0.5%)
            tolerance = 0.5
            
            # Find numbers that don't have matches in expected numbers
            unmatched_numbers = []
            
            for num in numbers_in_report:
                found_match = False
                for expected in expected_numbers:
                    if abs(num - expected) <= tolerance:
                        found_match = True
                        break
                
                if not found_match:
                    # Check if it's a reasonable derived number (like sum, difference)
                    if not self._is_reasonable_derived_number(num, expected_numbers):
                        unmatched_numbers.append(num)
            
            # Generate errors for unmatched numbers
            if unmatched_numbers:
                errors.append(f"Found numbers that don't match metrics: {unmatched_numbers}")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "numbers_found": numbers_in_report,
                "expected_numbers": expected_numbers
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Deterministic validation error: {str(e)}"],
                "numbers_found": [],
                "expected_numbers": []
            }
    
    def _extract_numbers(self, text: str) -> List[float]:
        """Extract all numbers from text"""
        # Pattern to match numbers (including percentages and decimals)
        pattern = r'-?\d+\.?\d*'
        matches = re.findall(pattern, text)
        
        numbers = []
        for match in matches:
            try:
                num = float(match)
                # Filter out years and other non-metric numbers
                if 1900 <= num <= 2100:  # Likely years
                    continue
                numbers.append(abs(num))  # Use absolute values
            except ValueError:
                continue
        
        return numbers
    
    def _is_reasonable_derived_number(self, number: float, expected_numbers: List[float]) -> bool:
        """Check if a number could be reasonably derived from expected numbers"""
        tolerance = 1.0
        
        # Check if it's a sum of two numbers
        for i, num1 in enumerate(expected_numbers):
            for num2 in expected_numbers[i+1:]:
                if abs(number - (num1 + num2)) <= tolerance:
                    return True
                if abs(number - abs(num1 - num2)) <= tolerance:
                    return True
        
        # Check if it's a round number close to an expected number
        for expected in expected_numbers:
            if abs(number - round(expected)) <= tolerance:
                return True
        
        return False
    
    def _semantic_validation(self, report: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered semantic validation
        
        Checks for fabricated facts or logical inconsistencies
        """
        try:
            metrics_text = "\n".join([f"- {k}: {v}" for k, v in metrics.items()])
            
            validation_prompt = f"""You are validating a financial report for accuracy and factual consistency.

METRICS PROVIDED:
{metrics_text}

REPORT TO VALIDATE:
{report}

Your task: Identify any fabricated facts, unsupported claims, or information that contradicts the provided metrics.

VALIDATION CRITERIA:
- Are there any specific companies mentioned that weren't in the metrics?
- Are there any economic events or factors mentioned that can't be derived from the metrics?
- Are there any claims about market drivers that go beyond what the numbers show?
- Does the report contain any information not supported by the provided metrics?

Respond with:
1. VALID: true/false
2. ISSUES: List specific problems found (or "None" if valid)

Be strict - if anything cannot be directly supported by the metrics, mark as invalid."""

            response = self.model.generate_content(
                validation_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=500,
                )
            )
            
            result_text = response.text.strip().lower()
            
            # Parse the AI response
            is_valid = "valid: true" in result_text or "valid:true" in result_text
            
            # Extract issues
            errors = []
            if not is_valid:
                # Try to extract specific issues from the response
                lines = result_text.split('\n')
                for line in lines:
                    if 'issues:' in line or 'problems:' in line:
                        issue = line.split(':', 1)[1].strip()
                        if issue and issue != "none":
                            errors.append(f"Semantic issue: {issue}")
                
                # If no specific issues found, add a generic error
                if not errors:
                    errors.append("Semantic validation failed: Report contains unsupported information")
            
            return {
                "valid": is_valid,
                "errors": errors,
                "ai_response": result_text
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Semantic validation error: {str(e)}"],
                "ai_response": ""
            }

# Synchronous wrapper
class SyncReportValidator(ReportValidator):
    def validate_sync(self, report: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous version of validate method"""
        try:
            # Deterministic validation
            deterministic_result = self._deterministic_validation(report, metrics)
            
            # Semantic validation using AI
            semantic_result = self._semantic_validation_sync(report, metrics)
            
            # Combine results
            overall_valid = deterministic_result["valid"] and semantic_result["valid"]
            all_errors = deterministic_result["errors"] + semantic_result["errors"]
            
            return {
                "valid": overall_valid,
                "deterministic_valid": deterministic_result["valid"],
                "semantic_valid": semantic_result["valid"],
                "errors": all_errors,
                "details": {
                    "deterministic": deterministic_result,
                    "semantic": semantic_result
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
    
    def _semantic_validation_sync(self, report: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous semantic validation"""
        try:
            metrics_text = "\n".join([f"- {k}: {v}" for k, v in metrics.items()])
            
            validation_prompt = f"""You are validating a financial report for accuracy and factual consistency.

METRICS PROVIDED:
{metrics_text}

REPORT TO VALIDATE:
{report}

Your task: Identify any fabricated facts, unsupported claims, or information that contradicts the provided metrics.

VALIDATION CRITERIA:
- Are there any specific companies mentioned that weren't in the metrics?
- Are there any economic events or factors mentioned that can't be derived from the metrics?
- Are there any claims about market drivers that go beyond what the numbers show?
- Does the report contain any information not supported by the provided metrics?

Respond with:
1. VALID: true/false
2. ISSUES: List specific problems found (or "None" if valid)

Be strict - if anything cannot be directly supported by the metrics, mark as invalid."""

            response = self.model.generate_content(
                validation_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=500,
                )
            )
            
            result_text = response.text.strip().lower()
            
            # Parse the AI response
            is_valid = "valid: true" in result_text or "valid:true" in result_text
            
            # Extract issues
            errors = []
            if not is_valid:
                lines = result_text.split('\n')
                for line in lines:
                    if 'issues:' in line or 'problems:' in line:
                        issue = line.split(':', 1)[1].strip()
                        if issue and issue != "none":
                            errors.append(f"Semantic issue: {issue}")
                
                if not errors:
                    errors.append("Semantic validation failed: Report contains unsupported information")
            
            return {
                "valid": is_valid,
                "errors": errors,
                "ai_response": result_text
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Semantic validation error: {str(e)}"],
                "ai_response": ""
            }

if __name__ == "__main__":
    # Test the validator
    validator = SyncReportValidator()
    
    # Sample test data
    test_report = "The MSCI ACWI gained 8.2% this quarter with 21 new highs. The S&P 500 returned 10.6% with 21 record highs."
    test_metrics = {
        "acwi_quarter_return": 8.2,
        "sp500_quarter_return": 10.6,
        "acwi_new_highs": 21,
        "sp500_new_highs": 21
    }
    
    result = validator.validate_sync(test_report, test_metrics)
    print("Validation Result:")
    print(result)