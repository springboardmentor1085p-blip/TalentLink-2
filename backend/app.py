from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_socketio import SocketIO, emit, join_room
from flask_migrate import Migrate
from config import Config
from models import db, User, Profile, Project, Proposal, Contract, Message, Review, Notification, ProjectMilestone, MilestoneUpdate, Payment
import json
import logging
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
cors = CORS()
cors.init_app(app, 
    resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "X-CSRF-Token"],
            "expose_headers": ["Content-Type", "X-CSRF-Token"],
            "supports_credentials": True,
            "max_age": 600
        }
    })

db.init_app(app)
jwt = JWTManager(app)
socketio = SocketIO(app, 
                  cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
                  cors_credentials=True)
migrate = Migrate(app, db)

# Initialize database
with app.app_context():
    db.create_all()
    # Create demo users
    if not User.query.filter_by(email='client@demo.com').first():
        client = User(email='client@demo.com', role='client', name='Demo Client')
        client.set_password('password123')
        db.session.add(client)
        
        freelancer = User(email='freelancer@demo.com', role='freelancer', name='Demo Freelancer')
        freelancer.set_password('password123')
        db.session.add(freelancer)
        
        db.session.commit()
        
        # Create profiles
        client_profile = Profile(user_id=client.id, bio='Looking for talented freelancers')
        freelancer_profile = Profile(
            user_id=freelancer.id,
            bio='Full-stack developer with 5 years experience',
            skills=json.dumps(['React', 'Python', 'Flask', 'Node.js']),
            hourly_rate=50.0
        )
        db.session.add(client_profile)
        db.session.add(freelancer_profile)
        db.session.commit()

# Test endpoint
@app.route('/api/test', methods=['GET'])
@jwt_required()
def test_auth():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    return jsonify({'message': 'Auth working!', 'user_id': current_user_id, 'user': user.name if user else None})

# Auth Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(email=data['email'], role=data['role'], name=data['name'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    profile = Profile(user_id=user.id)
    db.session.add(profile)
    db.session.commit()
    
    token = create_access_token(identity=str(user.id))
    return jsonify({'token': token, 'user': {'id': user.id, 'email': user.email, 'role': user.role, 'name': user.name}}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = create_access_token(identity=str(user.id))
    return jsonify({'token': token, 'user': {'id': user.id, 'email': user.email, 'role': user.role, 'name': user.name}})

# Profile Routes
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    profile = Profile.query.filter_by(user_id=user.id).first()
    
    return jsonify({
        'user': {'id': user.id, 'email': user.email, 'role': user.role, 'name': user.name},
        'profile': {
            'bio': profile.bio,
            'skills': json.loads(profile.skills) if profile.skills else [],
            'hourly_rate': profile.hourly_rate,
            'portfolio_url': profile.portfolio_url,
            'location': profile.location
        }
    })

@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = int(get_jwt_identity())
    profile = Profile.query.filter_by(user_id=current_user_id).first()
    data = request.json
    
    profile.bio = data.get('bio', profile.bio)
    profile.skills = json.dumps(data.get('skills', [])) if 'skills' in data else profile.skills
    profile.hourly_rate = data.get('hourly_rate', profile.hourly_rate)
    profile.portfolio_url = data.get('portfolio_url', profile.portfolio_url)
    profile.location = data.get('location', profile.location)
    
    db.session.commit()
    return jsonify({'message': 'Profile updated'})

# Project Routes
@app.route('/api/projects', methods=['GET'])
def get_projects():
    status = request.args.get('status')
    search = request.args.get('search', '')
    client_id = request.args.get('client_id', type=int)
    
    # Start with base query
    query = Project.query
    
    # If client_id is provided, show ALL their projects (ignore status filter)
    # Otherwise, default to 'open' status for freelancers browsing
    if client_id:
        query = query.filter_by(client_id=client_id)
    else:
        # For freelancers, only show open projects by default
        status = status or 'open'
        query = query.filter_by(status=status)
    
    if search:
        query = query.filter(Project.title.contains(search) | Project.description.contains(search))
    
    projects = query.order_by(Project.created_at.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'budget': p.budget,
        'duration': p.duration,
        'skills_required': json.loads(p.skills_required) if p.skills_required else [],
        'status': p.status,
        'created_at': p.created_at.isoformat(),
        'client': {'id': p.client.id, 'name': p.client.name},
        'proposal_count': len(p.proposals)
    } for p in projects])

