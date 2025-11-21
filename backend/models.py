from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'client' or 'freelancer'
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='client', lazy=True, foreign_keys='Project.client_id')
    proposals = db.relationship('Proposal', backref='freelancer', lazy=True)
    sent_messages = db.relationship('Message', backref='sender', lazy=True, foreign_keys='Message.sender_id')
    reviews_given = db.relationship('Review', backref='reviewer', lazy=True, foreign_keys='Review.reviewer_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text)
    skills = db.Column(db.Text)  # JSON string
    hourly_rate = db.Column(db.Float)
    portfolio_url = db.Column(db.String(255))
    avatar_url = db.Column(db.String(255))
    location = db.Column(db.String(100))
    
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50))
    skills_required = db.Column(db.Text)  # JSON string
    status = db.Column(db.String(20), default='open')  # open, in_progress, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    proposals = db.relationship('Proposal', backref='project', lazy=True, cascade='all, delete-orphan')
    contract = db.relationship('Contract', backref='project', uselist=False, cascade='all, delete-orphan')

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    proposed_amount = db.Column(db.Float, nullable=False)
    delivery_time = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'), nullable=False)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    
    proposal = db.relationship('Proposal', backref='contract')
    freelancer = db.relationship('User', backref='contracts')
    payments = db.relationship('Payment', backref='contract', lazy=True, cascade='all, delete-orphan')
    
    @property
    def total_paid(self):
        """Calculate total amount paid"""
        return sum(p.amount for p in self.payments if p.status == 'completed')
    
    @property
    def remaining_amount(self):
        """Calculate remaining amount to be paid"""
        return self.amount - self.total_paid
    
    @property
    def payment_status(self):
        """Get payment status: not_paid, partially_paid, paid"""
        paid = self.total_paid
        if paid == 0:
            return 'not_paid'
        elif paid < self.amount:
            return 'partially_paid'
        else:
            return 'paid'
    
    @property
    def payment_percentage(self):
        """Get payment completion percentage"""
        if self.amount == 0:
            return 0
        return round((self.total_paid / self.amount) * 100, 1)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    project = db.relationship('Project', backref='messages')
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
            db.session.commit()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    project = db.relationship('Project', backref='reviews')
    reviewee = db.relationship('User', foreign_keys=[reviewee_id], backref='reviews_received')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='notifications')

class ProjectMilestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Planning, Design, Development, Testing, Deployment
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    progress = db.Column(db.Integer, default=0)  # 0-100
    order = db.Column(db.Integer, nullable=False)  # Display order
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = db.relationship('Project', backref='milestones')
    updates = db.relationship('MilestoneUpdate', backref='milestone', lazy=True, cascade='all, delete-orphan')

class MilestoneUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    milestone_id = db.Column(db.Integer, db.ForeignKey('project_milestone.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    progress = db.Column(db.Integer)  # Progress at time of update
    attachment_url = db.Column(db.String(255))  # Optional file attachment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='milestone_updates')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))  # e.g., "Milestone 1 Payment", "Final Payment"
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    payment_method = db.Column(db.String(50))  # credit_card, paypal, bank_transfer, etc.
    transaction_id = db.Column(db.String(100))  # Simulated transaction ID
    paid_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Client who paid
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    payer = db.relationship('User', backref='payments_made')
