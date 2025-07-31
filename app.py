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
    
    if format.lower() == 'pdf':
        filename = f"career_guidance{name_suffix}_{timestamp}.pdf"
        return generate_pdf_report(filename)
    else:
        return jsonify({'error': 'Invalid format'}), 400

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
        'results': session['json_output']
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

if __name__ == '__main__':
    print("🚀 CareerGuideAI Web Application Starting...")
    print("📱 Available at: http://127.0.0.1:5000")
    print("🌐 Also try: http://localhost:5000")
    print("🌐 Network access: http://10.58.30.179:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 