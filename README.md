# 🚀 CareerGuideAI - Advanced AI Career Counselor

A comprehensive, professional AI-powered career guidance system that provides personalized career recommendations, skill gap analysis, learning roadmaps, and future skill predictions.

## ✨ Features

### 🎯 Core Functionalities
- **Smart Profile Parsing**: Automatically extracts skills, education, experience, and interests from user input
- **Career Matching**: Ranks top 3-5 career tracks with match scores (0-100)
- **Market Analysis**: Provides current and future demand projections
- **Skill Gap Analysis**: Identifies skills you have vs. skills you need
- **Personalized Learning Paths**: Creates structured learning phases with timelines
- **Future Skill Prediction**: Forecasts emerging skills and tech trends

### 📊 Advanced Analytics
- **Match Scoring**: Intelligent algorithm that considers skill overlap and experience level
- **Demand Forecasting**: Projects 2-5 year growth trends for each career path
- **Emerging Skills Detection**: Identifies high-growth skills like GenAI, MLOps, Blockchain
- **Resource Recommendations**: Suggests courses, books, and practice platforms

### 🎨 Multiple Interfaces
- **Web Application**: Beautiful, responsive web interface with interactive features
- **Command Line**: Terminal-based interface for quick analysis
- **API Integration**: JSON output for programmatic use
- **PDF Reports**: Professional downloadable career guidance reports

## 🏗️ Architecture

The system is built with a modular, extensible architecture:

```
CareerGuideAI/
├── career_guide_ai.py    # Main system with all core logic
├── app.py               # Flask web application
├── run_web_app.py       # Web app startup script
├── requirements.txt     # Dependencies
├── README.md           # This file
├── templates/          # HTML templates for web UI
├── examples/           # Example usage and test cases
└── output/             # Generated guidance files
```

## 🚀 Quick Start

### 1. Local Development
```bash
# Clone the repository
git clone https://github.com/Amrut735/Career-Guide-AI.git
cd Career-Guide-AI

# Install dependencies
pip install -r requirements.txt

# Run the web application
python app.py
# The web app will be available at http://localhost:5000
```

### 2. Deploy to the Internet (Make it Public)

**Option A: Google Cloud Platform (Recommended)**
```bash
# Follow the detailed guide in DEPLOYMENT_GUIDE.md
# Quick steps:
gcloud auth login
gcloud projects create career-guide-ai-[YOUR-UNIQUE-ID]
gcloud config set project career-guide-ai-[YOUR-UNIQUE-ID]
gcloud app deploy
```

**Option B: Heroku (Free Tier Available)**
```bash
# Install Heroku CLI and deploy
heroku create career-guide-ai
git push heroku main
```

**Option C: Railway (Free Tier Available)**
```bash
# Install Railway CLI and deploy
npm install -g @railway/cli
railway login
railway up
```

### 3. Command Line Interface
```bash
# Run the interactive demo
python examples/interactive_demo.py

# Run the main system
python career_guide_ai.py
```

### 2. Basic Usage
```python
from career_guide_ai import CareerGuideAI

# Initialize the system
career_ai = CareerGuideAI()

# Parse user input
user_input = """
Name: John Smith
Education: Bachelor's in Computer Science
Experience: Junior level
Skills: Python, JavaScript, SQL, basic machine learning
Interests: AI, data science, web development
"""

# Generate comprehensive guidance
user_profile = career_ai.parse_user_input(user_input)
guidance_text, json_output = career_ai.generate_guidance(user_profile)

# Display results
print(guidance_text)
print(json.dumps(json_output, indent=2))
```

### 3. Example Output

**Human Guidance:**
```
# 🚀 CareerGuideAI - Your Personalized Career Roadmap

## 👤 Your Profile Summary
- Name: John Smith
- Education Level: Bachelor's Degree
- Experience Level: junior
- Skills Identified: python, javascript, sql, machine learning
- Interests: ai, data science, web development

## 🎯 Best Career Matches

### 1. AI/ML Engineer
- Match Score: 85/100
- Current Market Demand: 96/100
- Future Demand Projection: 99/100
- Why Recommended: Strong match with 3 core skills. High High Emerging Demand with 50% growth rate.
```

## 🎯 Supported Career Tracks

The system currently supports 8 high-demand career tracks:

1. **Data Scientist** - Analytics, ML, Statistics
2. **Software Engineer** - Programming, Algorithms, Development
3. **DevOps Engineer** - Infrastructure, CI/CD, Cloud
4. **Product Manager** - Strategy, User Research, Analytics
5. **Cybersecurity Analyst** - Security, Threat Analysis, Compliance
6. **UX/UI Designer** - Design, User Research, Prototyping
7. **Cloud Architect** - Cloud Platforms, Architecture, Infrastructure
8. **AI/ML Engineer** - Machine Learning, Deep Learning, AI

