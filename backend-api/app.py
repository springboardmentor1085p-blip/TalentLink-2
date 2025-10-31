from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
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

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
