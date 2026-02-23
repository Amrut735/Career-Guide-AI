from datetime import datetime
from hashlib import sha256
import json
from typing import Dict, List, Tuple

from career_guide_ai import CareerGuideAI
from utils.validation import AnalyzeRequest


career_ai = CareerGuideAI()


def analyze_profile(payload: AnalyzeRequest) -> Tuple[str, Dict, Dict, str]:
    user_input = (
        f"Name: {payload.name}\n"
        f"Education: {payload.education}\n"
        f"Experience: {payload.experience}\n"
        f"Skills: {', '.join(payload.skills)}\n"
        f"Interests: {', '.join(payload.interests)}\n"
        f"Learning Style: {payload.learning_style}\n"
    )

    user_profile = career_ai.parse_user_input(user_input)
    guidance_text, json_output = career_ai.generate_guidance(user_profile)

    user_profile_payload = {
        "name": user_profile.name,
        "education": user_profile.education_level,
        "experience": user_profile.experience_level,
        "skills": user_profile.skills,
        "interests": user_profile.interests,
    }

    timestamp = datetime.now().isoformat()
    return guidance_text, json_output, user_profile_payload, timestamp


def build_cache_key(payload: AnalyzeRequest) -> str:
    normalized = payload.model_dump()
    raw = json.dumps(normalized, sort_keys=True)
    return f"ai:guidance:{sha256(raw.encode()).hexdigest()}"


def get_career_tracks() -> List[Dict]:
    tracks = []
    for track, data in career_ai.career_tracks.items():
        tracks.append(
            {
                "name": track,
                "core_skills": data["core_skills"],
                "emerging_skills": data["emerging_skills"],
                "market_demand": data["market_demand"],
                "future_demand": data["future_demand"],
                "growth_rate": data["growth_rate"],
            }
        )
    return tracks


def get_skills() -> List[str]:
    skills: List[str] = []
    for variants in career_ai.skill_normalization.values():
        skills.extend(variants)
    return list(set(skills))
