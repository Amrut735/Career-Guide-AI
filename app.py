#!/usr/bin/env python3
"""
CareerGuideAI Web Application
A modern, responsive web interface for the career guidance system.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, send_file, url_for
import json
import os
from datetime import datetime
from career_guide_ai import CareerGuideAI
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

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
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        name = data.get('name', '').strip()
        if not name:
            return jsonify({
                'success': False,
                'error': 'Name is required'
            }), 400
        
        skills = data.get('skills', [])
        if not skills:
            return jsonify({
                'success': False,
                'error': 'At least one skill is required'
            }), 400
        
        # Format user input
        user_input = f"""
        Name: {name}
        Education: {data.get('education', '')}
        Experience: {data.get('experience', '')}
        Skills: {', '.join(skills)}
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
        
        # Store analysis timestamp
        session['analysis_timestamp'] = datetime.now().isoformat()
        
        print(f"DEBUG: Stored in session - guidance_text: {len(guidance_text) if guidance_text else 0} chars")
        print(f"DEBUG: Session keys after storing: {list(session.keys())}")
        
        return jsonify({
            'success': True,
            'guidance': json_output,
            'user_profile': session['user_profile'],
            'timestamp': session['analysis_timestamp']
        })
        
    except Exception as e:
        print(f"ERROR in analyze: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/results')
def results():
    """Display results page."""
    print(f"DEBUG: Session keys: {list(session.keys())}")
    print(f"DEBUG: guidance_text in session: {'guidance_text' in session}")
    print(f"DEBUG: json_output in session: {'json_output' in session}")
    
    if 'guidance_text' not in session or 'json_output' not in session:
        print("DEBUG: No analysis data in session, redirecting to home")
        # Redirect to home page if no analysis data exists
        return redirect(url_for('index'))
    
    print("DEBUG: Rendering results page")
    return render_template('results.html', no_data=False)

@app.route('/download/<format>')
def download(format):
    """Download results in specified format."""
    if 'guidance_text' not in session or 'json_output' not in session:
        return jsonify({'error': 'No results available'}), 404
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_name = session.get('user_profile', {}).get('name', 'user')
    safe_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')
    
    if format.lower() == 'pdf':
        filename = f"career_guidance_{safe_name}_{timestamp}.pdf"
        return generate_pdf_report(filename)
    elif format.lower() == 'json':
        filename = f"career_guidance_{safe_name}_{timestamp}.json"
        return send_file(
            io.BytesIO(json.dumps(session['json_output'], indent=2).encode()),
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
    else:
        return jsonify({'error': 'Unsupported format'}), 400

def generate_pdf_report(filename):
    """Generate a comprehensive PDF career guidance report."""
    # Create PDF buffer
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.darkgreen
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    # Build the story (content)
    story = []
    
    # Title page
    story.append(Paragraph("Career Guidance Report", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Generated for: {session.get('user_profile', {}).get('name', 'User')}", heading_style))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    story.append(Paragraph(f"Time: {datetime.now().strftime('%I:%M %p')}", normal_style))
    story.append(PageBreak())
    
    # User Profile Summary
    story.append(Paragraph("User Profile Summary", heading_style))
    user_profile = session.get('user_profile', {})
    
    profile_data = [
        ['Field', 'Value'],
        ['Name', user_profile.get('name', 'Not specified')],
        ['Education Level', user_profile.get('education', 'Not specified')],
        ['Experience Level', user_profile.get('experience', 'Not specified')],
        ['Skills Count', str(len(user_profile.get('skills', [])))],
        ['Interests Count', str(len(user_profile.get('interests', [])))]
    ]
    
    profile_table = Table(profile_data, colWidths=[2*inch, 4*inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 20))
    
    # Career Recommendations
    json_output = session.get('json_output', {})
    if 'career_recommendations' in json_output:
        story.append(Paragraph("Top Career Recommendations", heading_style))
        
        for i, rec in enumerate(json_output['career_recommendations'][:3], 1):
            story.append(Paragraph(f"{i}. {rec.get('career_track', 'Career Track')}", subheading_style))
            story.append(Paragraph(f"Match Score: {rec.get('match_score', 0)}/100", normal_style))
            story.append(Paragraph(f"Market Demand: {rec.get('current_market_demand_score', 0)}/100", normal_style))
            story.append(Paragraph(f"Future Demand: {rec.get('future_demand_projection_score', 0)}/100", normal_style))
            story.append(Paragraph(f"Recommendation: {rec.get('why_recommended', 'No reason provided')}", normal_style))
            
            # Top recommended skills
            if 'top_recommended_skills' in rec:
                skills_text = ", ".join(rec['top_recommended_skills'][:5])
                story.append(Paragraph(f"Key Skills: {skills_text}", normal_style))
            
            story.append(Spacer(1, 12))
    
    story.append(PageBreak())
    
    # Skill Gap Analysis
    if 'skill_gap_analysis' in json_output and json_output['skill_gap_analysis']:
        story.append(Paragraph("Skill Gap Analysis", heading_style))
        gap = json_output['skill_gap_analysis'][0]
        
        # Skills you have
        story.append(Paragraph("Skills You Currently Have", subheading_style))
        if 'have_skills' in gap and gap['have_skills']:
            have_skills_text = ", ".join(gap['have_skills'][:10])  # Limit to first 10
            story.append(Paragraph(have_skills_text, normal_style))
        else:
            story.append(Paragraph("No skills identified", normal_style))
        
        story.append(Spacer(1, 12))
        
        # Skills to learn
        story.append(Paragraph("Skills to Develop", subheading_style))
        if 'need_skills' in gap and gap['need_skills']:
            need_skills_text = ", ".join(gap['need_skills'][:10])  # Limit to first 10
            story.append(Paragraph(need_skills_text, normal_style))
        else:
            story.append(Paragraph("No additional skills identified", normal_style))
        
        story.append(Spacer(1, 20))
    
    # Learning Roadmap
    if 'learning_path' in json_output and json_output['learning_path']:
        story.append(Paragraph("Learning Roadmap", heading_style))
        roadmap = json_output['learning_path'][0]
        
        story.append(Paragraph(f"Timeline: {roadmap.get('timeline_months', 'N/A')} months", subheading_style))
        
        if 'phases' in roadmap:
            for i, phase in enumerate(roadmap['phases'][:3], 1):  # Limit to first 3 phases
                story.append(Paragraph(f"Phase {i}: {phase.get('phase_name', 'Phase')} ({phase.get('duration_weeks', 0)} weeks)", subheading_style))
                
                # Focus skills
                if 'focus_skills' in phase and phase['focus_skills']:
                    focus_skills_text = ", ".join(phase['focus_skills'][:5])
                    story.append(Paragraph(f"Focus Skills: {focus_skills_text}", normal_style))
                
                # Projects
                if 'recommended_projects' in phase and phase['recommended_projects']:
                    story.append(Paragraph("Recommended Projects:", normal_style))
                    for project in phase['recommended_projects'][:3]:  # Limit to first 3
                        story.append(Paragraph(f"• {project}", normal_style))
                
                story.append(Spacer(1, 8))
    
    story.append(PageBreak())
    
    # Resume Boosters
    if 'resume_boosters' in json_output and json_output['resume_boosters']:
        story.append(Paragraph("Resume Enhancement", heading_style))
        booster = json_output['resume_boosters'][0]
        
        # Project Ideas
        story.append(Paragraph("Project Ideas", subheading_style))
        if 'project_ideas' in booster and booster['project_ideas']:
            for project in booster['project_ideas'][:5]:  # Limit to first 5
                story.append(Paragraph(f"• {project}", normal_style))
        else:
            story.append(Paragraph("No project ideas available", normal_style))
        
        story.append(Spacer(1, 12))
        
        # Resume Bullets
        story.append(Paragraph("Resume Bullet Points", subheading_style))
        if 'resume_bullets_sample' in booster and booster['resume_bullets_sample']:
            for bullet in booster['resume_bullets_sample'][:5]:  # Limit to first 5
                story.append(Paragraph(f"• {bullet}", normal_style))
        else:
            story.append(Paragraph("No resume bullets available", normal_style))
        
        story.append(Spacer(1, 20))
    
    # Emerging Trends
    if 'career_recommendations' in json_output and json_output['career_recommendations']:
        story.append(Paragraph("Emerging Trends & Future Skills", heading_style))
        rec = json_output['career_recommendations'][0]
        
        if 'emerging_skills' in rec and rec['emerging_skills']:
            trends_text = ", ".join(rec['emerging_skills'][:8])  # Limit to first 8
            story.append(Paragraph(f"Emerging Skills: {trends_text}", normal_style))
        else:
            story.append(Paragraph("No emerging trends identified", normal_style))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("Generated by CareerGuideAI", normal_style))
    story.append(Paragraph("For personalized career guidance and development", normal_style))
    
    # Build PDF
    doc.build(story)
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

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
        'results': session['json_output'],
        'user_profile': session.get('user_profile', {}),
        'timestamp': session.get('analysis_timestamp', '')
    })

@app.route('/api/analysis-history')
def get_analysis_history():
    """API endpoint to get analysis history."""
    # For now, return current session data
    # In a real app, this would query a database
    if 'json_output' not in session:
        return jsonify({'history': []})
    
    return jsonify({
        'history': [{
            'timestamp': session.get('analysis_timestamp', ''),
            'user_profile': session.get('user_profile', {}),
            'career_recommendations': len(session['json_output'].get('career_recommendations', [])),
            'top_career': session['json_output'].get('career_recommendations', [{}])[0].get('career_track', '') if session['json_output'].get('career_recommendations') else ''
        }]
    })

@app.route('/api/career-stats')
def get_career_stats():
    """API endpoint to get career statistics."""
    if 'json_output' not in session:
        return jsonify({'error': 'No analysis data available'}), 404
    
    recommendations = session['json_output'].get('career_recommendations', [])
    if not recommendations:
        return jsonify({'error': 'No career recommendations available'}), 404
    
    # Calculate statistics
    avg_match_score = sum(r.get('match_score', 0) for r in recommendations) / len(recommendations)
    avg_market_demand = sum(r.get('current_market_demand_score', 0) for r in recommendations) / len(recommendations)
    avg_future_demand = sum(r.get('future_demand_projection_score', 0) for r in recommendations) / len(recommendations)
    
    return jsonify({
        'total_recommendations': len(recommendations),
        'average_match_score': round(avg_match_score, 1),
        'average_market_demand': round(avg_market_demand, 1),
        'average_future_demand': round(avg_future_demand, 1),
        'top_career': recommendations[0].get('career_track', ''),
        'top_match_score': recommendations[0].get('match_score', 0)
    })

@app.route('/sitemap.xml')
def sitemap():
    """Serve sitemap.xml for SEO."""
    return send_file('static/sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Serve robots.txt for SEO."""
    robots_content = """User-agent: *
Allow: /
Sitemap: https://career-guide-ai.onrender.com/sitemap.xml"""
    return app.response_class(robots_content, mimetype='text/plain')

@app.route('/debug')
def debug():
    """Debug page for troubleshooting."""
    return render_template('debug.html')

@app.route('/api/debug/session')
def debug_session():
    """API endpoint to get session debug information."""
    return jsonify({
        'session_keys': list(session.keys()),
        'has_guidance': 'guidance_text' in session,
        'has_json': 'json_output' in session
    })

@app.route('/api/progress')
def get_progress():
    """API endpoint to get user progress information."""
    if 'json_output' not in session:
        return jsonify({'error': 'No analysis data available'}), 404
    
    recommendations = session['json_output'].get('career_recommendations', [])
    skill_gaps = session['json_output'].get('skill_gap_analysis', [])
    learning_paths = session['json_output'].get('learning_path', [])
    
    # Calculate progress metrics
    total_skills_needed = sum(len(gap.get('need_skills', [])) for gap in skill_gaps)
    total_learning_phases = sum(len(path.get('phases', [])) for path in learning_paths)
    
    progress_data = {
        'analysis_completed': True,
        'analysis_date': session.get('analysis_timestamp', ''),
        'career_recommendations_count': len(recommendations),
        'skill_gaps_count': len(skill_gaps),
        'learning_paths_count': len(learning_paths),
        'total_skills_to_learn': total_skills_needed,
        'total_learning_phases': total_learning_phases,
        'top_career_match': recommendations[0].get('career_track', '') if recommendations else '',
        'match_score': recommendations[0].get('match_score', 0) if recommendations else 0
    }
    
    return jsonify(progress_data)

if __name__ == '__main__':
    print("🚀 CareerGuideAI Web Application Starting...")
    print("📱 Available at: http://127.0.0.1:5001")
    print("🌐 Also try: http://localhost:5001")
    print("🌐 Network access: http://10.58.30.179:5001")
    app.run(debug=True, host='0.0.0.0', port=5001) 