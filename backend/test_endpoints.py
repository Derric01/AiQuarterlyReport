import requests
import json
import time

def test_all_endpoints():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing AI Quarterly Reports API")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Generate report
    try:
        metrics = {
            "acwi_quarter_return": 7.12,
            "sp500_quarter_return": 7.47,
            "quarter": "Q3 2025"
        }
        response = requests.post(f"{base_url}/report-ai", json={"metrics": metrics})
        print(f"✅ Report generation: {response.status_code}")
        if response.status_code == 200:
            report_data = response.json()
            report = report_data["report"]
            print(f"   Generated report: {report[:100]}...")
        else:
            print(f"   Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return
    
    # Test 3: Validate report
    try:
        response = requests.post(f"{base_url}/validate-ai", json={
            "report": report,
            "metrics": metrics
        })
        print(f"✅ Report validation: {response.status_code}")
        if response.status_code == 200:
            validation = response.json()
            print(f"   Valid: {validation['valid']}, Errors: {len(validation['errors'])}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Report validation failed: {e}")
    
    # Test 4: Style scoring
    try:
        response = requests.post(f"{base_url}/style-score-ai", json={"report": report})
        print(f"✅ Style scoring: {response.status_code}")
        if response.status_code == 200:
            style = response.json()
            print(f"   Style score: {style['style_score']}/{style['max_score']} - {style['feedback']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Style scoring failed: {e}")

if __name__ == "__main__":
    test_all_endpoints()