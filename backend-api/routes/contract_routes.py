from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Contract, Proposal

contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/', methods=['POST'])
@jwt_required()
def create_contract():
    ident = get_jwt_identity()
    data = request.get_json() or {}
    prop = Proposal.query.get_or_404(data.get('proposal_id'))
    # only client who owns the project can create contract
    if prop.project.client_id != ident['id']:
        return jsonify({'error': 'not authorized'}), 403
    if prop.status != 'accepted':
        return jsonify({'error': 'proposal must be accepted to create contract'}), 400
    contract = Contract(proposal_id=prop.id, start_date=data.get('start_date'), end_date=data.get('end_date'), status='active')
    db.session.add(contract)
    db.session.commit()
    return jsonify({'message': 'contract created', 'id': contract.id}), 201

@contract_bp.route('/<int:contract_id>', methods=['GET'])
@jwt_required()
def get_contract(contract_id):
    c = Contract.query.get_or_404(contract_id)
    return jsonify({
        'id': c.id,
        'proposal_id': c.proposal_id,
        'start_date': c.start_date.isoformat() if c.start_date else None,
        'end_date': c.end_date.isoformat() if c.end_date else None,
        'status': c.status
    }), 200
