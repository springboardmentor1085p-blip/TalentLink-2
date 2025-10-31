from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Message, User
from datetime import datetime

message_bp = Blueprint('message', __name__)

# --------------------------------------------
# Send a message (authenticated users only)
# --------------------------------------------
@message_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    ident = get_jwt_identity()

    # ✅ Handle both string and dict identities
    if isinstance(ident, dict):
        user_id = ident.get('id')
    else:
        user_id = ident

    data = request.get_json() or {}

    receiver_id = data.get('receiver_id')
    content = data.get('content')

    if not receiver_id or not content:
        return jsonify({'error': 'receiver_id and content are required'}), 400

    # Check if receiver exists
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({'error': 'Receiver not found'}), 404

    # Create and store the message
    message = Message(
        sender_id=user_id,
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.utcnow()
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({
        'message': 'Message sent successfully',
        'id': message.id,
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'timestamp': message.timestamp.isoformat()
    }), 201


# --------------------------------------------
# Get all messages between logged-in user and another user
# --------------------------------------------
@message_bp.route('/thread/<int:user_id>', methods=['GET'])
@jwt_required()
def get_thread(user_id):
    ident = get_jwt_identity()

    # ✅ Handle both string and dict identities
    if isinstance(ident, dict):
        current_user_id = ident.get('id')
    else:
        current_user_id = ident

    # Fetch messages between the current user and the specified user
    msgs = Message.query.filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user_id))
    ).order_by(Message.timestamp.asc()).all()

    # Format response
    return jsonify([
        {
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in msgs
    ]), 200


# --------------------------------------------
# Get inbox (all recent messages for logged-in user)
# --------------------------------------------
@message_bp.route('/inbox', methods=['GET'])
@jwt_required()
def get_inbox():
    ident = get_jwt_identity()

    if isinstance(ident, dict):
        current_user_id = ident.get('id')
    else:
        current_user_id = ident

    # Fetch all messages received by the current user
    msgs = Message.query.filter_by(receiver_id=current_user_id).order_by(Message.timestamp.desc()).all()

    return jsonify([
        {
            'id': msg.id,
            'sender_id': msg.sender_id,
            'sender_name': msg.sender.username if msg.sender else None,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in msgs
    ]), 200
