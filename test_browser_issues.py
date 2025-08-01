#!/usr/bin/env python3
"""
Browser Issue Detection Script
Tests all aspects of the CareerGuideAI application to identify problems
"""

import requests
import json
import time

def test_home_page():
    """Test if the home page loads correctly"""
    print("🌐 Testing Home Page...")
    try:
        response = requests.get('http://localhost:5001/')
        if response.status_code == 200:
            print("✅ Home page loads successfully")
            if 'CareerGuideAI' in response.text:
                print("✅ CareerGuideAI content found")
            else:
                print("❌ CareerGuideAI content not found")
            return True
        else:
            print(f"❌ Home page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Home page error: {e}")
        return False

def test_form_validation():
    """Test form validation endpoints"""
    print("\n🔍 Testing Form Validation...")
    
    # Test missing name
    try:
        response = requests.post('http://localhost:5001/analyze', 
                               json={'education': 'Bachelor', 'experience': 'junior', 'skills': ['python'], 'interests': ['ai']})
        if response.status_code == 400:
            data = response.json()
            if 'Name is required' in data.get('error', ''):
                print("✅ Name validation working")
            else:
                print(f"❌ Unexpected name validation error: {data}")
        else:
            print(f"❌ Name validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Name validation error: {e}")
    
    # Test missing skills
    try:
        response = requests.post('http://localhost:5001/analyze', 
                               json={'name': 'Test User', 'education': 'Bachelor', 'experience': 'junior', 'interests': ['ai']})
        if response.status_code == 400:
            data = response.json()
            if 'At least one skill is required' in data.get('error', ''):
                print("✅ Skills validation working")
            else:
                print(f"❌ Unexpected skills validation error: {data}")
        else:
            print(f"❌ Skills validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Skills validation error: {e}")

def test_complete_analysis():
    """Test complete analysis flow"""
    print("\n🚀 Testing Complete Analysis Flow...")
    
    # Valid form data
    form_data = {
        'name': 'Test User',
        'education': 'Bachelor',
        'experience': 'junior',
        'skills': ['python', 'machine learning', 'data analysis'],
        'interests': ['artificial intelligence', 'data science'],
        'learning_style': 'visual'
    }
    
    try:
        # Submit analysis
        print("📝 Submitting analysis...")
        response = requests.post('http://localhost:5001/analyze', json=form_data)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Analysis completed successfully")
                print(f"✅ User profile: {data.get('user_profile', {}).get('name', 'Unknown')}")
                print(f"✅ Timestamp: {data.get('timestamp', 'Unknown')}")
                
                # Test results page
                print("\n📊 Testing Results Page...")
                results_response = requests.get('http://localhost:5001/results')
                if results_response.status_code == 200:
                    print("✅ Results page loads successfully")
                    if 'Your Profile Summary' in results_response.text:
                        print("✅ Profile summary section found")
                    if 'Career Analysis Overview' in results_response.text:
                        print("✅ Career statistics dashboard found")
                    if 'Top Career Recommendations' in results_response.text:
                        print("✅ Career recommendations found")
                else:
                    print(f"❌ Results page failed: {results_response.status_code}")
                
                # Test API endpoints
                print("\n🔌 Testing API Endpoints...")
                
                # Career stats
                stats_response = requests.get('http://localhost:5001/api/career-stats')
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    print(f"✅ Career stats: {stats_data.get('total_recommendations', 0)} recommendations")
                else:
                    print(f"❌ Career stats failed: {stats_response.status_code}")
                
                # Analysis history
                history_response = requests.get('http://localhost:5001/api/analysis-history')
                if history_response.status_code == 200:
                    history_data = history_response.json()
                    print(f"✅ Analysis history: {len(history_data.get('history', []))} entries")
                else:
                    print(f"❌ Analysis history failed: {history_response.status_code}")
                
                # Progress tracking
                progress_response = requests.get('http://localhost:5001/api/progress')
                if progress_response.status_code == 200:
                    progress_data = progress_response.json()
                    print(f"✅ Progress tracking: {progress_data.get('top_career_match', 'Unknown')}")
                else:
                    print(f"❌ Progress tracking failed: {progress_response.status_code}")
                
                return True
            else:
                print(f"❌ Analysis failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Analysis request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_download_features():
    """Test download functionality"""
    print("\n📥 Testing Download Features...")
    
    try:
        # Test PDF download
        pdf_response = requests.get('http://localhost:5001/download/pdf')
        if pdf_response.status_code == 200:
            print("✅ PDF download working")
        else:
            print(f"❌ PDF download failed: {pdf_response.status_code}")
        
        # Test JSON download
        json_response = requests.get('http://localhost:5001/download/json')
        if json_response.status_code == 200:
            print("✅ JSON download working")
        else:
            print(f"❌ JSON download failed: {json_response.status_code}")
    except Exception as e:
        print(f"❌ Download error: {e}")

def main():
    """Run all tests"""
    print("🧪 CareerGuideAI Browser Issue Detection")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get('http://localhost:5001/', timeout=5)
        print("✅ Server is running on http://localhost:5001")
    except:
        print("❌ Server is not running! Please start the application with: python app.py")
        return
    
    # Run all tests
    home_ok = test_home_page()
    test_form_validation()
    analysis_ok = test_complete_analysis()
    test_download_features()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    if home_ok and analysis_ok:
        print("🎉 All backend functionality is working correctly!")
        print("\n💡 If you're still having issues in the browser:")
        print("   1. Clear browser cache and cookies")
        print("   2. Try incognito/private browsing mode")
        print("   3. Check browser console for JavaScript errors (F12)")
        print("   4. Try a different browser")
        print("   5. Disable browser extensions temporarily")
    else:
        print("❌ Some backend functionality is not working")
        print("   Please check the server logs for errors")

if __name__ == "__main__":
    main() 