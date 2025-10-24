from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Message, User

message_bp = Blueprint('message', __name__)

@message_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    ident = get_jwt_identity()
    data = request.get_json() or {}
    if not data.get('receiver_id') or not data.get('content'):
        return jsonify({'error': 'receiver_id and content required'}), 400
    # simple send
    m = Message(sender_id=ident['id'], receiver_id=data['receiver_id'], content=data['content'])
    db.session.add(m)
    db.session.commit()
    return jsonify({'message': 'sent', 'id': m.id}), 201

@message_bp.route('/thread/<int:user_id>', methods=['GET'])
@jwt_required()
def get_thread(user_id):
    ident = get_jwt_identity()
    # fetch messages between current user and user_id
    msgs = Message.query.filter(
        ((Message.sender_id==ident['id']) & (Message.receiver_id==user_id)) |
        ((Message.sender_id==user_id) & (Message.receiver_id==ident['id']))
    ).order_by(Message.timestamp.asc()).all()
    return jsonify([{
        'id': mm.id,
        'sender_id': mm.sender_id,
        'receiver_id': mm.receiver_id,
        'content': mm.content,
        'timestamp': mm.timestamp.isoformat()
    } for mm in msgs]), 200
