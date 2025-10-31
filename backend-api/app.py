from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit, join_room
from models import db, Message, User
from config import Config
from datetime import datetime

# Import your route blueprints
from models import db
from config import Config

# Blueprints
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.project_routes import project_bp
from routes.proposal_routes import proposal_bp
from routes.contract_routes import contract_bp
from routes.message_routes import message_bp
from routes.review_routes import review_bp

# APP FACTORY
# ---------------------------------------------

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/profiles')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(proposal_bp, url_prefix='/api/proposals')
    app.register_blueprint(contract_bp, url_prefix='/api/contracts')
    app.register_blueprint(message_bp, url_prefix='/api/messages')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')

    @app.route('/')
    def home():
        return jsonify({'message': 'TalentLink API running'})

    return app

# ---------------------------------------------
# MAIN SOCKET.IO LOGIC
# ---------------------------------------------
app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect')
def handle_connect():
    print("✅ A user connected!")


@socketio.on('disconnect')
def handle_disconnect():
    print("❌ A user disconnected.")

@socketio.on('join')
def handle_join(data):
    if not data or 'room' not in data:
        print("⚠️ join event missing 'room' data")
        return

    room = data['room']
    join_room(room)
    print(f"👤 Joined room: {room}")
    emit('joined', {'room': room}, room=room)


# -------------------------------
# SEND MESSAGE
# -------------------------------
@socketio.on('send_message')
def handle_send_message(data):
    if not data:
        return

    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    room = f"user_{receiver_id}"  # ✅ always deliver to receiver room

    if not sender_id or not receiver_id or not content:
        print("⚠️ Missing message data")
        return

    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.utcnow()
    )
    db.session.add(message)
    db.session.commit()

    print(f"📨 Message from {sender_id} → {receiver_id}: {content}")

    # Emit to receiver only
    emit('receive_message', {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'content': content,
        'timestamp': message.timestamp.isoformat()
    }, room=room)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    print("🚀 TalentLink API + SocketIO server running at http://127.0.0.1:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

