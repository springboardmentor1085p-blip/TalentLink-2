from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if not data.get('email') or not data.get('password') or not data.get('username') or not data.get('role'):
        return jsonify({'error': 'username, email, password and role required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    hashed = generate_password_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password=hashed, role=data['role'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'registered'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'email and password required'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'invalid credentials'}), 401
    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    return jsonify({'access_token': token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    ident = get_jwt_identity()
    user = User.query.get(ident['id'])
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}), 200