@app.route('/api/projects', methods=['POST'])
@jwt_required()
def create_project():
    try:
        current_user_id = int(get_jwt_identity())
        print(f"Creating project for user ID: {current_user_id}")
        
        user = User.query.get(current_user_id)
        if not user:
            print(f"User not found: {current_user_id}")
            return jsonify({'error': 'User not found'}), 404
            
        print(f"User found: {user.email}, role: {user.role}")
        
        if user.role != 'client':
            return jsonify({'error': 'Only clients can post projects'}), 403
        
        data = request.json
        print(f"Request data: {data}")
        
        # Validate required fields
        required_fields = ['title', 'description', 'budget']
        missing_fields = []
        
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
            elif field == 'budget':
                try:
                    budget_value = float(data[field])
                    if budget_value <= 0:
                        missing_fields.append(f'{field} (must be greater than 0)')
                except (ValueError, TypeError):
                    missing_fields.append(f'{field} (must be a valid number)')
            elif not data[field] or not str(data[field]).strip():
                missing_fields.append(field)
        
        if missing_fields:
            return jsonify({'error': f'Invalid or missing fields: {", ".join(missing_fields)}'}), 400
        
        project = Project(
            client_id=current_user_id,
            title=data['title'],
            description=data['description'],
            budget=float(data['budget']),
            duration=data.get('duration'),
            skills_required=json.dumps(data.get('skills_required', []))
        )
        db.session.add(project)
        db.session.commit()
        
        print(f"Project created successfully with ID: {project.id}")
        
        return jsonify({'id': project.id, 'message': 'Project created'}), 201
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating project: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    return jsonify({
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'budget': project.budget,
        'duration': project.duration,
        'skills_required': json.loads(project.skills_required) if project.skills_required else [],
        'status': project.status,
        'created_at': project.created_at.isoformat(),
        'client': {'id': project.client.id, 'name': project.client.name},
        'proposals': [{
            'id': prop.id,
            'freelancer': {'id': prop.freelancer.id, 'name': prop.freelancer.name},
            'proposed_amount': prop.proposed_amount,
            'delivery_time': prop.delivery_time,
            'status': prop.status
        } for prop in project.proposals]
    })

@app.route('/api/projects/<int:project_id>/my-proposal', methods=['GET'])
@jwt_required()
def get_my_proposal_for_project(project_id):
    """Get the current user's proposal for a specific project"""
    current_user_id = int(get_jwt_identity())
    
    proposal = Proposal.query.filter_by(
        project_id=project_id,
        freelancer_id=current_user_id
    ).first()
    
    if not proposal:
        return jsonify({'error': 'No proposal found'}), 404
    
    return jsonify({
        'id': proposal.id,
        'project_id': proposal.project_id,
        'cover_letter': proposal.cover_letter,
        'proposed_amount': proposal.proposed_amount,
        'delivery_time': proposal.delivery_time,
        'status': proposal.status,
        'created_at': proposal.created_at.isoformat()
    })

# Proposal Routes
@app.route('/api/proposals', methods=['POST'])
@jwt_required()
def create_proposal():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    if user.role != 'freelancer':
        return jsonify({'error': 'Only freelancers can submit proposals'}), 403
    
    data = request.json
    proposal = Proposal(
        project_id=data['project_id'],
        freelancer_id=current_user_id,
        cover_letter=data['cover_letter'],
        proposed_amount=data['proposed_amount'],
        delivery_time=data.get('delivery_time')
    )
    db.session.add(proposal)
    db.session.commit()
    
    # Create notification
    project = Project.query.get(data['project_id'])
    notif = Notification(
        user_id=project.client_id,
        type='new_proposal',
        content=f'New proposal received for {project.title}'
    )
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({'id': proposal.id, 'message': 'Proposal submitted'}), 201

