#!/usr/bin/env python3
"""
Migration script to add payment table to the database
"""
from app import app, db
from models import Payment

def add_payment_table():
    """Add payment table to database"""
    with app.app_context():
        print("Creating payment table...")
        db.create_all()
        print("✓ Payment table created successfully!")
        print("\nNew table added:")
        print("  - payment")
        print("\nPayment features:")
        print("  - Track payments for contracts")
        print("  - Payment status (pending, completed, failed)")
        print("  - Transaction IDs")
        print("  - Payment methods")
        print("  - Payment history")

if __name__ == '__main__':
    add_payment_table()
