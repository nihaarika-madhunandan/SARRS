from models import db
from datetime import datetime


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(300))
    status = db.Column(db.String(50), default="Pending")  # Pending, In Progress, Rescued
    is_rescued = db.Column(db.Boolean, default=False)  # Toggle status - visible only to rescuers
    priority = db.Column(db.String(20), default="Medium")  # Low, Medium, High
    
    # Rescuer information
    rescuer_id = db.Column(db.Integer, db.ForeignKey('rescuer.id'))
    rescuer_name = db.Column(db.String(100))
    rescuer_contact = db.Column(db.String(100))
    rescuer_email = db.Column(db.String(120))
    
    # Reporter information
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reporter_name = db.Column(db.String(100))
    reporter_contact = db.Column(db.String(100))
    reporter_email = db.Column(db.String(120))
    
    # Timestamps
    claimed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Report {self.id}: {self.animal_type}>"
