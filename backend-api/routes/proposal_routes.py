from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db, Proposal, Project, User
from datetime import datetime
from sqlalchemy.orm import joinedload

proposal_bp = Blueprint('proposal', __name__)

@proposal_bp.route('/<int:project_id>', methods=['POST'])
@jwt_required()
def submit_proposal(project_id):
    try:
        ident = get_jwt_identity()
        if ident['role'] != 'freelancer':
            return jsonify({'error': 'only freelancers can submit proposals'}), 403
            
        data = request.get_json() or {}
        
        # Validate required fields
        if not data.get('cover_letter'):
            return jsonify({'error': 'cover_letter is required'}), 400
        if not data.get('proposed_rate'):
            return jsonify({'error': 'proposed_rate is required'}), 400
            
        # Check if project exists and is not created by the same user
        project = Project.query.get_or_404(project_id)
        if project.client_id == ident['id']:
            return jsonify({'error': 'cannot submit proposal to your own project'}), 400
            
        # Check if user already submitted a proposal for this project
        existing_proposal = Proposal.query.filter_by(
            project_id=project_id, 
            freelancer_id=ident['id']
        ).first()
        
        if existing_proposal:
            return jsonify({'error': 'you have already submitted a proposal for this project'}), 400
            
        # Create new proposal
        prop = Proposal(
            project_id=project_id,
            freelancer_id=ident['id'],
            cover_letter=data['cover_letter'],
            proposed_rate=float(data['proposed_rate']),
            status='pending',
            created_at=datetime.utcnow()
        )
        
        db.session.add(prop)
        db.session.commit()
        
        return jsonify({
            'message': 'proposal submitted',
            'id': prop.id,
            'status': prop.status,
            'created_at': prop.created_at.isoformat()
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': 'invalid input data'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@proposal_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def list_proposals_for_project(project_id):
    try:
        ident = get_jwt_identity()
        
        # Check if project exists and user is the owner
        project = Project.query.get_or_404(project_id)
        if project.client_id != ident['id']:
            return jsonify({'error': 'unauthorized access to project proposals'}), 403
            
        # Get all proposals with freelancer details
        proposals = db.session.query(
            Proposal,
            User.username,
            User.email
        ).join(
            User, User.id == Proposal.freelancer_id
        ).filter(
            Proposal.project_id == project_id
        ).all()
        
        result = []
        for prop, username, email in proposals:
            result.append({
                'id': prop.id,
                'project_id': prop.project_id,
                'freelancer': {
                    'id': prop.freelancer_id,
                    'username': username,
                    'email': email
                },
                'cover_letter': prop.cover_letter,
                'proposed_rate': float(prop.proposed_rate) if prop.proposed_rate else None,
                'status': prop.status,
                'created_at': prop.created_at.isoformat() if prop.created_at else None
            })
            
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proposal_bp.route('/', methods=['GET'])
@jwt_required()
def list_freelancer_proposals():
    """
    List all proposals for the currently logged-in freelancer
    """
    try:
        ident = get_jwt_identity()
        
        if ident['role'] != 'freelancer':
            return jsonify({'error': 'only freelancers can view their proposals'}), 403
        
        # Get all proposals for the current freelancer with project details
        proposals = db.session.query(
            Proposal,
            Project.title,
            Project.budget,
            Project.status.label('project_status'),
            User.username.label('client_username'),
            User.email.label('client_email')
        ).join(
            Project, Project.id == Proposal.project_id
        ).join(
            User, User.id == Project.client_id
        ).filter(
            Proposal.freelancer_id == ident['id']
        ).order_by(
            Proposal.created_at.desc()
        ).all()
        
        result = []
        for prop, project_title, project_budget, project_status, client_username, client_email in proposals:
            result.append({
                'id': prop.id,
                'project': {
                    'id': prop.project_id,
                    'title': project_title,
                    'budget': float(project_budget) if project_budget else None,
                    'status': project_status
                },
                'client': {
                    'username': client_username,
                    'email': client_email
                },
                'cover_letter': prop.cover_letter,
                'proposed_rate': float(prop.proposed_rate) if prop.proposed_rate else None,
                'status': prop.status,
                'created_at': prop.created_at.isoformat() if prop.created_at else None
            })
            
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@proposal_bp.route('/<int:proposal_id>/status', methods=['PUT'])
@jwt_required()
def update_proposal_status(proposal_id):
    try:
        ident = get_jwt_identity()
        data = request.get_json() or {}
        
        if 'status' not in data:
            return jsonify({'error': 'status is required'}), 400
            
        if data['status'] not in ('accepted', 'rejected'):
            return jsonify({'error': "status must be either 'accepted' or 'rejected'"}), 400
            
        prop = Proposal.query.get_or_404(proposal_id)
        
        # Only project owner (client) can update status
        if prop.project.client_id != ident['id']:
            return jsonify({'error': 'only project client can update proposal status'}), 403
            
        # Check if proposal is already accepted/rejected
        if prop.status in ('accepted', 'rejected'):
            return jsonify({'error': f'proposal has already been {prop.status}'}), 400
            
        # Update status
        prop.status = data['status']
        
        # If accepting a proposal, reject all other proposals for this project
        if data['status'] == 'accepted':
            Proposal.query.filter(
                Proposal.project_id == prop.project_id,
                Proposal.id != proposal_id,
                Proposal.status == 'pending'
            ).update({'status': 'rejected'})
        
        db.session.commit()
        
        return jsonify({
            'message': f'proposal {data["status"]} successfully',
            'proposal_id': prop.id,
            'status': prop.status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
