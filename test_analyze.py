#!/usr/bin/env python3
"""
Test script for the analyze function
"""

import requests
import json

def test_analyze_function():
    """Test the analyze function with sample data"""
    
    # Sample form data
    test_data = {
        "name": "John Doe",
        "education": "Bachelor's Degree",
        "experience": "junior",
        "skills": ["python", "machine learning", "data analysis"],
        "interests": ["data science", "artificial intelligence"],
        "learning_style": "visual"
    }
    
    try:
        # Make POST request to analyze endpoint
        response = requests.post(
            'http://localhost:5001/analyze',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analyze function is working!")
            print(f"Success: {result.get('success')}")
            if result.get('success'):
                print("✅ Analysis completed successfully")
                print(f"User Profile: {result.get('user_profile')}")
                if 'guidance' in result:
                    guidance = result['guidance']
                    print(f"Career Recommendations: {len(guidance.get('career_recommendations', []))}")
                    print(f"Skill Gap Analysis: {len(guidance.get('skill_gap_analysis', []))}")
                    print(f"Learning Path: {len(guidance.get('learning_path', []))}")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing analyze function...")
    test_analyze_function() 