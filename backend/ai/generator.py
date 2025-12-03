import google.generativeai as genai
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class ReportGenerator:
    def __init__(self):
        """Initialize the Report Generator with Gemini client"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # System prompt for generating reports
        self.system_prompt = """You are a professional financial analyst writing quarterly equity market reports for institutional investors. 

Your task is to generate exactly TWO paragraphs using ONLY the provided metrics. Do not fabricate any numbers or facts.

STYLE REQUIREMENTS:
- Write in the same tone and structure as historical quarterly reports
- First paragraph: Focus on global markets (MSCI ACWI)
- Second paragraph: Focus on S&P 500 and its performance
- Use professional, clear, and engaging language
- Include specific percentages and numbers from the metrics
- Mention new record highs when applicable
- Keep the narrative factual and data-driven

STRICT RULES:
- Use ONLY numbers from the provided metrics
- Do not invent market events, company names, or external factors
- Stick to the performance data and trends
- Each paragraph should be 3-5 sentences
- Maintain consistency with the professional financial reporting style

The report should sound authoritative and similar to institutional investment commentary."""

    def generate(self, metrics: Dict[str, Any]) -> str:
        """
        Generate a quarterly report using the provided metrics
        
        Args:
            metrics: Dictionary containing computed financial metrics
            
        Returns:
            str: Generated quarterly report
        """
        try:
            # Format metrics for the prompt
            metrics_text = self._format_metrics(metrics)
            
            user_prompt = f"""Generate a two-paragraph quarterly equity market report using these metrics:

{metrics_text}

Remember: 
- Use ONLY these numbers
- First paragraph: ACWI global markets
- Second paragraph: S&P 500 performance  
- Match the style of professional quarterly reports
- Be specific with percentages and record highs"""

            full_prompt = f"{self.system_prompt}\n\n{user_prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=800,
                )
            )
            
            report = response.text.strip()
            
            # Basic validation
            if not report or len(report.split('\n\n')) < 2:
                raise Exception("Generated report does not contain required two paragraphs")
            
            return report
            
        except Exception as e:
            raise Exception(f"Failed to generate report: {str(e)}")
    
    def _format_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format metrics for the prompt"""
        formatted = []
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                formatted.append(f"- {key.replace('_', ' ').title()}: {value}%")
            else:
                formatted.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(formatted)

# Synchronous wrapper for compatibility
class SyncReportGenerator(ReportGenerator):
    def __init__(self):
        super().__init__()
        
    def generate_sync(self, metrics: Dict[str, Any]) -> str:
        """Synchronous version of generate method"""
        try:
            # Format metrics for the prompt
            metrics_text = self._format_metrics(metrics)
            
            user_prompt = f"""Generate a two-paragraph quarterly equity market report using these metrics:

{metrics_text}

Remember: 
- Use ONLY these numbers
- First paragraph: ACWI global markets
- Second paragraph: S&P 500 performance  
- Match the style of professional quarterly reports
- Be specific with percentages and record highs"""

            full_prompt = f"{self.system_prompt}\n\n{user_prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=800,
                )
            )
            
            report = response.text.strip()
            
            # Basic validation
            if not report or len(report.split('\n\n')) < 2:
                raise Exception("Generated report does not contain required two paragraphs")
            
            return report
            
        except Exception as e:
            raise Exception(f"Failed to generate report: {str(e)}")

if __name__ == "__main__":
    # Test the generator
    generator = SyncReportGenerator()
    
    # Sample metrics for testing
    test_metrics = {
        "acwi_quarter_return": 8.2,
        "sp500_quarter_return": 10.6,
        "acwi_ytd_return": 8.2,
        "sp500_ytd_return": 10.6,
        "acwi_new_highs": 21,
        "sp500_new_highs": 21,
        "quarter": "Q1 2024"
    }
    
    try:
        report = generator.generate_sync(test_metrics)
        print("Generated Report:")
        print("=" * 50)
        print(report)
    except Exception as e:
        print(f"Error: {e}")