# CareerGuideAI API Documentation

This document provides comprehensive documentation for all API endpoints in the CareerGuideAI application.

## 🌐 Base URL
- **Development**: `http://localhost:5001`
- **Production**: `https://career-guide-ai-2.onrender.com`

## 📋 Authentication
Currently, the API uses session-based authentication. All endpoints require an active session with analysis data.

## 🔗 Endpoints

### 1. Career Analysis

#### POST `/analyze`
Submit career analysis data and receive personalized recommendations.

**Request Body:**
```json
{
  "name": "John Doe",
  "education": "Bachelor",
  "experience": "junior",
  "skills": ["python", "javascript", "sql"],
  "interests": ["web development", "ai", "data science"],
  "learning_style": "visual"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Analysis completed successfully",
  "timestamp": "2025-08-01T21:42:11.442677"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Name is required"
}
```

**Status Codes:**
- `200`: Analysis completed successfully
- `400`: Bad request (missing required fields)
- `500`: Internal server error

---

### 2. Results Retrieval

#### GET `/api/results`
Retrieve the latest analysis results.

**Response:**
```json
{
  "success": true,
  "results": {
    "career_recommendations": [...],
    "skill_gaps": [...],
    "learning_paths": [...],
    "market_analysis": {...}
  },
  "user_profile": {
    "name": "John Doe",
    "education": "Bachelor",
    "experience": "junior",
    "skills": ["python", "javascript"],
    "interests": ["web development", "ai"],
    "learning_style": "visual"
  },
  "timestamp": "2025-08-01T21:42:11.442677"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "No analysis results found in session"
}
```

**Status Codes:**
- `200`: Results retrieved successfully
- `404`: No analysis results found

---

### 3. Career Statistics

#### GET `/api/career-stats`
Get aggregated statistics from the latest analysis.

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_recommendations": 5,
    "average_match_score": 14.0,
    "average_demand_score": 85.0,
    "top_career_match": "Data Scientist",
    "total_skills_analyzed": 3,
    "skill_gaps_identified": 1
  }
}
```

**Status Codes:**
- `200`: Statistics retrieved successfully
- `404`: No analysis data available

---

### 4. Analysis History

#### GET `/api/analysis-history`
Retrieve analysis history (currently returns the latest analysis).

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "timestamp": "2025-08-01T21:42:11.442677",
      "user_name": "John Doe",
      "career_count": 5,
      "top_match": "Data Scientist"
    }
  ]
}
```

**Status Codes:**
- `200`: History retrieved successfully
- `404`: No analysis history available

---

### 5. Progress Tracking

#### GET `/api/progress`
Get user progress information and learning recommendations.

**Response:**
```json
{
  "success": true,
  "progress": {
    "analysis_completed": true,
    "analysis_date": "2025-08-01T21:42:11.442677",
    "career_recommendations_count": 5,
    "learning_paths_count": 1,
    "match_score": 38,
    "skill_gaps_count": 1,
    "top_career_match": "Data Scientist",
    "total_learning_phases": 3,
    "total_skills_to_learn": 3
  }
}
```

**Status Codes:**
- `200`: Progress data retrieved successfully
- `404`: No progress data available

---

### 6. File Downloads

#### GET `/download/<format>`
Download analysis results in various formats.

**Parameters:**
- `format`: `pdf` or `json`

**Response:**
- `200`: File download (PDF or JSON)
- `404`: No analysis data available

**Example:**
```
GET /download/pdf
GET /download/json
```

---

### 7. Debug Information

#### GET `/api/debug/session`
Get current session information for debugging.

**Response:**
```json
{
  "success": true,
  "session_keys": ["guidance_text", "json_output", "user_profile", "analysis_timestamp"],
  "has_analysis_data": true,
  "timestamp": "2025-08-01T21:42:11.442677"
}
```

**Status Codes:**
- `200`: Session information retrieved successfully

---

## 📊 Data Models

### User Profile
```json
{
  "name": "string",
  "education": "string",
  "experience": "string",
  "skills": ["string"],
  "interests": ["string"],
  "learning_style": "string",
  "domain": "string (optional)"
}
```

### Career Recommendation
```json
{
  "career": "string",
  "match_score": "number",
  "demand_score": "number",
  "description": "string",
  "required_skills": ["string"],
  "salary_range": "string",
  "growth_potential": "string"
}
```

### Skill Gap
```json
{
  "skill": "string",
  "importance": "number",
  "difficulty": "string",
  "learning_resources": ["string"],
  "estimated_time": "string"
}
```

### Learning Path
```json
{
  "phase": "string",
  "duration": "string",
  "skills": ["string"],
  "resources": ["string"],
  "milestones": ["string"]
}
```

---

## 🔧 Error Handling

### Standard Error Response
```json
{
  "success": false,
  "error": "Error message description",
  "details": "Additional error details (optional)"
}
```

### Common Error Codes
- `400`: Bad Request - Invalid input data
- `404`: Not Found - Resource not available
- `500`: Internal Server Error - Server-side error

---

## 🧪 Testing

### Test Scripts
The application includes several test scripts for API validation:

```bash
# Test complete flow
python test_complete_flow.py

# Test browser issues
python test_browser_issues.py

# Test form submission
python test_form_step_by_step.py

# Test enhanced features
python test_enhanced_features.py
```

### Example API Test
```python
import requests

# Submit analysis
response = requests.post('http://localhost:5001/analyze', json={
    'name': 'Test User',
    'education': 'Bachelor',
    'experience': 'junior',
    'skills': ['python'],
    'interests': ['ai']
})

# Get results
results = requests.get('http://localhost:5001/api/results')
print(results.json())
```

---

## 📈 Rate Limiting
Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## 🔒 Security Considerations
- Session-based authentication
- Input validation on all endpoints
- CORS headers for web access
- Sanitized user inputs

---

## 📞 Support
For API support or questions:
1. Check the test scripts for examples
2. Review the application logs
3. Create an issue on GitHub
4. Check the debug endpoint for session information 