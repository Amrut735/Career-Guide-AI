from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from models import Roadmap, RoadmapItem
from services.roadmap_service import build_checklist_items
from utils.extensions import db


roadmaps_bp = Blueprint("roadmaps", __name__)


@roadmaps_bp.route("/api/roadmaps", methods=["POST"])
@login_required
def create_roadmap():
    data = request.get_json(silent=True) or {}
    results = data.get("results")
    guidance_text = data.get("guidance_text", "")

    if not results:
        return jsonify({"success": False, "error": "Results payload is required"}), 400

    title = data.get("title") or "Career Roadmap"
    roadmap = Roadmap(
        user_id=current_user.id,
        title=title,
        guidance_text=guidance_text,
        results_json=results,
    )
    db.session.add(roadmap)
    db.session.flush()

    items_payload = build_checklist_items(results)
    items = [
        RoadmapItem(
            roadmap_id=roadmap.id,
            title=item["title"],
            category=item["category"],
            phase=item.get("phase"),
            sort_order=item.get("sort_order", 0),
        )
        for item in items_payload
    ]
    db.session.add_all(items)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "roadmap": {
                "id": roadmap.id,
                "title": roadmap.title,
                "created_at": roadmap.created_at.isoformat(),
            },
            "items": [serialize_item(item) for item in items],
        }
    )


@roadmaps_bp.route("/api/roadmaps", methods=["GET"])
@login_required
def list_roadmaps():
    roadmaps = (
        Roadmap.query.filter_by(user_id=current_user.id)
        .order_by(Roadmap.created_at.desc())
        .all()
    )
    return jsonify(
        {
            "success": True,
            "roadmaps": [
                {
                    "id": roadmap.id,
                    "title": roadmap.title,
                    "created_at": roadmap.created_at.isoformat(),
                }
                for roadmap in roadmaps
            ],
        }
    )


@roadmaps_bp.route("/api/roadmaps/<int:roadmap_id>", methods=["GET"])
@login_required
def get_roadmap(roadmap_id: int):
    roadmap = Roadmap.query.filter_by(id=roadmap_id, user_id=current_user.id).first()
    if not roadmap:
        return jsonify({"success": False, "error": "Roadmap not found"}), 404

    items = (
        RoadmapItem.query.filter_by(roadmap_id=roadmap.id)
        .order_by(RoadmapItem.sort_order.asc())
        .all()
    )

    return jsonify(
        {
            "success": True,
            "roadmap": {
                "id": roadmap.id,
                "title": roadmap.title,
                "guidance_text": roadmap.guidance_text,
                "results": roadmap.results_json,
                "created_at": roadmap.created_at.isoformat(),
            },
            "items": [serialize_item(item) for item in items],
        }
    )


@roadmaps_bp.route("/api/roadmaps/<int:roadmap_id>/items/<int:item_id>", methods=["PATCH"])
@login_required
def update_roadmap_item(roadmap_id: int, item_id: int):
    item = (
        RoadmapItem.query.join(Roadmap)
        .filter(
            RoadmapItem.id == item_id,
            RoadmapItem.roadmap_id == roadmap_id,
            Roadmap.user_id == current_user.id,
        )
        .first()
    )
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404

    data = request.get_json(silent=True) or {}
    if "completed" in data:
        item.completed = bool(data["completed"])

    db.session.commit()
    return jsonify({"success": True, "item": serialize_item(item)})


def serialize_item(item: RoadmapItem):
    return {
        "id": item.id,
        "title": item.title,
        "category": item.category,
        "phase": item.phase,
        "sort_order": item.sort_order,
        "completed": item.completed,
    }
