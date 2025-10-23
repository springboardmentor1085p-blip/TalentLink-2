from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Proposal, Project

proposal_bp = Blueprint('proposal', __name__)

@proposal_bp.route('/<int:project_id>', methods=['POST'])
@jwt_required()
def submit_proposal(project_id):
    ident = get_jwt_identity()
    if ident['role'] != 'freelancer':
        return jsonify({'error': 'only freelancers can submit proposals'}), 403
    data = request.get_json() or {}
    p = Project.query.get_or_404(project_id)
    prop = Proposal(
        project_id=project_id,
        freelancer_id=ident['id'],
        cover_letter=data.get('cover_letter'),
        proposed_rate=data.get('proposed_rate')
    )
    db.session.add(prop)
    db.session.commit()
    return jsonify({'message': 'proposal submitted', 'id': prop.id}), 201

@proposal_bp.route('/project/<int:project_id>', methods=['GET'])
def list_proposals_for_project(project_id):
    proposals = Proposal.query.filter_by(project_id=project_id).all()
    return jsonify([{
        'id': pr.id,
        'project_id': pr.project_id,
        'freelancer_id': pr.freelancer_id,
        'cover_letter': pr.cover_letter,
        'proposed_rate': pr.proposed_rate,
        'status': pr.status
    } for pr in proposals]), 200

@proposal_bp.route('/<int:proposal_id>/status', methods=['PUT'])
@jwt_required()
def update_proposal_status(proposal_id):
    ident = get_jwt_identity()
    data = request.get_json() or {}
    prop = Proposal.query.get_or_404(proposal_id)
    # only project owner (client) can update status
    if prop.project.client_id != ident['id']:
        return jsonify({'error': 'only project client can update proposal status'}), 403
    if data.get('status') not in ('accepted', 'rejected'):
        return jsonify({'error': 'invalid status'}), 400
    prop.status = data.get('status')
    db.session.commit()
    return jsonify({'message': 'status updated'}), 200