@app.route('/api/proposals/<int:proposal_id>/accept', methods=['POST'])
@jwt_required()
def accept_proposal(proposal_id):
    current_user_id = int(get_jwt_identity())
    proposal = Proposal.query.get_or_404(proposal_id)
    project = Project.query.get(proposal.project_id)
    
    if project.client_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    proposal.status = 'accepted'
    project.status = 'in_progress'
    
    contract = Contract(
        project_id=project.id,
        proposal_id=proposal.id,
        freelancer_id=proposal.freelancer_id,
        amount=proposal.proposed_amount
    )
    db.session.add(contract)
    
    # Reject other proposals
    for p in project.proposals:
        if p.id != proposal_id:
            p.status = 'rejected'
    
    db.session.commit()
    
    return jsonify({'message': 'Proposal accepted', 'contract_id': contract.id})

@app.route('/api/my-proposals', methods=['GET'])
@jwt_required()
def get_my_proposals():
    current_user_id = int(get_jwt_identity())
    proposals = Proposal.query.filter_by(freelancer_id=current_user_id).all()
    
    return jsonify([{
        'id': p.id,
        'project': {'id': p.project.id, 'title': p.project.title},
        'proposed_amount': p.proposed_amount,
        'delivery_time': p.delivery_time,
        'status': p.status,
        'created_at': p.created_at.isoformat()
    } for p in proposals])

# Contract Routes
@app.route('/api/contracts', methods=['GET'])
@jwt_required()
def get_contracts():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role == 'freelancer':
        contracts = Contract.query.filter_by(freelancer_id=current_user_id).all()
    else:
        contracts = Contract.query.join(Project).filter(Project.client_id == current_user_id).all()
    
    return jsonify([{
        'id': c.id,
        'project': {
            'id': c.project.id, 
            'title': c.project.title,
            'client_id': c.project.client_id,
            'client_name': c.project.client.name
        },
        'freelancer': {'id': c.freelancer.id, 'name': c.freelancer.name},
        'amount': c.amount,
        'total_paid': c.total_paid,
        'remaining_amount': c.remaining_amount,
        'payment_status': c.payment_status,
        'payment_percentage': c.payment_percentage,
        'status': c.status,
        'start_date': c.start_date.isoformat(),
        'end_date': c.end_date.isoformat() if c.end_date else None
    } for c in contracts])

@app.route('/api/contracts/<int:contract_id>', methods=['GET'])
@jwt_required()
def get_contract_detail(contract_id):
    """Get detailed contract information including payments"""
    current_user_id = int(get_jwt_identity())
    contract = Contract.query.get_or_404(contract_id)
    
    # Check authorization
    if contract.freelancer_id != current_user_id and contract.project.client_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    payments = Payment.query.filter_by(contract_id=contract_id).order_by(Payment.created_at.desc()).all()
    
    return jsonify({
        'id': contract.id,
        'project': {
            'id': contract.project.id,
            'title': contract.project.title,
            'description': contract.project.description,
            'client_id': contract.project.client_id,
            'client_name': contract.project.client.name
        },
        'freelancer': {
            'id': contract.freelancer.id,
            'name': contract.freelancer.name
        },
        'amount': contract.amount,
        'total_paid': contract.total_paid,
        'remaining_amount': contract.remaining_amount,
        'payment_status': contract.payment_status,
        'payment_percentage': contract.payment_percentage,
        'status': contract.status,
        'start_date': contract.start_date.isoformat(),
        'end_date': contract.end_date.isoformat() if contract.end_date else None,
        'payments': [{
            'id': p.id,
            'amount': p.amount,
            'description': p.description,
            'status': p.status,
            'payment_method': p.payment_method,
            'transaction_id': p.transaction_id,
            'paid_at': p.paid_at.isoformat() if p.paid_at else None,
            'created_at': p.created_at.isoformat()
        } for p in payments]
    })

