from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Project, User

project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['GET'])
def list_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    out = []
    for p in projects:
        out.append({
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'budget': p.budget,
            'duration': p.duration,
            'skills_required': p.skills_required,
            'client_id': p.client_id
        })
    return jsonify(out), 200

@project_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    ident = get_jwt_identity()
    if ident['role'] != 'client':
        return jsonify({'error': 'only clients can create projects'}), 403
    data = request.get_json() or {}
    required = ['title']
    for r in required:
        if not data.get(r):
            return jsonify({'error': f'{r} is required'}), 400
    p = Project(
        client_id=ident['id'],
        title=data.get('title'),
        description=data.get('description'),
        budget=data.get('budget'),
        duration=data.get('duration'),
        skills_required=data.get('skills_required')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({'message': 'project created', 'id': p.id}), 201

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    p = Project.query.get_or_404(project_id)
    return jsonify({
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'budget': p.budget,
        'duration': p.duration,
        'skills_required': p.skills_required,
        'client_id': p.client_id
    }), 200
