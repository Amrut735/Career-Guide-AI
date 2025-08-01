#!/usr/bin/env python3
"""
Simple test to verify Flask app is working
"""

from app import app

def test_flask_app():
    """Test if Flask app is working"""
    with app.test_client() as client:
        # Test root endpoint
        response = client.get('/')
        print(f"Root endpoint status: {response.status_code}")
        
        # Test analyze endpoint
        test_data = {
            "name": "John Doe",
            "education": "Bachelor's Degree",
            "experience": "junior",
            "skills": ["python", "machine learning"],
            "interests": ["data science"],
            "learning_style": "visual"
        }
        
        response = client.post('/analyze', json=test_data)
        print(f"Analyze endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.get_json()
            print(f"Success: {result.get('success')}")
            if result.get('success'):
                print("✅ Analyze function is working!")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.data}")

if __name__ == "__main__":
    test_flask_app() 