#!/usr/bin/env python3
"""
Migration script to add milestone tables to the database
"""
from app import app, db
from models import ProjectMilestone, MilestoneUpdate

def add_milestone_tables():
    """Add milestone tables to database"""
    with app.app_context():
        print("Creating milestone tables...")
        db.create_all()
        print("✓ Milestone tables created successfully!")
        print("\nNew tables added:")
        print("  - project_milestone")
        print("  - milestone_update")

if __name__ == '__main__':
    add_milestone_tables()
