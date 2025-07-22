#!/usr/bin/env python3
"""
Test Cases for CareerGuideAI
Comprehensive testing of the career guidance system with various user profiles.
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path to import CareerGuideAI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from career_guide_ai import CareerGuideAI

def test_data_scientist_profile():
    """Test with a data scientist profile."""
    print("🧪 Testing Data Scientist Profile...")
    
    user_input = """
    Name: Sarah Johnson
    Education: Master's in Statistics
    Experience: Mid level
    Skills: Python, R, SQL, machine learning, statistics, data analysis, pandas, numpy
    Interests: data science, machine learning, artificial intelligence, research
    """
    
    return user_input, "Data Scientist"

def test_software_engineer_profile():
    """Test with a software engineer profile."""
    print("🧪 Testing Software Engineer Profile...")
    
    user_input = """
    Name: Mike Chen
    Education: Bachelor's in Computer Science
    Experience: Junior level
    Skills: Java, JavaScript, Python, algorithms, data structures, git, testing
    Interests: web development, software engineering, open source, coding
    """
    
    return user_input, "Software Engineer"

def test_devops_engineer_profile():
    """Test with a DevOps engineer profile."""
    print("🧪 Testing DevOps Engineer Profile...")
    
    user_input = """
    Name: Alex Rodriguez
    Education: Bachelor's in Information Technology
    Experience: Senior level
    Skills: Linux, Docker, Kubernetes, AWS, CI/CD, Jenkins, monitoring, scripting
    Interests: cloud computing, automation, infrastructure, system administration
    """
    
    return user_input, "DevOps Engineer"

def test_product_manager_profile():
    """Test with a product manager profile."""
    print("🧪 Testing Product Manager Profile...")
    
    user_input = """
    Name: Emily Davis
    Education: MBA
    Experience: Mid level
    Skills: product strategy, user research, data analysis, stakeholder management, agile, market research
    Interests: product management, user experience, business strategy, innovation
    """
    
    return user_input, "Product Manager"

def test_cybersecurity_profile():
    """Test with a cybersecurity profile."""
    print("🧪 Testing Cybersecurity Analyst Profile...")
    
    user_input = """
    Name: David Kim
    Education: Bachelor's in Cybersecurity
    Experience: Junior level
    Skills: network security, threat analysis, penetration testing, compliance, incident response
    Interests: cybersecurity, ethical hacking, security research, digital forensics
    """
    
    return user_input, "Cybersecurity Analyst"

def test_ux_designer_profile():
    """Test with a UX designer profile."""
    print("🧪 Testing UX/UI Designer Profile...")
    
    user_input = """
    Name: Lisa Wang
    Education: Bachelor's in Design
    Experience: Mid level
    Skills: user research, wireframing, prototyping, design systems, user testing, figma, sketch
    Interests: user experience, design, human-computer interaction, creative design
    """
    
    return user_input, "UX/UI Designer"

def test_student_profile():
    """Test with a student profile."""
    print("🧪 Testing Student Profile...")
    
    user_input = """
    Name: Tom Wilson
    Education: High School
    Experience: Student
    Skills: basic programming, html, css, some python
    Interests: technology, coding, learning new things, problem solving
    """
    
    return user_input, "Student"

def test_empty_profile():
    """Test with minimal profile information."""
    print("🧪 Testing Empty Profile...")
    
    user_input = """
    Name: Unknown User
    Education: 
    Experience: 
    Skills: 
    Interests: 
    """
    
    return user_input, "Empty Profile"

def run_test_case(career_ai, user_input, expected_career, test_name):
    """Run a single test case."""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")
    
    try:
        # Parse user input
        user_profile = career_ai.parse_user_input(user_input)
        
        # Generate guidance
        guidance_text, json_output = career_ai.generate_guidance(user_profile)
        
        # Display results
        print(f"👤 User: {user_profile.name or 'Not specified'}")
        print(f"🎓 Education: {user_profile.education_level or 'Not specified'}")
        print(f"💼 Experience: {user_profile.experience_level or 'Not specified'}")
        print(f"🛠️ Skills: {', '.join(user_profile.skills) if user_profile.skills else 'None'}")
        
        # Check recommendations
        if json_output["career_recommendations"]:
            top_recommendation = json_output["career_recommendations"][0]
            print(f"\n🏆 Top Recommendation: {top_recommendation['career_track']}")
            print(f"   Match Score: {top_recommendation['match_score']}/100")
            print(f"   Market Demand: {top_recommendation['current_market_demand_score']}/100")
            print(f"   Future Demand: {top_recommendation['future_demand_projection_score']}/100")
            
            # Check if expected career is in top recommendations
            top_careers = [rec['career_track'] for rec in json_output["career_recommendations"][:3]]
            if expected_career in top_careers:
                print(f"✅ Expected career '{expected_career}' found in top recommendations!")
            else:
                print(f"⚠️  Expected career '{expected_career}' not in top 3 recommendations")
                print(f"   Top 3: {', '.join(top_careers)}")
        else:
            print("❌ No career recommendations generated")
        
        # Check skill gaps
        if json_output["skill_gap_analysis"]:
            skill_gap = json_output["skill_gap_analysis"][0]
            print(f"\n📊 Skill Gap Analysis for {skill_gap['career_track']}:")
            print(f"   Skills you have: {', '.join(skill_gap['have_skills']) if skill_gap['have_skills'] else 'None'}")
            print(f"   Skills you need: {', '.join(skill_gap['need_skills']) if skill_gap['need_skills'] else 'None'}")
            print(f"   Priority gaps: {', '.join(skill_gap['priority_gaps']) if skill_gap['priority_gaps'] else 'None'}")
        
        # Check learning path
        if json_output["learning_path"]:
            learning_path = json_output["learning_path"][0]
            print(f"\n📚 Learning Path for {learning_path['career_track']}:")
            print(f"   Timeline: {learning_path['timeline_months']} months")
            print(f"   Phases: {len(learning_path['phases'])}")
            for i, phase in enumerate(learning_path['phases'], 1):
                print(f"   Phase {i}: {phase['phase_name']} ({phase['duration_weeks']} weeks)")
        
        # Save test results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name_clean = test_name.replace(" ", "_").lower()
        
        # Create test output directory
        test_output_dir = "test_output"
        if not os.path.exists(test_output_dir):
            os.makedirs(test_output_dir)
        
        # Save guidance
        guidance_file = os.path.join(test_output_dir, f"test_{test_name_clean}_{timestamp}.txt")
        with open(guidance_file, "w", encoding="utf-8") as f:
            f.write(guidance_text)
        
        # Save JSON
        json_file = os.path.join(test_output_dir, f"test_{test_name_clean}_{timestamp}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_output, f, indent=2)
        
        print(f"\n💾 Test results saved to:")
        print(f"   📄 {guidance_file}")
        print(f"   🔧 {json_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def main():
    """Run all test cases."""
    print("🧪 CareerGuideAI Test Suite")
    print("=" * 60)
    print("Running comprehensive tests with various user profiles...")
    print()
    
    # Initialize CareerGuideAI
    career_ai = CareerGuideAI()
    
    # Define test cases
    test_cases = [
        test_data_scientist_profile,
        test_software_engineer_profile,
        test_devops_engineer_profile,
        test_product_manager_profile,
        test_cybersecurity_profile,
        test_ux_designer_profile,
        test_student_profile,
        test_empty_profile
    ]
    
    # Run tests
    passed = 0
    total = len(test_cases)
    
    for test_func in test_cases:
        user_input, expected_career = test_func()
        test_name = test_func.__name__.replace("_", " ").title()
        
        if run_test_case(career_ai, user_input, expected_career, test_name):
            passed += 1
        
        print("\n" + "-" * 60)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! CareerGuideAI is working correctly.")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
    
    print("\n📁 Test results saved in 'test_output/' directory")
    print("=" * 60)

if __name__ == "__main__":
    main() 