## 🔮 Future Skill Prediction

The system predicts emerging skills based on:
- **High Emerging Demand** (>30% growth): GenAI, MLOps, Blockchain
- **Growing Steadily** (15-30% growth): Cloud Native, Kubernetes, DevOps
- **Stable** (<15% growth): Traditional programming, basic design

## 📚 Learning Roadmap Structure

Each career path includes a 3-phase learning journey:

1. **Foundation Phase** (6 weeks)
   - Core skills introduction
   - Basic projects
   - Beginner certifications

2. **Advanced Phase** (10 weeks)
   - Specialized skills
   - Real-world projects
   - Industry certifications

3. **Specialization Phase** (8 weeks)
   - Emerging technologies
   - Advanced projects
   - Specialized certifications

## 🛠️ Customization

### Adding New Career Tracks
```python
career_ai.career_tracks["New Career"] = {
    "core_skills": ["skill1", "skill2", "skill3"],
    "emerging_skills": ["emerging1", "emerging2"],
    "market_demand": 85,
    "future_demand": 90,
    "growth_rate": 25
}
```

### Customizing Skill Normalization
```python
career_ai.skill_normalization["new_skill"] = ["variant1", "variant2", "variant3"]
```

## 📊 Data Sources & Assumptions

The system uses simulated data based on:
- **Job Market Trends**: LinkedIn, Indeed job posting patterns
- **Technology Trends**: GitHub, Stack Overflow developer surveys
- **Industry Reports**: Gartner, Forrester, IDC projections
- **Learning Platform Data**: Coursera, Udemy, edX course popularity

## 🔧 API Integration

The JSON output is designed for easy integration:

```python
# Get structured data for your application
guidance_text, json_data = career_ai.generate_guidance(user_profile)

# Access specific recommendations
top_career = json_data["career_recommendations"][0]
learning_path = json_data["learning_path"][0]
skill_gaps = json_data["skill_gap_analysis"][0]
```

## 📄 PDF Report Generation

The web application includes a comprehensive PDF report generation feature:

### Features of the PDF Report:
- **Professional Layout**: Clean, structured format with proper styling
- **Complete Analysis**: Includes all sections from the web interface
- **User Profile Summary**: Personal information and background
- **Career Recommendations**: Top 3 career matches with detailed scores
- **Skill Gap Analysis**: Current skills vs. skills to develop
- **Learning Roadmap**: Structured learning phases with timelines
- **Resume Enhancement**: Project ideas and resume bullet points
- **Emerging Trends**: Future skills and industry trends

### How to Download:
1. Complete your career analysis on the web interface
2. Navigate to the results page
3. Click the "Download Report (PDF)" button
4. The PDF will be automatically generated and downloaded

### PDF Report Structure:
```
📋 Career Guidance Report
├── Title Page (Name, Date, Time)
├── User Profile Summary (Table format)
├── Top Career Recommendations (3 best matches)
├── Skill Gap Analysis (Have vs. Need)
├── Learning Roadmap (Phases with timelines)
├── Resume Enhancement (Projects & bullets)
└── Emerging Trends & Future Skills
```

## 🎨 Output Files

The system generates multiple output formats:
- `career_guidance.txt` - Human-readable guidance
- `career_guidance.json` - Structured data for applications
- `career_guidance_[name]_[timestamp].pdf` - Professional PDF report

## 🌐 Deployment Options

### Google Cloud Platform (Recommended)
- **Free Tier**: 28 instance hours/day
- **Cost**: $0-15/month depending on usage
- **Features**: Auto-scaling, HTTPS, custom domains
- **Guide**: See `DEPLOYMENT_GUIDE.md` for detailed instructions

### Heroku
- **Free Tier**: Available (with limitations)
- **Cost**: $7/month for basic paid plan
- **Features**: Easy deployment, add-ons ecosystem
- **Setup**: `heroku create && git push heroku main`

### Railway
- **Free Tier**: Available
- **Cost**: $5/month for basic plan
- **Features**: Modern platform, easy CI/CD
- **Setup**: `railway login && railway up`

### Render
- **Free Tier**: Available
- **Cost**: $7/month for basic plan
- **Features**: Automatic deployments from GitHub
- **Setup**: Connect GitHub repository, automatic deployment

## 🤝 Contributing

To enhance the system:

1. **Add Career Tracks**: Extend the career_tracks dictionary
2. **Improve Skill Matching**: Enhance the skill normalization logic
3. **Add Learning Resources**: Expand the learning_resources database
4. **Enhance Predictions**: Improve future skill forecasting algorithms

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For questions or issues:
1. Check the example usage in `career_guide_ai.py`
2. Review the JSON schema in the documentation
3. Test with different user profiles to understand the system

---

**Built with ❤️ for career development and skill advancement** 