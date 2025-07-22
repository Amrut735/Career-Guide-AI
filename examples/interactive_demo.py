#!/usr/bin/env python3
"""
Interactive Demo for CareerGuideAI
A user-friendly interface to test the career guidance system.
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path to import CareerGuideAI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from career_guide_ai import CareerGuideAI

def print_banner():
    """Print the CareerGuideAI banner."""
    print("=" * 70)
    print("🚀 CareerGuideAI - Advanced AI Career Counselor")
    print("=" * 70)
    print("Your personalized career guidance and future skill forecaster")
    print("=" * 70)
    print()

def get_user_input():
    """Get user input interactively."""
    print("📝 Please provide your information (press Enter to skip any field):")
    print()
    
    user_data = {}
    
    # Basic information
    user_data["name"] = input("👤 Your name: ").strip() or None
    user_data["education"] = input("🎓 Education level (e.g., High School, Bachelor's, Master's, PhD): ").strip() or None
    user_data["experience"] = input("💼 Experience level (student/fresher/junior/mid/senior): ").strip() or None
    
    print("\n🛠️ Skills (comma-separated, e.g., Python, JavaScript, SQL):")
    skills_input = input("   Your skills: ").strip()
    user_data["skills"] = [skill.strip() for skill in skills_input.split(",") if skill.strip()] if skills_input else []
    
    print("\n🎯 Interests (comma-separated, e.g., AI, web development, data science):")
    interests_input = input("   Your interests: ").strip()
    user_data["interests"] = [interest.strip() for interest in interests_input.split(",") if interest.strip()] if interests_input else []
    
    print("\n📚 Learning style (optional - visual/auditory/kinesthetic):")
    user_data["learning_style"] = input("   Your learning style: ").strip() or None
    
    return user_data

def format_user_input(user_data):
    """Format user data into the expected input format."""
    formatted = f"""
Name: {user_data.get('name', '')}
Education: {user_data.get('education', '')}
Experience: {user_data.get('experience', '')}
Skills: {', '.join(user_data.get('skills', []))}
Interests: {', '.join(user_data.get('interests', []))}
Learning Style: {user_data.get('learning_style', '')}
"""
    return formatted

def save_results(guidance_text, json_output, user_name=None):
    """Save results to files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name_suffix = f"_{user_name.replace(' ', '_')}" if user_name else ""
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save human-readable guidance
    guidance_file = os.path.join(output_dir, f"career_guidance{name_suffix}_{timestamp}.txt")
    with open(guidance_file, "w", encoding="utf-8") as f:
        f.write(guidance_text)
    
    # Save JSON output
    json_file = os.path.join(output_dir, f"career_guidance{name_suffix}_{timestamp}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=2)
    
    print(f"\n💾 Results saved to:")
    print(f"   📄 {guidance_file}")
    print(f"   🔧 {json_file}")
    
    return guidance_file, json_file

def display_quick_summary(json_output):
    """Display a quick summary of the results."""
    print("\n" + "=" * 50)
    print("🎯 QUICK SUMMARY")
    print("=" * 50)
    
    user_summary = json_output["user_summary"]
    print(f"👤 Profile: {user_summary['name'] or 'Not specified'}")
    print(f"🎓 Education: {user_summary['education_level'] or 'Not specified'}")
    print(f"💼 Experience: {user_summary['experience_level'] or 'Not specified'}")
    print(f"🛠️ Skills: {', '.join(user_summary['skills_normalized']) if user_summary['skills_normalized'] else 'None'}")
    
    if json_output["career_recommendations"]:
        top_career = json_output["career_recommendations"][0]
        print(f"\n🏆 TOP RECOMMENDATION: {top_career['career_track']}")
        print(f"   Match Score: {top_career['match_score']}/100")
        print(f"   Market Demand: {top_career['current_market_demand_score']}/100")
        print(f"   Future Demand: {top_career['future_demand_projection_score']}/100")
    
    print("=" * 50)

def main():
    """Main interactive demo function."""
    print_banner()
    
    try:
        # Initialize CareerGuideAI
        print("🤖 Initializing CareerGuideAI...")
        career_ai = CareerGuideAI()
        print("✅ System ready!")
        print()
        
        # Get user input
        user_data = get_user_input()
        
        # Format input
        user_input = format_user_input(user_data)
        
        print("\n🔍 Analyzing your profile...")
        print("⏳ Generating career recommendations...")
        print("📊 Creating learning roadmap...")
        print("🔮 Predicting future skills...")
        print()
        
        # Generate guidance
        user_profile = career_ai.parse_user_input(user_input)
        guidance_text, json_output = career_ai.generate_guidance(user_profile)
        
        # Display quick summary
        display_quick_summary(json_output)
        
        # Ask user if they want to see full results
        print("\n📋 Would you like to see the full detailed guidance?")
        show_full = input("   (y/n): ").lower().strip() in ['y', 'yes', '1']
        
        if show_full:
            print("\n" + "=" * 70)
            print("📋 FULL CAREER GUIDANCE")
            print("=" * 70)
            print(guidance_text)
        
        # Save results
        guidance_file, json_file = save_results(guidance_text, json_output, user_data.get('name'))
        
        # Ask if user wants to see JSON structure
        print("\n🔧 Would you like to see the JSON structure for programmatic use?")
        show_json = input("   (y/n): ").lower().strip() in ['y', 'yes', '1']
        
        if show_json:
            print("\n" + "=" * 50)
            print("🔧 JSON STRUCTURE")
            print("=" * 50)
            print(json.dumps(json_output, indent=2))
        
        print("\n🎉 Thank you for using CareerGuideAI!")
        print("💡 Use the saved files for future reference and planning.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your input and try again.")

if __name__ == "__main__":
    main() 