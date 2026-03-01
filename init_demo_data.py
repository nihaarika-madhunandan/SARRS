"""
MongoDB Demo Data Initialization for SARRS
This script creates demo users, rescuers, admins, and reports for testing
"""

from models import db
from models.user import User, Rescuer, Admin
from models.report import Report
from datetime import datetime, timedelta
import random

def create_demo_data():
    """Create demo data for the system"""
    
    if db is None:
        print("❌ MongoDB connection failed!")
        return
    
    print("🚀 Starting demo data initialization...")
    
    # Clear collections first (optional - remove if you want to keep existing data)
    print("🧹 Clearing existing data...")
    db.users.delete_many({})
    db.rescuers.delete_many({})
    db.admins.delete_many({})
    db.reports.delete_many({})
    
    try:
        # ==================== CREATE ADMIN ====================
        print("👤 Creating admin account...")
        admin = Admin.create(
            email="admin@resqpaws.com",
            full_name="Admin Dashboard",
            password="Admin@12345"
        )
        print(f"✅ Admin created: {admin.email}")
        
        # ==================== CREATE RESCUERS ====================
        print("\n🚑 Creating rescuer accounts...")
        rescuers_data = [
            {"email": "john.rescuer@resqpaws.com", "name": "John Martinez", "phone": "+1-555-0101", "experience": "5 years", "location": "Downtown"},
            {"email": "sarah.rescue@resqpaws.com", "name": "Sarah Williams", "phone": "+1-555-0102", "experience": "3 years", "location": "North District"},
            {"email": "mike.saver@resqpaws.com", "name": "Mike Thompson", "phone": "+1-555-0103", "experience": "7 years", "location": "East Side"},
            {"email": "emma.hero@resqpaws.com", "name": "Emma Johnson", "phone": "+1-555-0104", "experience": "2 years", "location": "West Zone"},
            {"email": "alex.guardian@resqpaws.com", "name": "Alex Chen", "phone": "+1-555-0105", "experience": "4 years", "location": "Central Park"},
        ]
        
        rescuers = []
        for data in rescuers_data:
            rescuer = Rescuer.create(
                email=data["email"],
                full_name=data["name"],
                phone=data["phone"],
                password="Rescuer@12345",
                experience=data["experience"],
                location=data["location"]
            )
            rescuers.append(rescuer)
            print(f"✅ Rescuer created: {rescuer.full_name} ({rescuer.email})")
        
        # ==================== CREATE USERS ====================
        print("\n👥 Creating user accounts...")
        users_data = [
            {"email": "user1@resqpaws.com", "name": "Alice Smith", "phone": "+1-555-0201"},
            {"email": "user2@resqpaws.com", "name": "Bob Johnson", "phone": "+1-555-0202"},
            {"email": "user3@resqpaws.com", "name": "Carol White", "phone": "+1-555-0203"},
        ]
        
        users = []
        for data in users_data:
            user = User.create(
                email=data["email"],
                full_name=data["name"],
                phone=data["phone"],
                password="User@12345"
            )
            users.append(user)
            print(f"✅ User created: {user.full_name} ({user.email})")
        
        # ==================== CREATE DEMO REPORTS ====================
        print("\n📋 Creating demo animal rescue reports...")
        
        animal_data = [
            {"type": "Golden Retriever", "condition": "Injured leg", "location": "Central Park", "priority": "High", "description": "Dog found limping near the fountain, appears to be in pain"},
            {"type": "Persian Cat", "condition": "Stuck in tree", "location": "Maple Street", "priority": "Medium", "description": "White Persian cat stuck in oak tree for 2 days"},
            {"type": "Pigeon", "condition": "Broken wing", "location": "Downtown Market", "priority": "Medium", "description": "Pigeon with visibly broken wing, unable to fly"},
            {"type": "Rabbit", "condition": "Malnourished", "location": "East Park", "priority": "Low", "description": "Small rabbit found in park, appears underweight"},
            {"type": "German Shepherd", "condition": "Lost, scared", "location": "Harbor Road", "priority": "High", "description": "Large German Shepherd found wandering, possibly lost pet"},
            {"type": "Kitten", "condition": "Dehydrated", "location": "Warehouse District", "priority": "High", "description": "Found crying kitten, very weak and dehydrated"},
            {"type": "Owl", "condition": "Stunned", "location": "Forest Edge", "priority": "Medium", "description": "Barn owl likely hit by car, stunned but alive"},
            {"type": "Puppy", "condition": "Abandoned", "location": "City Center", "priority": "High", "description": "Newborn puppy found abandoned in cardboard box"},
        ]
        
        base_time = datetime.utcnow()
        reports = []
        
        for idx, data in enumerate(animal_data):
            # Create report
            reporter = random.choice(users)
            rescuer = random.choice(rescuers) if random.random() > 0.3 else None
            is_rescued = rescuer is not None and random.random() > 0.4
            
            report = Report.create(
                animal_type=data["type"],
                condition=data["condition"],
                location=data["location"],
                description=data["description"],
                priority=data["priority"],
                reporter_id=reporter._id,
                reporter_name=reporter.full_name,
                reporter_contact=reporter.phone,
                reporter_email=reporter.email,
                latitude=random.uniform(40.7, 40.8),
                longitude=random.uniform(-74.0, -73.9)
            )
            
            # Update report with rescuer if applicable
            if rescuer:
                report.claim(rescuer._id, rescuer.full_name, rescuer.phone, rescuer.email)
                
                if is_rescued:
                    report.mark_rescued()
                    rescuer.update_rescue_count()
                    print(f"✅ Report created & rescued: {data['type']} by {rescuer.full_name}")
                else:
                    print(f"✅ Report created & claimed: {data['type']} by {rescuer.full_name}")
            else:
                print(f"✅ Report created (pending): {data['type']}")
            
            reports.append(report)
        
        # ==================== PRINT SUMMARY ====================
        print("\n" + "="*60)
        print("✅ DEMO DATA INITIALIZATION COMPLETE!")
        print("="*60)
        print("\n📊 SUMMARY:")
        print(f"   • Admins created: 1")
        print(f"   • Rescuers created: {len(rescuers)}")
        print(f"   • Users created: {len(users)}")
        print(f"   • Reports created: {len(reports)}")
        print(f"   • Reports with rescuers: {sum(1 for r in reports if r.rescuer_id)}")
        print(f"   • Reports rescued: {sum(1 for r in reports if r.is_rescued)}")
        print(f"   • Pending reports: {sum(1 for r in reports if not r.is_rescued)}")
        
        print("\n🔑 LOGIN CREDENTIALS:")
        print("   Admin Account:")
        print("      Email: admin@resqpaws.com")
        print("      Password: Admin@12345")
        print("\n   Sample Rescuer Account:")
        print("      Email: john.rescuer@resqpaws.com")
        print("      Password: Rescuer@12345")
        print("\n   Sample User Account:")
        print("      Email: user1@resqpaws.com")
        print("      Password: User@12345")
        
        print("\n💡 TIP: Login with any email and the system will auto-detect your role!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error creating demo data: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    create_demo_data()
