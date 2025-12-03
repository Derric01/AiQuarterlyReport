from ai.generator import ReportGenerator
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Test the AI directly
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

response = model.generate_content("Generate a simple 2-paragraph financial report about Q3 2025 with ACWI return 7.12% and S&P 500 return 7.47%")
print("RAW AI RESPONSE:")
print(response.text)
print("=" * 50)

# Test the generator
try:
    rg = ReportGenerator()
    result = rg.generate({'acwi_quarter_return': 7.12, 'sp500_quarter_return': 7.47, 'quarter': 'Q3 2025'})
    print("GENERATOR WORKS:")
    print(result)
except Exception as e:
    print(f"GENERATOR ERROR: {e}")