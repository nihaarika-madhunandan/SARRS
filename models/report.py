from app import db
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
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Report {self.id}: {self.animal_type}>"
