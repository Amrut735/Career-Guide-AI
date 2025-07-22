#!/usr/bin/env python3
"""
CareerGuideAI Web Application
A modern, responsive web interface for the career guidance system.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, send_file
import json
import os
from datetime import datetime
from career_guide_ai import CareerGuideAI
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'career_guide_ai_secret_key_2024'

# Initialize CareerGuideAI
career_ai = CareerGuideAI()

@app.route('/')
def index():
    """Main page with career guidance form."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze user profile and return career guidance."""
    try:
        # Get form data
        data = request.get_json()
        
        # Format user input
        user_input = f"""
        Name: {data.get('name', '')}
        Education: {data.get('education', '')}
        Experience: {data.get('experience', '')}
        Skills: {', '.join(data.get('skills', []))}
        Interests: {', '.join(data.get('interests', []))}
        Learning Style: {data.get('learning_style', '')}
        """
        
        # Generate guidance
        user_profile = career_ai.parse_user_input(user_input)
        guidance_text, json_output = career_ai.generate_guidance(user_profile)
        
        # Store in session for later use
        session['guidance_text'] = guidance_text
        session['json_output'] = json_output
        session['user_profile'] = {
            'name': user_profile.name,
            'education': user_profile.education_level,
            'experience': user_profile.experience_level,
            'skills': user_profile.skills,
            'interests': user_profile.interests
        }
        
        return jsonify({
            'success': True,
            'guidance': json_output,
            'user_profile': session['user_profile']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/results')
def results():
    """Display results page."""
    if 'guidance_text' not in session:
        return redirect('/')
    
    return render_template('results.html')

@app.route('/download/<format>')
def download(format):
    """Download results in specified format."""
    if 'guidance_text' not in session or 'json_output' not in session:
        return jsonify({'error': 'No results available'}), 404
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_name = session.get('user_profile', {}).get('name', 'user')
    name_suffix = f"_{user_name.replace(' ', '_')}" if user_name else ""
    
    if format == 'pdf':
        filename = f"career_guidance{name_suffix}_{timestamp}.pdf"
        # Create PDF in memory
        pdf_buffer = io.BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
        textobject = pdf.beginText(40, 750)
        for line in session['guidance_text'].split('\n'):
            textobject.textLine(line)
        pdf.drawText(textobject)
        pdf.save()
        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    else:
        return jsonify({'error': 'Invalid format'}), 400

@app.route('/api/career-tracks')
def get_career_tracks():
    """API endpoint to get available career tracks."""
    tracks = []
    for track, data in career_ai.career_tracks.items():
        tracks.append({
            'name': track,
            'core_skills': data['core_skills'],
            'emerging_skills': data['emerging_skills'],
            'market_demand': data['market_demand'],
            'future_demand': data['future_demand'],
            'growth_rate': data['growth_rate']
        })
    
    return jsonify(tracks)

@app.route('/api/skills')
def get_skills():
    """API endpoint to get available skills for autocomplete."""
    skills = []
    for skill, variants in career_ai.skill_normalization.items():
        skills.extend(variants)
    
    return jsonify(list(set(skills)))

@app.route('/api/results')
def get_results():
    """API endpoint to get analysis results from session."""
    if 'json_output' not in session:
        return jsonify({
            'success': False,
            'error': 'No results available'
        }), 404
    
    return jsonify({
        'success': True,
        'results': session['json_output']
    })

if __name__ == '__main__':
    print("🚀 CareerGuideAI Web Application Starting...")
    print("📱 Available at: http://127.0.0.1:5000")
    print("🌐 Also try: http://localhost:5000")
    print("🌐 Network access: http://10.58.30.179:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 