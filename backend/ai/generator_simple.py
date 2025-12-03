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

    def generate(self, metrics: Dict[str, Any]) -> str:
        """Generate a quarterly report using the provided metrics"""
        try:
            # Format metrics for the prompt
            metrics_text = self._format_metrics(metrics)
            
            prompt = f"""Generate a professional two-paragraph quarterly equity market report using these exact metrics:

{metrics_text}

Requirements:
- First paragraph: Focus on ACWI (global markets performance)
- Second paragraph: Focus on S&P 500 performance
- Use the exact numbers provided
- Keep it professional and factual
- Each paragraph should be 3-4 sentences"""

            response = self.model.generate_content(prompt)
            
            # Handle different response formats
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            elif hasattr(response, 'candidates') and response.candidates:
                if response.candidates[0].content.parts:
                    return response.candidates[0].content.parts[0].text.strip()
            
            raise Exception("No valid response from AI model")
            
        except Exception as e:
            return f"Error generating report: {str(e)}"

    def _format_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format metrics for the prompt"""
        formatted = []
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                formatted.append(f"- {key.replace('_', ' ').title()}: {value}%")
            else:
                formatted.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(formatted)