@app.route('/api/contracts/<int:contract_id>/complete', methods=['POST'])
@jwt_required()
def complete_contract(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    contract.status = 'completed'
    contract.project.status = 'completed'
    contract.end_date = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Contract completed'})

# Payment Routes
@app.route('/api/contracts/<int:contract_id>/payments', methods=['POST'])
@jwt_required()
def create_payment(contract_id):
    """Create a payment for a contract (simulated)"""
    current_user_id = int(get_jwt_identity())
    contract = Contract.query.get_or_404(contract_id)
    
    # Check if user is the client
    if contract.project.client_id != current_user_id:
        return jsonify({'error': 'Only the client can make payments'}), 403
    
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description', 'Payment')
    payment_method = data.get('payment_method', 'credit_card')
    
    if not amount or amount <= 0:
        return jsonify({'error': 'Invalid payment amount'}), 400
    
    if amount > contract.remaining_amount:
        return jsonify({'error': f'Payment amount exceeds remaining balance of ${contract.remaining_amount}'}), 400
    
    # Simulate payment processing
    import random
    import string
    transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    
    payment = Payment(
        contract_id=contract_id,
        amount=amount,
        description=description,
        status='completed',  # Simulated instant success
        payment_method=payment_method,
        transaction_id=transaction_id,
        paid_by=current_user_id,
        paid_at=datetime.utcnow()
    )
    
    db.session.add(payment)
    db.session.commit()
    
    # Create notification for freelancer
    notif = Notification(
        user_id=contract.freelancer_id,
        type='payment_received',
        content=f'Payment of ${amount} received for project "{contract.project.title}"'
    )
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({
        'id': payment.id,
        'amount': payment.amount,
        'transaction_id': payment.transaction_id,
        'status': payment.status,
        'remaining_amount': contract.remaining_amount,
        'payment_status': contract.payment_status,
        'message': 'Payment processed successfully'
    }), 201

@app.route('/api/contracts/<int:contract_id>/payments', methods=['GET'])
@jwt_required()
def get_contract_payments(contract_id):
    """Get all payments for a contract"""
    current_user_id = int(get_jwt_identity())
    contract = Contract.query.get_or_404(contract_id)
    
    # Check authorization
    if contract.freelancer_id != current_user_id and contract.project.client_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    payments = Payment.query.filter_by(contract_id=contract_id).order_by(Payment.created_at.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'amount': p.amount,
        'description': p.description,
        'status': p.status,
        'payment_method': p.payment_method,
        'transaction_id': p.transaction_id,
        'paid_at': p.paid_at.isoformat() if p.paid_at else None,
        'created_at': p.created_at.isoformat()
    } for p in payments])

