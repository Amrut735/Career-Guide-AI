#!/usr/bin/env python3
"""
CareerGuideAI - Advanced AI Career Counselor and Future Skill Forecaster
A comprehensive system for career guidance, skill analysis, and future trend prediction.
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import random

@dataclass
class UserProfile:
    name: Optional[str] = None
    education_level: Optional[str] = None
    experience_level: Optional[str] = None
    skills: List[str] = None
    interests: List[str] = None
    learning_style: Optional[str] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.interests is None:
            self.interests = []

@dataclass
class CareerRecommendation:
    career_track: str
    match_score: int
    current_market_demand_score: int
    future_demand_projection_score: int
    why_recommended: str
    top_recommended_skills: List[str]
    emerging_skills: List[str]

@dataclass
class SkillGapAnalysis:
    career_track: str
    have_skills: List[str]
    need_skills: List[str]
    priority_gaps: List[str]

@dataclass
class LearningPhase:
    phase_name: str
    duration_weeks: int
    focus_skills: List[str]
    recommended_projects: List[str]
    recommended_certifications: List[str]
    practice_resources: List[Dict[str, str]]

@dataclass
class LearningPath:
    career_track: str
    timeline_months: int
    phases: List[LearningPhase]

@dataclass
class ResumeBooster:
    career_track: str
    project_ideas: List[str]
    resume_bullets_sample: List[str]

class CareerGuideAI:
    def __init__(self):
        self.career_tracks = {
            "Data Scientist": {
                "core_skills": ["python", "statistics", "machine learning", "sql", "data analysis"],
                "emerging_skills": ["genai", "mlops", "llm", "vector databases", "ai ethics"],
                "market_demand": 95,
                "future_demand": 98,
                "growth_rate": 35
            },
            "Software Engineer": {
                "core_skills": ["programming", "algorithms", "data structures", "version control", "testing"],
                "emerging_skills": ["cloud native", "microservices", "devops", "kubernetes", "serverless"],
                "market_demand": 90,
                "future_demand": 92,
                "growth_rate": 25
            },
            "DevOps Engineer": {
                "core_skills": ["linux", "docker", "kubernetes", "ci/cd", "cloud platforms"],
                "emerging_skills": ["gitops", "observability", "platform engineering", "security", "aiops"],
                "market_demand": 88,
                "future_demand": 95,
                "growth_rate": 40
            },
            "Product Manager": {
                "core_skills": ["product strategy", "user research", "data analysis", "stakeholder management", "agile"],
                "emerging_skills": ["ai product management", "data-driven decisions", "customer success", "growth hacking"],
                "market_demand": 85,
                "future_demand": 88,
                "growth_rate": 20
            },
            "Cybersecurity Analyst": {
                "core_skills": ["network security", "threat analysis", "incident response", "compliance", "penetration testing"],
                "emerging_skills": ["zero trust", "cloud security", "ai security", "threat intelligence", "devsecops"],
                "market_demand": 92,
                "future_demand": 96,
                "growth_rate": 45
            },
            "UX/UI Designer": {
                "core_skills": ["user research", "wireframing", "prototyping", "design systems", "user testing"],
                "emerging_skills": ["ai-powered design", "voice ui", "ar/vr design", "accessibility", "design ops"],
                "market_demand": 82,
                "future_demand": 85,
                "growth_rate": 18
            },
            "Cloud Architect": {
                "core_skills": ["cloud platforms", "architecture design", "infrastructure", "networking", "security"],
                "emerging_skills": ["multi-cloud", "edge computing", "serverless", "cloud native", "finops"],
                "market_demand": 90,
                "future_demand": 94,
                "growth_rate": 32
            },
            "AI/ML Engineer": {
                "core_skills": ["machine learning", "deep learning", "python", "tensorflow", "pytorch"],
                "emerging_skills": ["genai", "llm", "mlops", "ai ethics", "federated learning"],
                "market_demand": 96,
                "future_demand": 99,
                "growth_rate": 50
            }
        }
        
        self.skill_normalization = {
            "python": ["python", "py", "programming"],
            "javascript": ["javascript", "js", "node.js", "react", "vue", "angular"],
            "java": ["java", "spring", "android"],
            "sql": ["sql", "database", "mysql", "postgresql"],
            "machine learning": ["ml", "machine learning", "ai", "artificial intelligence"],
            "data analysis": ["data analysis", "analytics", "excel", "tableau", "power bi"],
            "cloud": ["aws", "azure", "gcp", "cloud", "docker", "kubernetes"],
            "devops": ["devops", "ci/cd", "jenkins", "gitlab", "github actions"],
            "security": ["cybersecurity", "security", "penetration testing", "ethical hacking"],
            "design": ["ui", "ux", "design", "figma", "sketch", "adobe"]
        }
        
        self.learning_resources = {
            "courses": [
                {"title": "Coursera Specializations", "provider": "Coursera", "url_placeholder": "coursera.org"},
                {"title": "Udemy Best Sellers", "provider": "Udemy", "url_placeholder": "udemy.com"},
                {"title": "edX MicroMasters", "provider": "edX", "url_placeholder": "edx.org"},
                {"title": "DataCamp Tracks", "provider": "DataCamp", "url_placeholder": "datacamp.com"}
            ],
            "books": [
                {"title": "Industry Standard Books", "provider": "Various Publishers", "url_placeholder": "amazon.com"},
                {"title": "O'Reilly Learning", "provider": "O'Reilly", "url_placeholder": "oreilly.com"}
            ],
            "practice": [
                {"title": "LeetCode Problems", "provider": "LeetCode", "url_placeholder": "leetcode.com"},
                {"title": "HackerRank Challenges", "provider": "HackerRank", "url_placeholder": "hackerrank.com"},
                {"title": "Kaggle Competitions", "provider": "Kaggle", "url_placeholder": "kaggle.com"},
                {"title": "GitHub Projects", "provider": "GitHub", "url_placeholder": "github.com"}
            ]
        }

    def normalize_skills(self, skills: List[str]) -> List[str]:
        """Normalize and standardize skill names."""
        normalized = []
        for skill in skills:
            skill_lower = skill.lower().strip()
            found = False
            for standard, variants in self.skill_normalization.items():
                if skill_lower in variants or skill_lower == standard:
                    normalized.append(standard)
                    found = True
                    break
            if not found:
                normalized.append(skill_lower)
        return list(set(normalized))

    def calculate_match_score(self, user_skills: List[str], career_skills: List[str]) -> int:
        """Calculate match score between user skills and career requirements."""
        if not career_skills:
            return 0
        
        user_skills_set = set(user_skills)
        career_skills_set = set(career_skills)
        
        # Calculate intersection
        matching_skills = user_skills_set.intersection(career_skills_set)
        
        # Calculate match percentage
        match_percentage = len(matching_skills) / len(career_skills_set) * 100
        
        # Bonus for having more skills than required
        bonus = min(10, len(user_skills_set) - len(career_skills_set))
        
        return min(100, int(match_percentage + bonus))

    def get_demand_label(self, growth_rate: float) -> str:
        """Get demand label based on growth rate."""
        if growth_rate > 30:
            return "High Emerging Demand"
        elif growth_rate > 15:
            return "Growing Steadily"
        else:
            return "Stable"

    def generate_career_recommendations(self, user_profile: UserProfile) -> List[CareerRecommendation]:
        """Generate career recommendations based on user profile."""
        recommendations = []
        normalized_skills = self.normalize_skills(user_profile.skills)
        
        for career, data in self.career_tracks.items():
            match_score = self.calculate_match_score(normalized_skills, data["core_skills"])
            
            # Generate why recommended text
            matching_skills = set(normalized_skills).intersection(set(data["core_skills"]))
            why_recommended = f"Strong match with {len(matching_skills)} core skills. "
            why_recommended += f"High {self.get_demand_label(data['growth_rate'])} with {data['growth_rate']}% growth rate."
            
            recommendation = CareerRecommendation(
                career_track=career,
                match_score=match_score,
                current_market_demand_score=data["market_demand"],
                future_demand_projection_score=data["future_demand"],
                why_recommended=why_recommended,
                top_recommended_skills=data["core_skills"][:5],
                emerging_skills=data["emerging_skills"]
            )
            recommendations.append(recommendation)
        
        # Sort by match score and return top 5
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations[:5]

    def analyze_skill_gaps(self, user_profile: UserProfile, career_track: str) -> SkillGapAnalysis:
        """Analyze skill gaps for a specific career track."""
        normalized_skills = self.normalize_skills(user_profile.skills)
        career_data = self.career_tracks[career_track]
        
        have_skills = list(set(normalized_skills).intersection(set(career_data["core_skills"])))
        need_skills = [skill for skill in career_data["core_skills"] if skill not in normalized_skills]
        
        # Prioritize gaps based on importance and market demand
        priority_gaps = need_skills[:3]  # Top 3 priority skills to learn
        
        return SkillGapAnalysis(
            career_track=career_track,
            have_skills=have_skills,
            need_skills=need_skills,
            priority_gaps=priority_gaps
        )

    def generate_learning_path(self, career_track: str, user_profile: UserProfile) -> LearningPath:
        """Generate a personalized learning path for a career track."""
        career_data = self.career_tracks[career_track]
        normalized_skills = self.normalize_skills(user_profile.skills)
        
        # Determine experience level and adjust timeline
        experience_multiplier = {
            "student": 1.5,
            "fresher": 1.2,
            "junior": 1.0,
            "mid": 0.8,
            "senior": 0.6
        }
        
        # Adjust timeline based on education level
        education_multiplier = {
            "High School": 1.3,
            "Bachelor's Degree": 1.0,
            "Master's Degree": 0.8,
            "PhD": 0.7
        }
        
        base_timeline = 12  # 12 months base timeline
        exp_multiplier = experience_multiplier.get(user_profile.experience_level, 1.0)
        edu_multiplier = education_multiplier.get(user_profile.education_level, 1.0)
        timeline_months = int(base_timeline * exp_multiplier * edu_multiplier)
        
        # Generate personalized learning phases
        phases = []
        
        # Phase 1: Foundation (personalized duration)
        foundation_skills = [skill for skill in career_data["core_skills"][:3] if skill not in normalized_skills]
        foundation_duration = max(4, min(8, len(foundation_skills) * 2))  # 4-8 weeks based on skill gaps
        
        # Personalized foundation projects based on background
        foundation_projects = self._get_personalized_projects(career_track, "foundation", user_profile)
        
        phases.append(LearningPhase(
            phase_name="Foundation",
            duration_weeks=foundation_duration,
            focus_skills=foundation_skills,
            recommended_projects=foundation_projects,
            recommended_certifications=self._get_personalized_certifications(career_track, "foundation", user_profile),
            practice_resources=self._get_personalized_resources(career_track, "foundation", user_profile)
        ))
        
        # Phase 2: Advanced (personalized duration)
        advanced_skills = career_data["core_skills"][3:] + career_data["emerging_skills"][:2]
        advanced_duration = max(6, min(12, len(advanced_skills) * 1.5))  # 6-12 weeks based on skill complexity
        
        advanced_projects = self._get_personalized_projects(career_track, "advanced", user_profile)
        
        phases.append(LearningPhase(
            phase_name="Advanced",
            duration_weeks=advanced_duration,
            focus_skills=advanced_skills,
            recommended_projects=advanced_projects,
            recommended_certifications=self._get_personalized_certifications(career_track, "advanced", user_profile),
            practice_resources=self._get_personalized_resources(career_track, "advanced", user_profile)
        ))
        
        # Phase 3: Specialization (personalized duration)
        specialization_skills = career_data["emerging_skills"]
        specialization_duration = max(4, min(10, len(specialization_skills) * 1.2))  # 4-10 weeks
        
        specialization_projects = self._get_personalized_projects(career_track, "specialization", user_profile)
        
        phases.append(LearningPhase(
            phase_name="Specialization",
            duration_weeks=specialization_duration,
            focus_skills=specialization_skills,
            recommended_projects=specialization_projects,
            recommended_certifications=self._get_personalized_certifications(career_track, "specialization", user_profile),
            practice_resources=self._get_personalized_resources(career_track, "specialization", user_profile)
        ))
        
        return LearningPath(
            career_track=career_track,
            timeline_months=timeline_months,
            phases=phases
        )
    
    def _get_personalized_projects(self, career_track: str, phase: str, user_profile: UserProfile) -> List[str]:
        """Generate personalized project ideas based on user background."""
        projects = []
        
        # Base projects by career track and phase
        base_projects = {
            "Data Scientist": {
                "foundation": [
                    "Build a data analysis dashboard using Python and Pandas",
                    "Create a simple machine learning model for prediction",
                    "Analyze a real-world dataset and create visualizations"
                ],
                "advanced": [
                    "Develop a recommendation system using collaborative filtering",
                    "Build a natural language processing pipeline",
                    "Create a time series forecasting model"
                ],
                "specialization": [
                    "Build a GenAI-powered chatbot using LLMs",
                    "Develop an MLOps pipeline for model deployment",
                    "Create a vector database for semantic search"
                ]
            },
            "Software Engineer": {
                "foundation": [
                    "Build a RESTful API using Python/Node.js",
                    "Create a simple web application with frontend and backend",
                    "Develop a command-line tool for automation"
                ],
                "advanced": [
                    "Build a microservices architecture",
                    "Create a real-time chat application",
                    "Develop a mobile app with React Native"
                ],
                "specialization": [
                    "Build a cloud-native application with Kubernetes",
                    "Develop a serverless application using AWS Lambda",
                    "Create a CI/CD pipeline with GitHub Actions"
                ]
            },
            "AI/ML Engineer": {
                "foundation": [
                    "Implement basic ML algorithms from scratch",
                    "Build a neural network using TensorFlow/PyTorch",
                    "Create a computer vision application"
                ],
                "advanced": [
                    "Develop a deep learning model for image classification",
                    "Build a recommendation system using neural networks",
                    "Create a natural language processing model"
                ],
                "specialization": [
                    "Fine-tune a large language model for specific tasks",
                    "Build a multimodal AI system",
                    "Develop an AI ethics framework for your models"
                ]
            }
        }
        
        # Get base projects for the career track and phase
        if career_track in base_projects and phase in base_projects[career_track]:
            projects.extend(base_projects[career_track][phase])
        
        # Add personalized projects based on user background
        if user_profile.experience_level == "student":
            projects.append("Create a portfolio website showcasing your projects")
            projects.append("Participate in hackathons and coding competitions")
        elif user_profile.experience_level == "fresher":
            projects.append("Build projects that demonstrate your technical skills")
            projects.append("Contribute to open-source projects in your field")
        elif user_profile.experience_level in ["junior", "mid"]:
            projects.append("Build production-ready applications with best practices")
            projects.append("Create tools that improve team productivity")
        elif user_profile.experience_level == "senior":
            projects.append("Architect and lead development of complex systems")
            projects.append("Mentor junior developers and create learning resources")
        
        # Add projects based on education level
        if user_profile.education_level == "PhD":
            projects.append("Publish research papers or technical blog posts")
        elif user_profile.education_level == "Master's Degree":
            projects.append("Work on advanced research or thesis projects")
        
        return projects[:4]  # Limit to 4 projects
    
    def _get_personalized_certifications(self, career_track: str, phase: str, user_profile: UserProfile) -> List[str]:
        """Generate personalized certification recommendations."""
        certifications = []
        
        # Base certifications by career track
        base_certifications = {
            "Data Scientist": {
                "foundation": ["Python for Data Science", "SQL Fundamentals"],
                "advanced": ["Machine Learning Specialization", "Deep Learning Certification"],
                "specialization": ["AWS Machine Learning", "Google Cloud AI/ML"]
            },
            "Software Engineer": {
                "foundation": ["Programming Fundamentals", "Web Development"],
                "advanced": ["Software Architecture", "System Design"],
                "specialization": ["AWS Solutions Architect", "Google Cloud Professional"]
            },
            "AI/ML Engineer": {
                "foundation": ["Machine Learning Basics", "Python for AI"],
                "advanced": ["Deep Learning Specialization", "NLP Certification"],
                "specialization": ["AI Ethics Certification", "MLOps Professional"]
            }
        }
        
        if career_track in base_certifications and phase in base_certifications[career_track]:
            certifications.extend(base_certifications[career_track][phase])
        
        # Add certifications based on experience level
        if user_profile.experience_level == "student":
            certifications.append("Student-focused certifications and courses")
        elif user_profile.experience_level in ["junior", "mid"]:
            certifications.append("Industry-recognized professional certifications")
        elif user_profile.experience_level == "senior":
            certifications.append("Advanced and leadership certifications")
        
        return certifications[:3]  # Limit to 3 certifications
    
    def _get_personalized_resources(self, career_track: str, phase: str, user_profile: UserProfile) -> List[Dict[str, str]]:
        """Generate personalized learning resources."""
        resources = []
        
        # Base resources
        if phase == "foundation":
            resources.extend(self.learning_resources["courses"][:2])
            resources.extend(self.learning_resources["practice"][:1])
        elif phase == "advanced":
            resources.extend(self.learning_resources["courses"][2:])
            resources.extend(self.learning_resources["books"])
        else:  # specialization
            resources.extend(self.learning_resources["practice"][2:])
            resources.extend(self.learning_resources["courses"][:1])
        
        # Add personalized resources based on background
        if user_profile.experience_level == "student":
            resources.append({"title": "Free Student Resources", "provider": "Various", "url_placeholder": "github.com/student-resources"})
        elif user_profile.experience_level == "senior":
            resources.append({"title": "Advanced Technical Papers", "provider": "arXiv", "url_placeholder": "arxiv.org"})
        
        return resources

    def generate_resume_boosters(self, career_track: str) -> ResumeBooster:
        """Generate project ideas and resume bullets for a career track."""
        career_data = self.career_tracks[career_track]
        
        project_ideas = [
            f"Developed a {career_track.lower()} solution using modern technologies",
            f"Built an automated system for {career_track.lower()} tasks",
            f"Created a data-driven {career_track.lower()} application",
            f"Implemented best practices in {career_track.lower()} development"
        ]
        
        resume_bullets = [
            f"Led {career_track.lower()} initiatives resulting in 25% efficiency improvement",
            f"Developed scalable solutions using {', '.join(career_data['core_skills'][:3])}",
            f"Collaborated with cross-functional teams to deliver high-impact projects",
            f"Stayed current with emerging technologies including {', '.join(career_data['emerging_skills'][:2])}"
        ]
        
        return ResumeBooster(
            career_track=career_track,
            project_ideas=project_ideas,
            resume_bullets_sample=resume_bullets
        )

    def parse_user_input(self, user_input: str) -> UserProfile:
        """Parse user input to extract profile information."""
        profile = UserProfile()
        
        # Extract name
        name_match = re.search(r"name[:\s]+([^\n,]+)", user_input, re.IGNORECASE)
        if name_match:
            profile.name = name_match.group(1).strip()
        
        # Extract education level
        education_keywords = {
            "high school": "High School",
            "bachelor": "Bachelor's Degree",
            "master": "Master's Degree",
            "phd": "PhD",
            "doctorate": "PhD"
        }
        
        for keyword, level in education_keywords.items():
            if keyword in user_input.lower():
                profile.education_level = level
                break
        
        # Extract experience level
        experience_keywords = {
            "student": "student",
            "fresher": "fresher",
            "junior": "junior",
            "mid": "mid",
            "senior": "senior"
        }
        
        for keyword, level in experience_keywords.items():
            if keyword in user_input.lower():
                profile.experience_level = level
                break
        
        # Extract skills (look for common skill patterns)
        skills = []
        for skill_list in self.skill_normalization.values():
            for skill in skill_list:
                if skill in user_input.lower():
                    skills.append(skill)
        
        # Add any other skills mentioned
        skill_patterns = [
            r"skills?[:\s]+([^.\n]+)",
            r"know[:\s]+([^.\n]+)",
            r"experience[:\s]+([^.\n]+)"
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            for match in matches:
                skills.extend([s.strip() for s in match.split(',')])
        
        profile.skills = list(set(skills))
        
        # Extract interests
        interest_patterns = [
            r"interest[:\s]+([^.\n]+)",
            r"like[:\s]+([^.\n]+)",
            r"passion[:\s]+([^.\n]+)"
        ]
        
        interests = []
        for pattern in interest_patterns:
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            for match in matches:
                interests.extend([s.strip() for s in match.split(',')])
        
        profile.interests = list(set(interests))
        
        return profile

    def generate_guidance(self, user_profile: UserProfile) -> Tuple[str, Dict[str, Any]]:
        """Generate comprehensive career guidance."""
        # Generate recommendations
        recommendations = self.generate_career_recommendations(user_profile)
        
        # Generate skill gap analysis for top recommendation
        top_career = recommendations[0].career_track if recommendations else None
        skill_gaps = []
        learning_paths = []
        resume_boosters = []
        
        if top_career:
            skill_gaps.append(self.analyze_skill_gaps(user_profile, top_career))
            learning_paths.append(self.generate_learning_path(top_career, user_profile))
            resume_boosters.append(self.generate_resume_boosters(top_career))
        
        # Generate human-readable guidance
        guidance_text = self._generate_human_guidance(user_profile, recommendations, skill_gaps, learning_paths, resume_boosters)
        
        # Generate JSON output
        json_output = self._generate_json_output(user_profile, recommendations, skill_gaps, learning_paths, resume_boosters)
        
        return guidance_text, json_output

    def _generate_human_guidance(self, user_profile: UserProfile, recommendations: List[CareerRecommendation], 
                               skill_gaps: List[SkillGapAnalysis], learning_paths: List[LearningPath], 
                               resume_boosters: List[ResumeBooster]) -> str:
        """Generate human-readable guidance text."""
        guidance = f"""
