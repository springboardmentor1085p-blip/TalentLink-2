from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Review, Contract

review_bp = Blueprint('review', __name__)

@review_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    ident = get_jwt_identity()
    data = request.get_json() or {}
    if not data.get('contract_id') or not data.get('rating'):
        return jsonify({'error': 'contract_id and rating required'}), 400
    contract = Contract.query.get_or_404(data.get('contract_id'))
    # basic check: only participants can review (either freelancer or client)
    prop = contract.proposal
    client_id = prop.project.client_id
    freelancer_id = prop.freelancer_id
    if ident['id'] not in (client_id, freelancer_id):
        return jsonify({'error': 'not authorized to review'}), 403
    review = Review(contract_id=contract.id, reviewer_id=ident['id'], rating=int(data.get('rating')), comment=data.get('comment'))
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'review saved', 'id': review.id}), 201