@app.route('/api/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    current_user_id = int(get_jwt_identity())
    
    # Get all messages involving the current user
    messages = Message.query.filter(
        (Message.sender_id == current_user_id) | 
        (Message.receiver_id == current_user_id)
    ).order_by(Message.created_at.desc()).all()
    
    # Get unique user IDs from messages
    user_ids = set()
    for msg in messages:
        if msg.sender_id != current_user_id:
            user_ids.add(msg.sender_id)
        if msg.receiver_id != current_user_id:
            user_ids.add(msg.receiver_id)
    
    # Get user details for each conversation
    result = []
    for user_id in user_ids:
        user = User.query.get(user_id)
        if not user:
            continue
            
        # Get the last message in this conversation
        last_message = next(
            (m for m in messages 
             if (m.sender_id == user_id or m.receiver_id == user_id)),
            None
        )
        
        # Get unread count
        unread_count = Message.query.filter(
            Message.sender_id == user_id,
            Message.receiver_id == current_user_id,
            Message.is_read == False
        ).count()
        
        result.append({
            'id': user.id,
            'user_id': user.id,
            'name': user.name,
            'role': user.role,
            'last_message': {
                'content': last_message.content if last_message else None,
                'timestamp': last_message.created_at.isoformat() if last_message else None,
                'is_sender': last_message.sender_id == current_user_id if last_message else False
            },
            'unread_count': unread_count,
            'is_online': False
        })
    
    return jsonify(result)

@app.route('/api/messages', methods=['POST'])
@jwt_required()
def send_message():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        receiver_id = data.get('receiver_id')
        content = data.get('content')
        
        if not receiver_id or not content:
            return jsonify({'error': 'Receiver ID and content are required'}), 400
        
        # Verify receiver exists
        receiver = User.query.get(receiver_id)
        if not receiver:
            return jsonify({'error': 'Receiver not found'}), 404
        
        # Create message
        message = Message(
            sender_id=current_user_id,
            receiver_id=receiver_id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
        
        # Create notification for receiver
        notif = Notification(
            user_id=receiver_id,
            type='new_message',
            content=f'New message from {User.query.get(current_user_id).name}'
        )
        db.session.add(notif)
        db.session.commit()
        
        return jsonify({
            'id': message.id,
            'content': message.content,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'created_at': message.created_at.isoformat(),
            'is_read': message.is_read
        }), 201
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error sending message: {str(e)}")
        return jsonify({'error': 'Failed to send message'}), 500
@app.route('/api/messages', methods=['GET'])
@jwt_required()
def get_messages():
    current_user_id = int(get_jwt_identity())
    other_user_id = request.args.get('user_id', type=int)
    
    if not other_user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    # Get messages between the two users
    messages = Message.query.filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == current_user_id))
    ).order_by(Message.created_at.asc()).all()
    
    # Mark messages as read
    Message.query.filter(
        Message.sender_id == other_user_id,
        Message.receiver_id == current_user_id,
        Message.is_read == False
    ).update({
        'is_read': True,
        'read_at': datetime.utcnow()
    }, synchronize_session=False)
    
    db.session.commit()
    
    return jsonify([{
        'id': m.id,
        'content': m.content,
        'sender_id': m.sender_id,
        'receiver_id': m.receiver_id,
        'timestamp': m.created_at.isoformat(),
        'is_read': m.is_read,
        'read_at': m.read_at.isoformat() if m.read_at else None
    } for m in messages])

@app.route('/api/messages/mark-read', methods=['POST'])
@jwt_required()
def mark_messages_read():
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        message_ids = data.get('message_ids', [])
        
        if not message_ids:
            return jsonify({'error': 'No message IDs provided'}), 400
            
        # Update messages as read
        updated_count = Message.query.filter(
            Message.id.in_(message_ids),
            Message.receiver_id == current_user_id
        ).update({
            'is_read': True,
            'read_at': datetime.utcnow()
        }, synchronize_session=False)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'updated_count': updated_count
        })
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error marking messages as read: {str(e)}")
        return jsonify({'error': 'Failed to mark messages as read'}), 500

