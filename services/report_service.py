import io
from datetime import datetime
from typing import Dict

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def create_pdf_report(user_profile: Dict, json_output: Dict) -> io.BytesIO:
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue,
    )
    subheading_style = ParagraphStyle(
        "CustomSubheading",
        parent=styles["Heading3"],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.darkgreen,
    )
    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=6,
    )

    story = []
    story.append(Paragraph("Career Guidance Report", title_style))
    story.append(Spacer(1, 20))
    story.append(
        Paragraph(f"Generated for: {user_profile.get('name', 'User')}", heading_style)
    )
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", normal_style))
    story.append(Paragraph(f"Time: {datetime.now().strftime('%I:%M %p')}", normal_style))
    story.append(PageBreak())

    story.append(Paragraph("User Profile Summary", heading_style))
    profile_data = [
        ["Field", "Value"],
        ["Name", user_profile.get("name", "Not specified")],
        ["Education Level", user_profile.get("education", "Not specified")],
        ["Experience Level", user_profile.get("experience", "Not specified")],
        ["Skills Count", str(len(user_profile.get("skills", [])))],
        ["Interests Count", str(len(user_profile.get("interests", [])))],
    ]

    profile_table = Table(profile_data, colWidths=[2 * inch, 4 * inch])
    profile_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    story.append(profile_table)
    story.append(Spacer(1, 20))

    if "career_recommendations" in json_output:
        story.append(Paragraph("Top Career Recommendations", heading_style))
        for i, rec in enumerate(json_output["career_recommendations"][:3], 1):
            story.append(
                Paragraph(f"{i}. {rec.get('career_track', 'Career Track')}", subheading_style)
            )
            story.append(
                Paragraph(f"Match Score: {rec.get('match_score', 0)}/100", normal_style)
            )
            story.append(
                Paragraph(
                    f"Market Demand: {rec.get('current_market_demand_score', 0)}/100",
                    normal_style,
                )
            )
            story.append(
                Paragraph(
                    f"Future Demand: {rec.get('future_demand_projection_score', 0)}/100",
                    normal_style,
                )
            )
            story.append(
                Paragraph(
                    f"Recommendation: {rec.get('why_recommended', 'No reason provided')}",
                    normal_style,
                )
            )
            if "top_recommended_skills" in rec:
                skills_text = ", ".join(rec["top_recommended_skills"][:5])
                story.append(Paragraph(f"Key Skills: {skills_text}", normal_style))
            story.append(Spacer(1, 12))

    story.append(PageBreak())

    if json_output.get("skill_gap_analysis"):
        story.append(Paragraph("Skill Gap Analysis", heading_style))
        gap = json_output["skill_gap_analysis"][0]
        story.append(Paragraph("Skills You Currently Have", subheading_style))
        have_skills_text = ", ".join(gap.get("have_skills", [])[:10])
        story.append(Paragraph(have_skills_text or "No skills identified", normal_style))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Skills to Develop", subheading_style))
        need_skills_text = ", ".join(gap.get("need_skills", [])[:10])
        story.append(Paragraph(need_skills_text or "No additional skills identified", normal_style))
        story.append(Spacer(1, 20))

    if json_output.get("learning_path"):
        story.append(Paragraph("Learning Roadmap", heading_style))
        roadmap = json_output["learning_path"][0]
        story.append(
            Paragraph(f"Timeline: {roadmap.get('timeline_months', 'N/A')} months", subheading_style)
        )
        for i, phase in enumerate(roadmap.get("phases", [])[:3], 1):
            story.append(
                Paragraph(
                    f"Phase {i}: {phase.get('phase_name', 'Phase')} ({phase.get('duration_weeks', 0)} weeks)",
                    subheading_style,
                )
            )
            focus_skills_text = ", ".join(phase.get("focus_skills", [])[:5])
            if focus_skills_text:
                story.append(Paragraph(f"Focus Skills: {focus_skills_text}", normal_style))
            if phase.get("recommended_projects"):
                story.append(Paragraph("Recommended Projects:", normal_style))
                for project in phase["recommended_projects"][:3]:
                    story.append(Paragraph(f"• {project}", normal_style))
            story.append(Spacer(1, 8))

    story.append(PageBreak())

    if json_output.get("resume_boosters"):
        story.append(Paragraph("Resume Enhancement", heading_style))
        booster = json_output["resume_boosters"][0]
        story.append(Paragraph("Project Ideas", subheading_style))
        for project in booster.get("project_ideas", [])[:5]:
            story.append(Paragraph(f"• {project}", normal_style))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Resume Bullet Points", subheading_style))
        for bullet in booster.get("resume_bullets_sample", [])[:5]:
            story.append(Paragraph(f"• {bullet}", normal_style))
        story.append(Spacer(1, 20))

    if json_output.get("career_recommendations"):
        story.append(Paragraph("Emerging Trends & Future Skills", heading_style))
        rec = json_output["career_recommendations"][0]
        trends_text = ", ".join(rec.get("emerging_skills", [])[:8])
        story.append(Paragraph(f"Emerging Skills: {trends_text or 'None identified'}", normal_style))

    story.append(Spacer(1, 30))
    story.append(Paragraph("Generated by CareerGuideAI", normal_style))
    story.append(Paragraph("For personalized career guidance and development", normal_style))

    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer
