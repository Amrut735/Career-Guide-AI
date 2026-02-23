from typing import Dict, List


def build_checklist_items(results: Dict) -> List[Dict]:
    items: List[Dict] = []
    order = 0

    for gap in results.get("skill_gap_analysis", []):
        for skill in gap.get("need_skills", []):
            items.append(
                {
                    "title": f"Learn skill: {skill}",
                    "category": "skill_gap",
                    "phase": None,
                    "sort_order": order,
                }
            )
            order += 1

    for roadmap in results.get("learning_path", []):
        for phase in roadmap.get("phases", []):
            phase_name = phase.get("phase_name", "Phase")
            for skill in phase.get("focus_skills", []):
                items.append(
                    {
                        "title": f"[{phase_name}] Focus skill: {skill}",
                        "category": "learning",
                        "phase": phase_name,
                        "sort_order": order,
                    }
                )
                order += 1
            for project in phase.get("recommended_projects", []):
                items.append(
                    {
                        "title": f"[{phase_name}] Build project: {project}",
                        "category": "project",
                        "phase": phase_name,
                        "sort_order": order,
                    }
                )
                order += 1
            for cert in phase.get("recommended_certifications", []):
                items.append(
                    {
                        "title": f"[{phase_name}] Earn certification: {cert}",
                        "category": "certification",
                        "phase": phase_name,
                        "sort_order": order,
                    }
                )
                order += 1

    for booster in results.get("resume_boosters", []):
        for project in booster.get("project_ideas", []):
            items.append(
                {
                    "title": f"Resume project: {project}",
                    "category": "resume",
                    "phase": None,
                    "sort_order": order,
                }
            )
            order += 1

    return items