# 🚀 CareerGuideAI - Your Personalized Career Roadmap

## 👤 Your Profile Summary
- **Name:** {user_profile.name or 'Not specified'}
- **Education Level:** {user_profile.education_level or 'Not specified'}
- **Experience Level:** {user_profile.experience_level or 'Not specified'}
- **Skills Identified:** {', '.join(user_profile.skills) if user_profile.skills else 'None specified'}
- **Interests:** {', '.join(user_profile.interests) if user_profile.interests else 'None specified'}

## 🎯 Best Career Matches
"""
        
        for i, rec in enumerate(recommendations, 1):
            guidance += f"""
### {i}. {rec.career_track}
- **Match Score:** {rec.match_score}/100
- **Current Market Demand:** {rec.current_market_demand_score}/100
- **Future Demand Projection:** {rec.future_demand_projection_score}/100
- **Why Recommended:** {rec.why_recommended}
"""
        
        if skill_gaps:
            gap = skill_gaps[0]
            guidance += f"""
## 💪 Skills You Have
{', '.join(gap.have_skills) if gap.have_skills else 'None identified'}

## 📚 Skills to Learn
{', '.join(gap.need_skills) if gap.need_skills else 'All core skills covered'}

## 🎯 Priority Skills to Focus On
{', '.join(gap.priority_gaps) if gap.priority_gaps else 'No immediate gaps identified'}
"""
        
        if learning_paths:
            path = learning_paths[0]
            guidance += f"""
## 🛣️ Learning Roadmap for {path.career_track}
**Timeline:** {path.timeline_months} months

"""
            for phase in path.phases:
                guidance += f"""
### {phase.phase_name} Phase ({phase.duration_weeks} weeks)
**Focus Skills:** {', '.join(phase.focus_skills)}
**Projects:** {', '.join(phase.recommended_projects)}
**Certifications:** {', '.join(phase.recommended_certifications)}
"""
        
        guidance += """
## 🔮 Emerging Trends to Watch
- **GenAI & LLMs:** Transformative impact across all tech roles
- **MLOps & AI Engineering:** Growing demand for AI infrastructure
- **Cloud Native & Kubernetes:** Standard for modern applications
- **Cybersecurity:** Increasing importance with digital transformation
- **DevOps & Platform Engineering:** Streamlining development workflows

## 💡 Actionable Next Steps
1. **Start with the Foundation Phase** of your chosen career path
2. **Build a portfolio** with the recommended projects
3. **Earn relevant certifications** to validate your skills
4. **Network with professionals** in your target field
5. **Stay updated** with emerging technologies and trends

## 📈 Market Insights
- Tech roles are experiencing 20-50% growth rates
- Remote work is expanding opportunities globally
- Continuous learning is essential for career advancement
- Specialized skills command premium salaries

