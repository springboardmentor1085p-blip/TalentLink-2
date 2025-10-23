from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Profile, User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    p = Profile.query.filter_by(user_id=user_id).first()
    if not p:
        return jsonify({}), 200
    return jsonify({
        'user_id': p.user_id,
        'full_name': p.full_name,
        'bio': p.bio,
        'skills': p.skills,
        'hourly_rate': p.hourly_rate,
        'availability': p.availability,
        'location': p.location
    }), 200

@profile_bp.route('/', methods=['POST'])
@jwt_required()
def create_or_update_profile():
    ident = get_jwt_identity()
    data = request.get_json() or {}
    p = Profile.query.filter_by(user_id=ident['id']).first()
    if not p:
        p = Profile(user_id=ident['id'])
        db.session.add(p)
    p.full_name = data.get('full_name')
    p.bio = data.get('bio')
    p.skills = data.get('skills')
    p.hourly_rate = data.get('hourly_rate')
    p.availability = data.get('availability')
    p.location = data.get('location')
    db.session.commit()
    return jsonify({'message': 'profile saved'}), 200
