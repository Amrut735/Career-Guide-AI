from flask import Blueprint, jsonify, request, session

from services.career_service import analyze_profile, build_cache_key, get_career_tracks, get_skills
from tasks import celery, generate_guidance_task
from utils.extensions import cache, limiter
from utils.validation import AnalyzeRequest, ValidationError


api_bp = Blueprint("api", __name__)


@api_bp.route("/analyze", methods=["POST"])
@limiter.limit("10 per minute")
def analyze():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"success": False, "error": "No data provided"}), 400

    try:
        payload = AnalyzeRequest.model_validate(data)
    except ValidationError as exc:
        return (
            jsonify({"success": False, "error": "Validation failed", "details": exc.errors()}),
            422,
        )

    cache_key = build_cache_key(payload)
    cached = cache.get(cache_key)
    if cached:
        guidance_text = cached["guidance_text"]
        json_output = cached["json_output"]
        user_profile = cached["user_profile"]
        timestamp = cached["timestamp"]
    else:
        guidance_text, json_output, user_profile, timestamp = analyze_profile(payload)
        cache.set(
            cache_key,
            {
                "guidance_text": guidance_text,
                "json_output": json_output,
                "user_profile": user_profile,
                "timestamp": timestamp,
            },
            timeout=3600,
        )

    session["guidance_text"] = guidance_text
    session["json_output"] = json_output
    session["user_profile"] = user_profile
    session["analysis_timestamp"] = timestamp

    return jsonify(
        {
            "success": True,
            "guidance": json_output,
            "user_profile": user_profile,
            "timestamp": timestamp,
            "cached": bool(cached),
        }
    )


@api_bp.route("/api/analyze/async", methods=["POST"])
@limiter.limit("10 per minute")
def analyze_async():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"success": False, "error": "No data provided"}), 400

    try:
        payload = AnalyzeRequest.model_validate(data)
    except ValidationError as exc:
        return (
            jsonify({"success": False, "error": "Validation failed", "details": exc.errors()}),
            422,
        )

    task = generate_guidance_task.delay(payload.model_dump())
    return jsonify({"success": True, "task_id": task.id}), 202


@api_bp.route("/api/tasks/<task_id>", methods=["GET"])
def get_task_status(task_id: str):
    task = celery.AsyncResult(task_id)
    if task.state == "PENDING":
        return jsonify({"state": task.state, "status": "Queued"}), 202
    if task.state == "FAILURE":
        return jsonify({"state": task.state, "status": str(task.info)}), 500

    if not task.ready():
        return jsonify({"state": task.state, "status": "Processing"}), 202

    result = task.get()
    session["guidance_text"] = result["guidance_text"]
    session["json_output"] = result["json_output"]
    session["user_profile"] = result["user_profile"]
    session["analysis_timestamp"] = result["timestamp"]

    return jsonify({"state": task.state, "result": result}), 200


@api_bp.route("/api/career-tracks")
def get_career_tracks_route():
    return jsonify(get_career_tracks())


@api_bp.route("/api/skills")
def get_skills_route():
    return jsonify(get_skills())


@api_bp.route("/api/results")
def get_results():
    if "json_output" not in session:
        return jsonify({"success": False, "error": "No results available"}), 404

    return jsonify(
        {
            "success": True,
            "results": session["json_output"],
            "user_profile": session.get("user_profile", {}),
            "guidance_text": session.get("guidance_text", ""),
            "timestamp": session.get("analysis_timestamp", ""),
        }
    )


@api_bp.route("/api/analysis-history")
def get_analysis_history():
    if "json_output" not in session:
        return jsonify({"history": []})

    return jsonify(
        {
            "history": [
                {
                    "timestamp": session.get("analysis_timestamp", ""),
                    "user_profile": session.get("user_profile", {}),
                    "career_recommendations": len(
                        session["json_output"].get("career_recommendations", [])
                    ),
                    "top_career": session["json_output"]
                    .get("career_recommendations", [{}])[0]
                    .get("career_track", "")
                    if session["json_output"].get("career_recommendations")
                    else "",
                }
            ]
        }
    )


@api_bp.route("/api/career-stats")
def get_career_stats():
    if "json_output" not in session:
        return jsonify({"error": "No analysis data available"}), 404

    recommendations = session["json_output"].get("career_recommendations", [])
    if not recommendations:
        return jsonify({"error": "No career recommendations available"}), 404

    avg_match_score = sum(r.get("match_score", 0) for r in recommendations) / len(recommendations)
    avg_market_demand = sum(
        r.get("current_market_demand_score", 0) for r in recommendations
    ) / len(recommendations)
    avg_future_demand = sum(
        r.get("future_demand_projection_score", 0) for r in recommendations
    ) / len(recommendations)

    return jsonify(
        {
            "total_recommendations": len(recommendations),
            "average_match_score": round(avg_match_score, 1),
            "average_market_demand": round(avg_market_demand, 1),
            "average_future_demand": round(avg_future_demand, 1),
            "top_career": recommendations[0].get("career_track", ""),
            "top_match_score": recommendations[0].get("match_score", 0),
        }
    )


@api_bp.route("/api/debug/session")
def debug_session():
    return jsonify(
        {
            "session_keys": list(session.keys()),
            "has_guidance": "guidance_text" in session,
            "has_json": "json_output" in session,
        }
    )


@api_bp.route("/api/progress")
def get_progress():
    if "json_output" not in session:
        return jsonify({"error": "No analysis data available"}), 404

    recommendations = session["json_output"].get("career_recommendations", [])
    skill_gaps = session["json_output"].get("skill_gap_analysis", [])
    learning_paths = session["json_output"].get("learning_path", [])

    total_skills_needed = sum(len(gap.get("need_skills", [])) for gap in skill_gaps)
    total_learning_phases = sum(len(path.get("phases", [])) for path in learning_paths)

    progress_data = {
        "analysis_completed": True,
        "analysis_date": session.get("analysis_timestamp", ""),
        "career_recommendations_count": len(recommendations),
        "skill_gaps_count": len(skill_gaps),
        "learning_paths_count": len(learning_paths),
        "total_skills_to_learn": total_skills_needed,
        "total_learning_phases": total_learning_phases,
        "top_career_match": recommendations[0].get("career_track", "") if recommendations else "",
        "match_score": recommendations[0].get("match_score", 0) if recommendations else 0,
    }

    return jsonify(progress_data)
