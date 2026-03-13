#!/usr/bin/env python
"""
SARRS - Demo Data Generator for Live MongoDB
Creates comprehensive demo accounts and reports for testing on MongoDB Atlas
Run this in your deployed environment or after MongoDB connection is live:
    python init_demo_data_live.py
"""

from models import db
from models.user import User, Rescuer, Admin
from models.report import Report
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

def create_demo_data():
    """Create comprehensive demo data for all roles"""
    
    if db is None:
        print("❌ MongoDB connection failed. Check your MONGODB_URI in .env")
        return False
    
    try:
        print("🚀 Starting SARRS Demo Data Creation...\n")
        
        # ==================== CLEAR EXISTING DATA ====================
        print("🗑️  Clearing existing demo data...")
        db.users.delete_many({})
        db.rescuers.delete_many({})
        db.admins.delete_many({})
        db.reports.delete_many({})
        print("✅ Cleared all collections\n")
        
        # ==================== CREATE DEMO USERS (REPORTERS) ====================
        print("👤 Creating Demo Users (Reporters)...")
        
        users_data = [
            {
                "email": "user@example.com",
                "full_name": "John Reporter",
                "phone": "+1-555-0101",
                "password": "password123",
                "description": "Wildlife enthusiast from downtown"
            },
            {
                "email": "sarah@example.com",
                "full_name": "Sarah Finder",
                "phone": "+1-555-0102",
                "password": "demo1234",
                "description": "Animal welfare volunteer"
            },
            {
                "email": "Mike.chen@example.com",
                "full_name": "Mike Chen",
                "phone": "+1-555-0103",
                "password": "secure123",
                "description": "Park ranger with rescue experience"
            },
            {
                "email": "emma.watson@example.com",
                "full_name": "Emma Watson",
                "phone": "+1-555-0104",
                "password": "emma1234",
                "description": "Community coordinator"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            try:
                user = User.create(
                    user_data["email"],
                    user_data["full_name"],
                    user_data["phone"],
                    user_data["password"]
                )
                created_users.append(user)
                print(f"   ✅ {user_data['full_name']}: {user_data['email']} / {user_data['password']}")
            except Exception as e:
                print(f"   ⚠️  Error creating user {user_data['email']}: {e}")
        
        print()
        
        # ==================== CREATE DEMO RESCUERS ====================
        print("🚀 Creating Demo Rescuers...")
        
        rescuers_data = [
            {
                "email": "alex.rescuer@example.com",
                "full_name": "Alex Rescuer",
                "phone": "+1-555-0201",
                "password": "rescuer123",
                "experience": "5 years - Specialized in bird rescue",
                "location": "Downtown Rescue Center",
                "description": "Professional wildlife rescuer with expertise in aerial rescues"
            },
            {
                "email": "james.wildlife@example.com",
                "full_name": "James Wilson",
                "phone": "+1-555-0202",
                "password": "james1234",
                "experience": "8 years - Wildlife rehabilitation",
                "location": "Northern Animal Sanctuary",
                "description": "Expert in large animal rescue and rehabilitation"
            },
            {
                "email": "lisa.rescue@example.com",
                "full_name": "Lisa Johnson",
                "phone": "+1-555-0203",
                "password": "lisa5678",
                "experience": "6 years - Urban wildlife rescue",
                "location": "City Wildlife Services",
                "description": "Specialized in urban animal rescue and relocation"
            },
            {
                "email": "david.rescuer@example.com",
                "full_name": "David Kumar",
                "phone": "+1-555-0204",
                "password": "david123",
                "experience": "10 years - All species rescue",
                "location": "Metropolitan Rescue Team",
                "description": "Senior rescuer with comprehensive wildlife experience"
            },
            {
                "email": "sophia.wildlife@example.com",
                "full_name": "Sophia Martinez",
                "phone": "+1-555-0205",
                "password": "sophia99",
                "experience": "3 years - Small animal specialist",
                "location": "Community Animal Care",
                "description": "Focused on small animal rescue and emergency response"
            }
        ]
        
        created_rescuers = []
        for rescuer_data in rescuers_data:
            try:
                rescuer = Rescuer.create(
                    rescuer_data["email"],
                    rescuer_data["full_name"],
                    rescuer_data["phone"],
                    rescuer_data["password"],
                    rescuer_data["experience"],
                    rescuer_data["location"]
                )
                created_rescuers.append(rescuer)
                print(f"   ✅ {rescuer_data['full_name']}: {rescuer_data['email']} / {rescuer_data['password']}")
                print(f"      📍 {rescuer_data['location']} | 🎖️  {rescuer_data['experience']}\n")
            except Exception as e:
                print(f"   ⚠️  Error creating rescuer {rescuer_data['email']}: {e}")
        
        print()
        
        # ==================== CREATE DEMO ADMINS ====================
        print("👨‍💼 Creating Demo Admins...")
        
        admins_data = [
            {
                "email": "admin@sarrs.com",
                "full_name": "Admin Dashboard",
                "password": "admin1234",
                "description": "Main system administrator"
            },
            {
                "email": "manager@sarrs.com",
                "full_name": "System Manager",
                "password": "manager123",
                "description": "Operations manager"
            }
        ]
        
        created_admins = []
        for admin_data in admins_data:
            try:
                admin = Admin.create(
                    admin_data["email"],
                    admin_data["full_name"],
                    admin_data["password"]
                )
                created_admins.append(admin)
                print(f"   ✅ {admin_data['full_name']}: {admin_data['email']} / {admin_data['password']}")
                print(f"      {admin_data['description']}\n")
            except Exception as e:
                print(f"   ⚠️  Error creating admin {admin_data['email']}: {e}")
        
        print()
        
        # ==================== CREATE DEMO REPORTS ====================
        print("📋 Creating Demo Reports (Animals Needing Help)...")
        
        reports_data = [
            {
                "animal_type": "Bird",
                "condition": "Injured Wing",
                "location": "Downtown Park",
                "description": "Eagle found with broken wing near the fountain. Alert and responsive.",
                "priority": "High",
                "reporter_idx": 0,
                "status": "Pending",
                "latitude": 40.7128,
                "longitude": -74.0060
            },
            {
                "animal_type": "Dog",
                "condition": "Lost/Stray",
                "location": "Main Street, Commercial District",
                "description": "Golden Retriever, tag missing, appears friendly but scared. Microchip check needed.",
                "priority": "Medium", 
                "reporter_idx": 1,
                "status": "Pending",
                "latitude": 40.7150,
                "longitude": -74.0070
            },
            {
                "animal_type": "Cat",
                "condition": "Stuck/Trapped",
                "location": "Residential Area, Oak Avenue",
                "description": "Orange tabby cat stuck in tree for 2 days. Owner very concerned.",
                "priority": "Medium",
                "reporter_idx": 2,
                "status": "Assigned",
                "assigned_to": 0 if created_rescuers else None,
                "latitude": 40.7200,
                "longitude": -74.0100
            },
            {
                "animal_type": "Deer",
                "condition": "Hit by Vehicle",
                "location": "Highway 5, Mile Marker 42",
                "description": "Deer hit by car, unable to move. Urgent medical attention needed. On roadside.",
                "priority": "Critical",
                "reporter_idx": 0,
                "status": "Assigned",
                "assigned_to": 1 if len(created_rescuers) > 1 else None,
                "latitude": 40.6800,
                "longitude": -74.0200
            },
            {
                "animal_type": "Raccoon",
                "condition": "Disease/Illness Suspected",
                "location": "Suburban Neighborhood",
                "description": "Raccoon acting disoriented near residential area. Possible rabies. Keep distance.",
                "priority": "High",
                "reporter_idx": 3,
                "status": "Pending",
                "latitude": 40.7300,
                "longitude": -74.0150
            },
            {
                "animal_type": "Swan",
                "condition": "Caught in Debris",
                "location": "Riverside Lake",
                "description": "Swan tangled in fishing net and plastic. Unable to swim properly. In water.",
                "priority": "High",
                "reporter_idx": 1,
                "status": "Completed",
                "assigned_to": 2 if len(created_rescuers) > 2 else None,
                "is_rescued": True,
                "latitude": 40.6900,
                "longitude": -74.0180
            },
            {
                "animal_type": "Fox",
                "condition": "Suspected Injury",
                "location": "Forest Edge, Conservation Area",
                "description": "Red fox seen limping. Possibly broken front leg. Shy but observable from distance.",
                "priority": "Medium",
                "reporter_idx": 2,
                "status": "Assigned",
                "assigned_to": 3 if len(created_rescuers) > 3 else None,
                "latitude": 40.6750,
                "longitude": -74.0250
            },
            {
                "animal_type": "Rabbit",
                "condition": "Orphaned/Abandoned",
                "location": "Residential Garden",
                "description": "Young rabbit found without mother. Appears healthy but needs feeding. In box.",
                "priority": "Low",
                "reporter_idx": 3,
                "status": "Assigned",
                "assigned_to": 4 if len(created_rescuers) > 4 else None,
                "latitude": 40.7100,
                "longitude": -74.0210
            }
        ]
        
        created_reports = []
        for report_data in reports_data:
            try:
                reporter = created_users[report_data["reporter_idx"]]
                
                report = Report.create(
                    animal_type=report_data["animal_type"],
                    condition=report_data["condition"],
                    location=report_data["location"],
                    description=report_data["description"],
                    priority=report_data["priority"],
                    reporter_id=reporter._id,
                    reporter_name=reporter.full_name,
                    reporter_contact=reporter.phone,
                    reporter_email=reporter.email,
                    latitude=report_data.get("latitude"),
                    longitude=report_data.get("longitude")
                )
                
                # Update status if needed
                if report_data.get("status") == "Assigned" and report_data.get("assigned_to") is not None:
                    rescuer = created_rescuers[report_data["assigned_to"]]
                    db.reports.update_one(
                        {"_id": ObjectId(report.id)},
                        {
                            "$set": {
                                "status": "Assigned",
                                "rescuer_id": rescuer._id,
                                "rescuer_name": rescuer.full_name,
                                "rescuer_contact": rescuer.phone,
                                "rescuer_email": rescuer.email,
                                "claimed_at": datetime.utcnow(),
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                
                # Mark as completed if specified
                if report_data.get("is_rescued"):
                    db.reports.update_one(
                        {"_id": ObjectId(report.id)},
                        {
                            "$set": {
                                "is_rescued": True,
                                "status": "Completed",
                                "completed_at": datetime.utcnow() - timedelta(hours=2),
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                
                created_reports.append(report)
                print(f"   ✅ {report_data['animal_type']}: {report_data['condition']}")
                print(f"      📍 {report_data['location']} | Priority: {report_data['priority']}")
                print(f"      Reported by: {reporter.full_name}\n")
            except Exception as e:
                print(f"   ⚠️  Error creating report: {e}")
        
        print("\n" + "="*60)
        print("✨ DEMO DATA CREATION COMPLETE! ✨")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   👤 Users (Reporters): {len(created_users)}")
        print(f"   🚀 Rescuers: {len(created_rescuers)}")
        print(f"   👨‍💼 Admins: {len(created_admins)}")
        print(f"   📋 Reports: {len(created_reports)}")
        
        print("\n🔐 LOGIN CREDENTIALS:")
        print("\n📝 REPORTER ACCOUNTS:")
        print("   • user@example.com / password123")
        print("   • sarah@example.com / demo1234")
        print("   • Mike.chen@example.com / secure123")
        print("   • emma.watson@example.com / emma1234")
        
        print("\n🚒 RESCUER ACCOUNTS:")
        print("   • alex.rescuer@example.com / rescuer123")
        print("   • james.wildlife@example.com / james1234")
        print("   • lisa.rescue@example.com / lisa5678")
        print("   • david.rescuer@example.com / david123")
        print("   • sophia.wildlife@example.com / sophia99")
        
        print("\n🔑 ADMIN ACCOUNTS:")
        print("   • admin@sarrs.com / admin1234")
        print("   • manager@sarrs.com / manager123")
        
        print("\n✅ Demo data is live and ready to use on MongoDB Atlas!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating demo data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_demo_data()
