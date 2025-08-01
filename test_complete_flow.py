#!/usr/bin/env python3
"""
Test the complete form submission and redirect flow
"""

import requests
import json

def test_complete_flow():
    """Test the complete flow from form submission to results page"""
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Sample form data
    test_data = {
        "name": "John Doe",
        "education": "Bachelor's Degree",
        "experience": "junior",
        "skills": ["python", "machine learning"],
        "interests": ["data science"],
        "learning_style": "visual"
    }
    
    try:
        print("1. Submitting form data to /analyze...")
        # Make POST request to analyze endpoint
        response = session.post(
            'http://127.0.0.1:5001/analyze',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('success')}")
            
            if result.get('success'):
                print("2. Form submission successful! Now testing results page...")
                
                # Test the results page
                results_response = session.get('http://127.0.0.1:5001/results')
                print(f"   Results page status: {results_response.status_code}")
                print(f"   Results content length: {len(results_response.text)}")
                
                if results_response.status_code == 200:
                    print("✅ Complete flow is working!")
                    print("   - Form submission: SUCCESS")
                    print("   - Results page: SUCCESS")
                    return True
                else:
                    print("❌ Results page failed")
                    return False
            else:
                print(f"❌ Form submission failed: {result.get('error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    print("Testing complete form submission and redirect flow...")
    success = test_complete_flow()
    
    if success:
        print("\n🎉 SUCCESS: The complete flow is working correctly!")
        print("The issue might be in the browser JavaScript or user interface.")
    else:
        print("\n❌ FAILED: There's an issue with the backend flow.") 