@app.route('/api/users/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    reviews = Review.query.filter_by(reviewee_id=user_id).all()
    
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
    
    return jsonify({
        'average_rating': round(avg_rating, 1),
        'total_reviews': len(reviews),
        'reviews': [{
            'id': r.id,
            'reviewer': {'name': r.reviewer.name},
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.isoformat()
        } for r in reviews]
    })

# Dashboard & Analytics
@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role == 'client':
        projects = Project.query.filter_by(client_id=current_user_id).all()
        total_proposals = sum(len(p.proposals) for p in projects)
        
        return jsonify({
            'total_projects': len(projects),
            'active_projects': len([p for p in projects if p.status == 'in_progress']),
            'completed_projects': len([p for p in projects if p.status == 'completed']),
            'total_proposals': total_proposals
        })
    else:
        proposals = Proposal.query.filter_by(freelancer_id=current_user_id).all()
        contracts = Contract.query.filter_by(freelancer_id=current_user_id).all()
        
        return jsonify({
            'total_proposals': len(proposals),
            'accepted_proposals': len([p for p in proposals if p.status == 'accepted']),
            'active_contracts': len([c for c in contracts if c.status == 'active']),
            'completed_contracts': len([c for c in contracts if c.status == 'completed']),
            'total_earnings': sum(c.amount for c in contracts if c.status == 'completed')
        })

# Notifications
@app.route('/api/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        current_user_id = int(get_jwt_identity())
        print(f"Fetching notifications for user ID: {current_user_id}")
        
        notifications = Notification.query.filter_by(user_id=current_user_id).order_by(Notification.created_at.desc()).limit(20).all()
        
        print(f"Found {len(notifications)} notifications")
        
        return jsonify([{
            'id': n.id,
            'type': n.type,
            'content': n.content,
            'read': n.read,
            'created_at': n.created_at.isoformat()
        } for n in notifications])
    except Exception as e:
        print(f"Error fetching notifications: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/notifications/<int:notif_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notif_id):
    notification = Notification.query.get_or_404(notif_id)
    notification.read = True
    db.session.commit()
    return jsonify({'message': 'Marked as read'})

@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user information by ID"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    })

# Project Milestone Routes
@app.route('/api/projects/<int:project_id>/milestones', methods=['GET'])
@jwt_required()
def get_project_milestones(project_id):
    """Get all milestones for a project"""
    project = Project.query.get_or_404(project_id)
    milestones = ProjectMilestone.query.filter_by(project_id=project_id).order_by(ProjectMilestone.order).all()
    
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'description': m.description,
        'status': m.status,
        'progress': m.progress,
        'order': m.order,
        'started_at': m.started_at.isoformat() if m.started_at else None,
        'completed_at': m.completed_at.isoformat() if m.completed_at else None,
        'created_at': m.created_at.isoformat(),
        'updated_at': m.updated_at.isoformat(),
        'updates_count': len(m.updates)
    } for m in milestones])

@app.route('/api/projects/<int:project_id>/milestones', methods=['POST'])
@jwt_required()
def create_project_milestones(project_id):
    """Create default milestones for a project"""
    current_user_id = int(get_jwt_identity())
    project = Project.query.get_or_404(project_id)
    
    # Check if user is authorized (client or freelancer on contract)
    contract = Contract.query.filter_by(project_id=project_id).first()
    if project.client_id != current_user_id and (not contract or contract.freelancer_id != current_user_id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Check if milestones already exist
    existing = ProjectMilestone.query.filter_by(project_id=project_id).first()
    if existing:
        return jsonify({'error': 'Milestones already exist for this project'}), 400
    
    # Create default milestones
    default_milestones = [
        {'name': 'Planning', 'description': 'Project planning and requirements gathering', 'order': 1},
        {'name': 'Design', 'description': 'UI/UX design and architecture', 'order': 2},
        {'name': 'Development', 'description': 'Core development and implementation', 'order': 3},
        {'name': 'Testing', 'description': 'Testing and quality assurance', 'order': 4},
        {'name': 'Deployment', 'description': 'Deployment and launch', 'order': 5}
    ]
    
    created_milestones = []
    for milestone_data in default_milestones:
        milestone = ProjectMilestone(
            project_id=project_id,
            **milestone_data
        )
        db.session.add(milestone)
        created_milestones.append(milestone)
    
    db.session.commit()
    
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'description': m.description,
        'status': m.status,
        'progress': m.progress,
        'order': m.order
    } for m in created_milestones]), 201

