from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from bson.objectid import ObjectId


class User(UserMixin):
    """User model for reporters - stored in MongoDB"""
    
    def __init__(self, email, full_name, phone, password, role="user"):
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.role = role
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self._id = None
    
    @staticmethod
    def create(email, full_name, phone, password):
        """Create and save a new user"""
        if db is None:
            raise Exception("Database connection failed")
        
        user = User(email, full_name, phone, password, role="user")
        user_dict = {
            "email": email,
            "full_name": full_name,
            "phone": phone,
            "role": "user",
            "password_hash": user.password_hash,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        result = db.users.insert_one(user_dict)
        user._id = str(result.inserted_id)
        return user
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        if db is None:
            return None
        user_data = db.users.find_one({"email": email})
        if user_data:
            user = User(
                user_data["email"],
                user_data["full_name"],
                user_data["phone"],
                "",
                user_data.get("role", "user")
            )
            user._id = str(user_data["_id"])
            user.password_hash = user_data["password_hash"]
            return user
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        if db is None:
            return None
        try:
            user_data = db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                user = User(
                    user_data["email"],
                    user_data["full_name"],
                    user_data["phone"],
                    "",
                    user_data.get("role", "user")
                )
                user._id = str(user_data["_id"])
                user.password_hash = user_data["password_hash"]
                return user
        except:
            pass
        return None
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self._id
    
    def __repr__(self):
        return f"<User {self.email}>"


class Rescuer(UserMixin):
    """Rescuer model - stored in MongoDB"""
    
    def __init__(self, email, full_name, phone, password, experience="", location=""):
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.role = "rescuer"
        self.password_hash = generate_password_hash(password)
        self.experience = experience
        self.location = location
        self.animals_rescued = 0
        self.rating = 5.0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self._id = None
    
    @staticmethod
    def create(email, full_name, phone, password, experience="", location=""):
        """Create and save a new rescuer"""
        if db is None:
            raise Exception("Database connection failed")
        
        rescuer = Rescuer(email, full_name, phone, password, experience, location)
        rescuer_dict = {
            "email": email,
            "full_name": full_name,
            "phone": phone,
            "role": "rescuer",
            "password_hash": rescuer.password_hash,
            "experience": experience,
            "location": location,
            "animals_rescued": 0,
            "rating": 5.0,
            "created_at": rescuer.created_at,
            "updated_at": rescuer.updated_at
        }
        result = db.rescuers.insert_one(rescuer_dict)
        rescuer._id = str(result.inserted_id)
        return rescuer
    
    @staticmethod
    def find_by_email(email):
        """Find rescuer by email"""
        if db is None:
            return None
        rescuer_data = db.rescuers.find_one({"email": email})
        if rescuer_data:
            rescuer = Rescuer(
                rescuer_data["email"],
                rescuer_data["full_name"],
                rescuer_data["phone"],
                "",
                rescuer_data.get("experience", ""),
                rescuer_data.get("location", "")
            )
            rescuer._id = str(rescuer_data["_id"])
            rescuer.password_hash = rescuer_data["password_hash"]
            rescuer.animals_rescued = rescuer_data.get("animals_rescued", 0)
            rescuer.rating = rescuer_data.get("rating", 5.0)
            return rescuer
        return None
    
    @staticmethod
    def find_by_id(rescuer_id):
        """Find rescuer by ID"""
        if db is None:
            return None
        try:
            rescuer_data = db.rescuers.find_one({"_id": ObjectId(rescuer_id)})
            if rescuer_data:
                rescuer = Rescuer(
                    rescuer_data["email"],
                    rescuer_data["full_name"],
                    rescuer_data["phone"],
                    "",
                    rescuer_data.get("experience", ""),
                    rescuer_data.get("location", "")
                )
                rescuer._id = str(rescuer_data["_id"])
                rescuer.password_hash = rescuer_data["password_hash"]
                rescuer.animals_rescued = rescuer_data.get("animals_rescued", 0)
                rescuer.rating = rescuer_data.get("rating", 5.0)
                return rescuer
        except:
            pass
        return None
    
    @staticmethod
    def find_all():
        """Find all rescuers"""
        if db is None:
            return []
        rescuers = []
        for rescuer_data in db.rescuers.find():
            rescuer = Rescuer(
                rescuer_data["email"],
                rescuer_data["full_name"],
                rescuer_data["phone"],
                "",
                rescuer_data.get("experience", ""),
                rescuer_data.get("location", "")
            )
            rescuer._id = str(rescuer_data["_id"])
            rescuer.password_hash = rescuer_data["password_hash"]
            rescuer.animals_rescued = rescuer_data.get("animals_rescued", 0)
            rescuer.rating = rescuer_data.get("rating", 5.0)
            rescuers.append(rescuer)
        return rescuers
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self._id
    
    def update_rescue_count(self):
        """Increment animals rescued"""
        if db is None:
            return
        db.rescuers.update_one(
            {"_id": ObjectId(self._id)},
            {"$inc": {"animals_rescued": 1}, "$set": {"updated_at": datetime.utcnow()}}
        )
        self.animals_rescued += 1
    
    def __repr__(self):
        return f"<Rescuer {self.email}>"


class Admin(UserMixin):
    """Admin model - stored in MongoDB"""
    
    def __init__(self, email, full_name, password):
        self.email = email
        self.full_name = full_name
        self.role = "admin"
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()
        self._id = None
    
    @staticmethod
    def create(email, full_name, password):
        """Create and save a new admin"""
        if db is None:
            raise Exception("Database connection failed")
        
        admin = Admin(email, full_name, password)
        admin_dict = {
            "email": email,
            "full_name": full_name,
            "role": "admin",
            "password_hash": admin.password_hash,
            "created_at": admin.created_at
        }
        result = db.admins.insert_one(admin_dict)
        admin._id = str(result.inserted_id)
        return admin
    
    @staticmethod
    def find_by_email(email):
        """Find admin by email"""
        if db is None:
            return None
        admin_data = db.admins.find_one({"email": email})
        if admin_data:
            admin = Admin(
                admin_data["email"],
                admin_data["full_name"],
                ""
            )
            admin._id = str(admin_data["_id"])
            admin.password_hash = admin_data["password_hash"]
            return admin
        return None
    
    @staticmethod
    def find_by_id(admin_id):
        """Find admin by ID"""
        if db is None:
            return None
        try:
            admin_data = db.admins.find_one({"_id": ObjectId(admin_id)})
            if admin_data:
                admin = Admin(
                    admin_data["email"],
                    admin_data["full_name"],
                    ""
                )
                admin._id = str(admin_data["_id"])
                admin.password_hash = admin_data["password_hash"]
                return admin
        except:
            pass
        return None
    
    @staticmethod
    def find_all():
        """Find all admins"""
        if db is None:
            return []
        admins = []
        for admin_data in db.admins.find():
            admin = Admin(
                admin_data["email"],
                admin_data["full_name"],
                ""
            )
            admin._id = str(admin_data["_id"])
            admin.password_hash = admin_data["password_hash"]
            admins.append(admin)
        return admins
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self._id
    
    def __repr__(self):
        return f"<Admin {self.email}>"

