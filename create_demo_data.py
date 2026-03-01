#!/usr/bin/env python
"""
ResQPaws - Demo Data Generator
Creates test accounts and demo reports for testing the application
"""

from app import app, db
from models.user import User, Rescuer, Admin
from models.report import Report
from datetime import datetime, timedelta
import os

def create_demo_data():
    """Create demo users, rescuers, admins, and reports"""
    
    with app.app_context():
        # Clear existing data (optional - comment out to keep existing data)
        print("🗑️  Clearing existing data...")
        db.session.query(Report).delete()
        db.session.query(User).delete()
        db.session.query(Rescuer).delete()
        db.session.query(Admin).delete()
        db.session.commit()
        
        print("📝 Creating demo accounts...\n")
        
        # ==================== CREATE DEMO USERS ====================
        print("👤 Creating Demo Users (Reporters)...")
        
        user1 = User(
            email="user@example.com",
            full_name="John Reporter",
            phone="555-0101",
            role="user"
        )
        user1.set_password("password123")
        
        user2 = User(
            email="reporter@demo.com",
            full_name="Sarah Finder",
            phone="555-0102",
            role="user"
        )
        user2.set_password("demo1234")
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        print("   ✅ User 1: user@example.com / password123")
        print("   ✅ User 2: reporter@demo.com / demo1234\n")
        
        # ==================== CREATE DEMO RESCUERS ====================
        print("🚀 Creating Demo Rescuers...")
        
        rescuer1 = Rescuer(
            email="rescuer@example.com",
            full_name="Alex Rescuer",
            phone="555-0201",
            experience="5 years",
            location="Downtown",
            role="rescuer",
            animals_rescued=15,
            rating=4.8
        )
        rescuer1.set_password("rescuer123")
        
        rescuer2 = Rescuer(
            email="demo.rescuer@test.com",
            full_name="Maria Cruz",
            phone="555-0202",
            experience="3 years",
            location="North District",
            role="rescuer",
            animals_rescued=8,
            rating=4.5
        )
        rescuer2.set_password("rescuer456")
        
        rescuer3 = Rescuer(
            email="pro.rescuer@mail.com",
            full_name="James Patterson",
            phone="555-0203",
            experience="10 years",
            location="East Side",
            role="rescuer",
            animals_rescued=42,
            rating=5.0
        )
        rescuer3.set_password("rescuer789")
        
        db.session.add(rescuer1)
        db.session.add(rescuer2)
        db.session.add(rescuer3)
        db.session.commit()
        
        print("   ✅ Rescuer 1: rescuer@example.com / rescuer123")
        print("   ✅ Rescuer 2: demo.rescuer@test.com / rescuer456")
        print("   ✅ Rescuer 3: pro.rescuer@mail.com / rescuer789\n")
        
        # ==================== CREATE DEMO ADMIN ====================
        print("🛡️  Creating Demo Admin...")
        
        admin = Admin(
            email="admin@example.com",
            full_name="Admin User",
            role="admin"
        )
        admin.set_password("admin123")
        
        db.session.add(admin)
        db.session.commit()
        
        print("   ✅ Admin: admin@example.com / admin123\n")
        
        # ==================== CREATE DEMO REPORTS ====================
        print("📋 Creating Demo Animal Reports...\n")
        
        demo_reports = [
            {
                "animal_type": "Dog",
                "condition": "Injured front leg",
                "location": "Central Park, Downtown",
                "latitude": 40.7829,
                "longitude": -73.9654,
                "priority": "High",
                "description": "Golden Retriever with a fractured front leg. Very friendly, needs immediate care.",
                "reporter_id": user1.id,
                "reporter_name": user1.full_name,
                "reporter_contact": user1.phone,
                "reporter_email": user1.email,
                "status": "Pending",
                "is_rescued": False,
                "created_at": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "animal_type": "Cat",
                "condition": "Stuck in tree",
                "location": "Maple Street, Residential Area",
                "latitude": 40.7614,
                "longitude": -73.9776,
                "priority": "Medium",
                "description": "Orange tabby cat stuck on high branch. Unable to come down for 6 hours.",
                "reporter_id": user2.id,
                "reporter_name": user2.full_name,
                "reporter_contact": user2.phone,
                "reporter_email": user2.email,
                "status": "In Progress",
                "is_rescued": False,
                "rescuer_id": rescuer1.id,
                "rescuer_name": rescuer1.full_name,
                "rescuer_contact": rescuer1.phone,
                "rescuer_email": rescuer1.email,
                "claimed_at": datetime.utcnow() - timedelta(hours=1),
                "created_at": datetime.utcnow() - timedelta(hours=3)
            },
            {
                "animal_type": "Bird",
                "condition": "Wing injury",
                "location": "Harbor Road, Beach Area",
                "latitude": 40.5731,
                "longitude": -73.9712,
                "priority": "High",
                "description": "Seagull with apparent wing fracture. Unable to fly.",
                "reporter_id": user1.id,
                "reporter_name": user1.full_name,
                "reporter_contact": user1.phone,
                "reporter_email": user1.email,
                "status": "Rescued",
                "is_rescued": True,
                "rescuer_id": rescuer3.id,
                "rescuer_name": rescuer3.full_name,
                "rescuer_contact": rescuer3.phone,
                "rescuer_email": rescuer3.email,
                "claimed_at": datetime.utcnow() - timedelta(hours=5),
                "completed_at": datetime.utcnow() - timedelta(hours=1),
                "created_at": datetime.utcnow() - timedelta(hours=6)
            },
            {
                "animal_type": "Rabbit",
                "condition": "Bleeding from mouth",
                "location": "Community Garden, West End",
                "latitude": 40.7830,
                "longitude": -74.0033,
                "priority": "High",
                "description": "White rabbit found in garden with signs of injury. Possibly hit by a car.",
                "reporter_id": user2.id,
                "reporter_name": user2.full_name,
                "reporter_contact": user2.phone,
                "reporter_email": user2.email,
                "status": "Pending",
                "is_rescued": False,
                "created_at": datetime.utcnow() - timedelta(hours=1)
            },
            {
                "animal_type": "Fox",
                "condition": "Caught in fence",
                "location": "Industrial Park, North District",
                "latitude": 40.8089,
                "longitude": -73.9482,
                "priority": "Medium",
                "description": "Red fox tangled in chain-link fence. Appears distressed.",
                "reporter_id": user1.id,
                "reporter_name": user1.full_name,
                "reporter_contact": user1.phone,
                "reporter_email": user1.email,
                "status": "In Progress",
                "is_rescued": False,
                "rescuer_id": rescuer2.id,
                "rescuer_name": rescuer2.full_name,
                "rescuer_contact": rescuer2.phone,
                "rescuer_email": rescuer2.email,
                "claimed_at": datetime.utcnow() - timedelta(minutes=30),
                "created_at": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "animal_type": "Pigeon",
                "condition": "Broken wing",
                "location": "Grand Central Station, Downtown",
                "latitude": 40.7527,
                "longitude": -73.9772,
                "priority": "Low",
                "description": "Gray pigeon with visibly broken right wing. Cannot fly.",
                "reporter_id": user2.id,
                "reporter_name": user2.full_name,
                "reporter_contact": user2.phone,
                "reporter_email": user2.email,
                "status": "Rescued",
                "is_rescued": True,
                "rescuer_id": rescuer1.id,
                "rescuer_name": rescuer1.full_name,
                "rescuer_contact": rescuer1.phone,
                "rescuer_email": rescuer1.email,
                "claimed_at": datetime.utcnow() - timedelta(hours=8),
                "completed_at": datetime.utcnow() - timedelta(hours=3),
                "created_at": datetime.utcnow() - timedelta(hours=10)
            },
        ]
        
        for idx, report_data in enumerate(demo_reports, 1):
            report = Report(**report_data)
            db.session.add(report)
            print(f"   Report {idx}: {report_data['animal_type']} - {report_data['condition']}")
        
        db.session.commit()
        print(f"\n   ✅ Created {len(demo_reports)} demo reports\n")
        
        # ==================== SUMMARY ====================
        print("=" * 60)
        print("✅ DEMO DATA CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("\n📚 TEST CREDENTIALS:\n")
        
        print("👤 USERS (Reporters):")
        print("   Email: user@example.com")
        print("   Password: password123")
        print()
        print("   Email: reporter@demo.com")
        print("   Password: demo1234")
        print()
        
        print("🚀 RESCUERS:")
        print("   Email: rescuer@example.com")
        print("   Password: rescuer123")
        print()
        print("   Email: demo.rescuer@test.com")
        print("   Password: rescuer456")
        print()
        print("   Email: pro.rescuer@mail.com")
        print("   Password: rescuer789")
        print()
        
        print("🛡️  ADMIN:")
        print("   Email: admin@example.com")
        print("   Password: admin123")
        print()
        
        print("=" * 60)
        print("\n🌐 Access the application at: http://localhost:5000\n")
        print("📝 Test Flow:")
        print("   1. Login as USER to see the reporter dashboard")
        print("   2. Login as RESCUER to claim and rescue animals")
        print("   3. Login as ADMIN to view analytics\n")

if __name__ == "__main__":
    create_demo_data()