@app.route('/api/milestones/<int:milestone_id>', methods=['PUT'])
@jwt_required()
def update_milestone(milestone_id):
    """Update milestone progress and status"""
    current_user_id = int(get_jwt_identity())
    milestone = ProjectMilestone.query.get_or_404(milestone_id)
    
    # Check if user is authorized (freelancer on contract)
    contract = Contract.query.filter_by(project_id=milestone.project_id).first()
    if not contract or contract.freelancer_id != current_user_id:
        return jsonify({'error': 'Only the assigned freelancer can update milestones'}), 403
    
    data = request.get_json()
    
    # Update milestone
    if 'status' in data:
        milestone.status = data['status']
        if data['status'] == 'in_progress' and not milestone.started_at:
            milestone.started_at = datetime.utcnow()
        elif data['status'] == 'completed':
            milestone.completed_at = datetime.utcnow()
            milestone.progress = 100
    
    if 'progress' in data:
        milestone.progress = min(100, max(0, data['progress']))
    
    if 'description' in data:
        milestone.description = data['description']
    
    milestone.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Create notification for client
    notif = Notification(
        user_id=milestone.project.client_id,
        type='milestone_update',
        content=f'Milestone "{milestone.name}" updated to {milestone.progress}% in project "{milestone.project.title}"'
    )
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({
        'id': milestone.id,
        'name': milestone.name,
        'status': milestone.status,
        'progress': milestone.progress,
        'updated_at': milestone.updated_at.isoformat()
    })

@app.route('/api/milestones/<int:milestone_id>/updates', methods=['GET'])
@jwt_required()
def get_milestone_updates(milestone_id):
    """Get all updates for a milestone"""
    milestone = ProjectMilestone.query.get_or_404(milestone_id)
    updates = MilestoneUpdate.query.filter_by(milestone_id=milestone_id).order_by(MilestoneUpdate.created_at.desc()).all()
    
    return jsonify([{
        'id': u.id,
        'content': u.content,
        'progress': u.progress,
        'attachment_url': u.attachment_url,
        'created_at': u.created_at.isoformat(),
        'user': {
            'id': u.user.id,
            'name': u.user.name
        }
    } for u in updates])

@app.route('/api/milestones/<int:milestone_id>/updates', methods=['POST'])
@jwt_required()
def create_milestone_update(milestone_id):
    """Add an update/comment to a milestone"""
    current_user_id = int(get_jwt_identity())
    milestone = ProjectMilestone.query.get_or_404(milestone_id)
    data = request.get_json()
    
    # Check if user is authorized
    contract = Contract.query.filter_by(project_id=milestone.project_id).first()
    if not contract or contract.freelancer_id != current_user_id:
        return jsonify({'error': 'Only the assigned freelancer can add updates'}), 403
    
    update = MilestoneUpdate(
        milestone_id=milestone_id,
        user_id=current_user_id,
        content=data.get('content', ''),
        progress=data.get('progress'),
        attachment_url=data.get('attachment_url')
    )
    db.session.add(update)
    db.session.commit()
    
    # Create notification for client
    notif = Notification(
        user_id=milestone.project.client_id,
        type='milestone_update',
        content=f'New update on "{milestone.name}" in project "{milestone.project.title}"'
    )
    db.session.add(notif)
    db.session.commit()
    
    return jsonify({
        'id': update.id,
        'content': update.content,
        'progress': update.progress,
        'created_at': update.created_at.isoformat()
    }), 201

@app.route('/api/freelancers', methods=['GET'])
@jwt_required()
def get_freelancers():
    """Get all freelancers with their profiles"""
    freelancers = User.query.filter_by(role='freelancer').all()
    
    result = []
    for freelancer in freelancers:
        profile = Profile.query.filter_by(user_id=freelancer.id).first()
        
        # Calculate average rating
        reviews = Review.query.filter_by(reviewee_id=freelancer.id).all()
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 5.0
        
        result.append({
            'id': freelancer.id,
            'name': freelancer.name,
            'email': freelancer.email,
            'bio': profile.bio if profile else None,
            'skills': json.loads(profile.skills) if profile and profile.skills else [],
            'hourly_rate': profile.hourly_rate if profile else None,
            'portfolio_url': profile.portfolio_url if profile else None,
            'location': profile.location if profile else None,
            'rating': round(avg_rating, 1),
            'reviews_count': len(reviews)
        })
    
    return jsonify(result)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
