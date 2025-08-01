#!/usr/bin/env python3
"""
Debug script to test form submission and identify issues
"""

import requests
import json
import time

def test_form_submission():
    """Test the form submission with detailed debugging"""
    print("🔍 Testing Form Submission with Debug Info")
    print("=" * 50)
    
    # Test data
    test_data = {
        'name': 'Test User',
        'education': 'Bachelor',
        'experience': 'junior',
        'skills': ['python', 'javascript'],
        'interests': ['web development', 'ai'],
        'learning_style': 'visual'
    }
    
    print(f"📝 Test data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Test 1: Check if server is running
        print("\n1️⃣ Testing server connectivity...")
        response = requests.get('http://localhost:5001/', timeout=5)
        print(f"   ✅ Server is running (Status: {response.status_code})")
        
        # Test 2: Submit form data
        print("\n2️⃣ Submitting form data...")
        start_time = time.time()
        
        response = requests.post(
            'http://localhost:5001/analyze',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        end_time = time.time()
        print(f"   ⏱️  Request took {end_time - start_time:.2f} seconds")
        print(f"   📊 Status Code: {response.status_code}")
        print(f"   📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ Success! Response: {json.dumps(result, indent=2)}")
                
                # Test 3: Check results page
                print("\n3️⃣ Testing results page...")
                results_response = requests.get('http://localhost:5001/results', timeout=10)
                print(f"   📊 Results page status: {results_response.status_code}")
                print(f"   📄 Results page length: {len(results_response.text)} characters")
                
                if results_response.status_code == 200:
                    print("   ✅ Results page loads successfully!")
                else:
                    print("   ❌ Results page failed to load")
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON decode error: {e}")
                print(f"   📄 Raw response: {response.text[:500]}")
        else:
            print(f"   ❌ Request failed with status {response.status_code}")
            print(f"   📄 Response text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server. Is it running?")
    except requests.exceptions.Timeout:
        print("   ❌ Request timed out")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")

def test_browser_simulation():
    """Simulate browser behavior"""
    print("\n🌐 Browser Simulation Test")
    print("=" * 30)
    
    session = requests.Session()
    
    try:
        # Step 1: Visit home page
        print("1. Visiting home page...")
        response = session.get('http://localhost:5001/')
        print(f"   Status: {response.status_code}")
        
        # Step 2: Submit form
        print("2. Submitting form...")
        form_data = {
            'name': 'Browser Test User',
            'education': 'Bachelor',
            'experience': 'junior',
            'skills': ['python', 'javascript'],
            'interests': ['web development'],
            'learning_style': 'visual'
        }
        
        response = session.post(
            'http://localhost:5001/analyze',
            json=form_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result.get('success', False)}")
        
        # Step 3: Visit results page
        print("3. Visiting results page...")
        response = session.get('http://localhost:5001/results')
        print(f"   Status: {response.status_code}")
        print(f"   Content length: {len(response.text)}")
        
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_form_submission()
    test_browser_simulation() 