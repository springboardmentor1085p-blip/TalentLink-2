from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from models import db, Project, User, Proposal, Contract
from datetime import datetime

project_bp = Blueprint('project', __name__)

def format_project(project, include_details=False):
    """Helper function to format project data"""
    result = {
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'budget': float(project.budget) if project.budget else None,
        'duration': project.duration,
        'skills_required': project.skills_required,
        'client_id': project.client_id,
        'status': project.status if hasattr(project, 'status') else 'active',
        'created_at': project.created_at.isoformat() if project.created_at else None
    }
    
    if include_details and hasattr(project, 'client'):
        result['client'] = {
            'id': project.client.id,
            'username': project.client.username,
            'email': project.client.email
        }
    
    return result

@project_bp.route('/', methods=['GET'])
@jwt_required()
def list_projects():
    try:
        ident = get_jwt_identity()
        status = request.args.get('status', 'active')
        
        # Base query
        query = Project.query
        
        # Filter by status if provided
        if status.lower() in ['active', 'completed', 'cancelled']:
            query = query.filter(Project.status == status.lower())
        
        # If user is a freelancer, show projects they haven't proposed to
        if ident['role'] == 'freelancer':
            # Get project IDs where user has already submitted a proposal
            proposed_project_ids = db.session.query(Proposal.project_id).filter(
                Proposal.freelancer_id == ident['id']
            ).subquery()
            
            # Filter out projects the freelancer has already proposed to
            query = query.filter(
                Project.id.notin_(proposed_project_ids),
                Project.status == 'active',
                Project.client_id != ident['id']  # Don't show own projects
            )
        # If user is a client, show their projects
        elif ident['role'] == 'client':
            query = query.filter(Project.client_id == ident['id'])
        
        # Execute query and format results
        projects = query.order_by(Project.created_at.desc()).all()
        return jsonify([format_project(p) for p in projects]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@project_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    try:
        ident = get_jwt_identity()
        
        # Only clients can create projects
        if ident['role'] != 'client':
            return jsonify({'error': 'only clients can create projects'}), 403
        
        data = request.get_json() or {}
        
        # Validate required fields
        required_fields = ['title', 'description', 'budget', 'duration']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'error': 'missing required fields',
                'missing': missing_fields
            }), 400
        
        # Create new project
        project = Project(
            client_id=ident['id'],
            title=data['title'].strip(),
            description=data['description'].strip(),
            budget=float(data['budget']),
            duration=data['duration'].strip(),
            skills_required=data.get('skills_required', '').strip(),
            status='active',
            created_at=datetime.utcnow()
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'message': 'project created successfully',
            'project': format_project(project)
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': 'invalid input data'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    try:
        ident = get_jwt_identity()
        
        # Get project with client details
        project = db.session.query(
            Project,
            User.username,
            User.email
        ).join(
            User, User.id == Project.client_id
        ).filter(
            Project.id == project_id
        ).first()
        
        if not project:
            return jsonify({'error': 'project not found'}), 404
            
        project_obj, username, email = project
        
        # Check if user has permission to view this project
        if project_obj.client_id != ident['id'] and ident['role'] != 'admin':
            return jsonify({'error': 'unauthorized access to project'}), 403
        
        # Format response
        response = format_project(project_obj, include_details=True)
        response['client']['username'] = username
        response['client']['email'] = email
        
        # Add proposal count if client is viewing their own project
        if project_obj.client_id == ident['id']:
            response['proposal_count'] = Proposal.query.filter_by(
                project_id=project_id
            ).count()
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
