from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Review

review_bp = Blueprint("review_bp", __name__)

# --- Create a new review ---
@review_bp.route("/", methods=["POST"])
@jwt_required()
def create_review():
    data = request.get_json() or {}
    identity = get_jwt_identity()
    user_id = identity.get("id")  # Extract user ID safely from dict

    required_fields = ["project_id", "reviewee_id", "rating"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        rating_value = float(data["rating"])
    except ValueError:
        return jsonify({"error": "Rating must be a number"}), 400

    new_review = Review(
        project_id=data["project_id"],
        reviewer_id=user_id,
        reviewee_id=data["reviewee_id"],
        rating=rating_value,
        comment=data.get("comment", "")
    )

    db.session.add(new_review)
    db.session.commit()

    return jsonify({
        "message": "Review added successfully",
        "review": new_review.to_dict()
    }), 201


# --- Get all reviews for a user (freelancer/client) ---
@review_bp.route("/user/<int:user_id>", methods=["GET"])
@jwt_required(optional=True)
def get_reviews_for_user(user_id):
    reviews = Review.query.filter_by(reviewee_id=user_id).all()
    return jsonify([r.to_dict() for r in reviews]), 200


# --- Get all reviews for a project ---
@review_bp.route("/project/<int:project_id>", methods=["GET"])
@jwt_required(optional=True)
def get_reviews_for_project(project_id):
    reviews = Review.query.filter_by(project_id=project_id).all()
    return jsonify([r.to_dict() for r in reviews]), 200


# --- Update review ---
@review_bp.route("/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review(review_id):
    identity = get_jwt_identity()
    user_id = identity.get("id")

    review = Review.query.get_or_404(review_id)
    if review.reviewer_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    if "rating" in data:
        try:
            review.rating = float(data["rating"])
        except ValueError:
            return jsonify({"error": "Invalid rating value"}), 400
    review.comment = data.get("comment", review.comment)

    db.session.commit()

    return jsonify({
        "message": "Review updated successfully",
        "review": review.to_dict()
    }), 200


# --- Delete review ---
@review_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):
    identity = get_jwt_identity()
    user_id = identity.get("id")

    review = Review.query.get_or_404(review_id)
    if review.reviewer_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review deleted successfully"}), 200
