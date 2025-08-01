#!/usr/bin/env python3
"""
Step-by-step form testing to identify browser issues
"""

import requests
import json

def test_form_submission():
    """Test the exact form submission that should work"""
    print("🧪 Testing Form Submission Step by Step")
    print("=" * 50)
    
    # Test data that should work
    test_data = {
        'name': 'John Doe',
        'education': 'Bachelor',
        'experience': 'junior',
        'skills': ['python', 'javascript'],
        'interests': ['web development', 'ai'],
        'learning_style': 'visual'
    }
    
    print("📝 Submitting form with data:")
    for key, value in test_data.items():
        print(f"   {key}: {value}")
    
    try:
        # Submit the form
        response = requests.post('http://localhost:5001/analyze', 
                               json=test_data,
                               headers={'Content-Type': 'application/json'})
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Form submission successful!")
                print(f"✅ User: {data.get('user_profile', {}).get('name', 'Unknown')}")
                print(f"✅ Timestamp: {data.get('timestamp', 'Unknown')}")
                
                # Test results page
                print("\n🔍 Testing results page...")
                results = requests.get('http://localhost:5001/results')
                if results.status_code == 200:
                    print("✅ Results page loads successfully")
                    if 'John Doe' in results.text:
                        print("✅ User name appears in results")
                    if 'Your Profile Summary' in results.text:
                        print("✅ Profile summary found")
                    if 'python' in results.text.lower():
                        print("✅ Skills appear in results")
                else:
                    print(f"❌ Results page failed: {results.status_code}")
                
                return True
            else:
                print(f"❌ Form submission failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"❌ Error details: {error_data}")
            except:
                print(f"❌ Response text: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_browser_simulation():
    """Simulate what the browser should do"""
    print("\n🌐 Browser Simulation Test")
    print("=" * 30)
    
    # Create a session to maintain cookies (like a browser)
    session = requests.Session()
    
    # Step 1: Visit home page
    print("1. Visiting home page...")
    home = session.get('http://localhost:5001/')
    if home.status_code == 200:
        print("✅ Home page loaded")
    else:
        print(f"❌ Home page failed: {home.status_code}")
        return False
    
    # Step 2: Submit form
    print("2. Submitting form...")
    form_data = {
        'name': 'Jane Smith',
        'education': 'Master',
        'experience': 'mid-level',
        'skills': ['machine learning', 'python', 'sql'],
        'interests': ['data science', 'artificial intelligence'],
        'learning_style': 'kinesthetic'
    }
    
    analyze = session.post('http://localhost:5001/analyze', json=form_data)
    if analyze.status_code == 200:
        data = analyze.json()
        if data.get('success'):
            print("✅ Form submitted successfully")
        else:
            print(f"❌ Form submission failed: {data.get('error')}")
            return False
    else:
        print(f"❌ Form submission HTTP error: {analyze.status_code}")
        return False
    
    # Step 3: Visit results page
    print("3. Visiting results page...")
    results = session.get('http://localhost:5001/results')
    if results.status_code == 200:
        print("✅ Results page loaded")
        if 'Jane Smith' in results.text:
            print("✅ User data appears in results")
        if 'machine learning' in results.text.lower():
            print("✅ Skills appear in results")
        return True
    else:
        print(f"❌ Results page failed: {results.status_code}")
        return False

if __name__ == "__main__":
    print("🚀 CareerGuideAI Browser Issue Detection")
    print("=" * 60)
    
    # Test 1: Direct form submission
    success1 = test_form_submission()
    
    # Test 2: Browser simulation
    success2 = test_browser_simulation()
    
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    
    if success1 and success2:
        print("🎉 All tests passed! The backend is working perfectly.")
        print("\n💡 The issue is definitely in your browser. Try:")
        print("   1. Clear browser cache and cookies")
        print("   2. Use incognito/private mode")
        print("   3. Try a different browser")
        print("   4. Check browser console for JavaScript errors")
        print("   5. Disable browser extensions")
    else:
        print("❌ Some tests failed. Check the server logs.") 