---
*Generated by CareerGuideAI - Your AI Career Counselor*
"""
        
        return guidance

    def _generate_json_output(self, user_profile: UserProfile, recommendations: List[CareerRecommendation],
                            skill_gaps: List[SkillGapAnalysis], learning_paths: List[LearningPath],
                            resume_boosters: List[ResumeBooster]) -> Dict[str, Any]:
        """Generate structured JSON output."""
        return {
            "user_summary": {
                "name": user_profile.name,
                "education_level": user_profile.education_level,
                "experience_level": user_profile.experience_level,
                "skills_normalized": self.normalize_skills(user_profile.skills),
                "interests_normalized": user_profile.interests
            },
            "career_recommendations": [
                {
                    "career_track": rec.career_track,
                    "match_score": rec.match_score,
                    "current_market_demand_score": rec.current_market_demand_score,
                    "future_demand_projection_score": rec.future_demand_projection_score,
                    "why_recommended": rec.why_recommended,
                    "top_recommended_skills": rec.top_recommended_skills,
                    "emerging_skills": rec.emerging_skills
                }
                for rec in recommendations
            ],
            "skill_gap_analysis": [
                {
                    "career_track": gap.career_track,
                    "have_skills": gap.have_skills,
                    "need_skills": gap.need_skills,
                    "priority_gaps": gap.priority_gaps
                }
                for gap in skill_gaps
            ],
            "learning_path": [
                {
                    "career_track": path.career_track,
                    "timeline_months": path.timeline_months,
                    "phases": [
                        {
                            "phase_name": phase.phase_name,
                            "duration_weeks": phase.duration_weeks,
                            "focus_skills": phase.focus_skills,
                            "recommended_projects": phase.recommended_projects,
                            "recommended_certifications": phase.recommended_certifications,
                            "practice_resources": phase.practice_resources
                        }
                        for phase in path.phases
                    ]
                }
                for path in learning_paths
            ],
            "resume_boosters": [
                {
                    "career_track": booster.career_track,
                    "project_ideas": booster.project_ideas,
                    "resume_bullets_sample": booster.resume_bullets_sample
                }
                for booster in resume_boosters
            ],
            "clarifications_needed": [],
            "meta": {
                "version": "1.0",
                "model_notes": "CareerGuideAI - Advanced career counseling system with future skill prediction",
                "confidence_notes": "Recommendations based on current market trends and projected growth rates"
            }
        }

def main():
    """Main function to demonstrate CareerGuideAI functionality."""
    print("🚀 Welcome to CareerGuideAI - Your Advanced Career Counselor!")
    print("=" * 60)
    
    # Initialize the AI system
    career_ai = CareerGuideAI()
    
    # Example user input
    example_input = """
    Name: John Smith
    Education: Bachelor's degree in Computer Science
    Experience: Junior level
    Skills: Python, JavaScript, SQL, basic machine learning
    Interests: AI, data science, web development
    """
    
    print("📝 Analyzing your profile...")
    user_profile = career_ai.parse_user_input(example_input)
    
    print("🎯 Generating career recommendations...")
    guidance_text, json_output = career_ai.generate_guidance(user_profile)
    
    # Display human-readable guidance
    print("\n" + "=" * 60)
    print("📋 HUMAN GUIDANCE")
    print("=" * 60)
    print(guidance_text)
    
    # Display JSON output
    print("\n" + "=" * 60)
    print("🔧 JSON OUTPUT")
    print("=" * 60)
    print(json.dumps(json_output, indent=2))
    
    # Save outputs to files
    with open("career_guidance.txt", "w", encoding="utf-8") as f:
        f.write(guidance_text)
    
    with open("career_guidance.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=2)
    
    print(f"\n✅ Outputs saved to:")
    print("   - career_guidance.txt (Human-readable guidance)")
    print("   - career_guidance.json (Structured data)")

if __name__ == "__main__":
    main() 