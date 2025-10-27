from app import create_app
from models import db

app = create_app()

with app.app_context():
    # Drop all tables
    db.drop_all()
    print("Dropped all tables")
    
    # Create all tables
    db.create_all()
    print("Created all tables")
