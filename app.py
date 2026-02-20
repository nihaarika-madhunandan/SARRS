from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ------------------ DATABASE CONFIG ------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reports.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

db = SQLAlchemy(app)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------ DATABASE MODEL ------------------
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

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        animal_type = request.form.get("animal_type")
        condition = request.form.get("condition")
        location = request.form.get("location")
        description = request.form.get("description")
        latitude = request.form.get("latitude", type=float)
        longitude = request.form.get("longitude", type=float)

        image_path = None
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_")
                filename = timestamp + filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                image_path = f"uploads/{filename}"

        new_report = Report(
            animal_type=animal_type,
            condition=condition,
            location=location,
            description=description,
            latitude=latitude,
            longitude=longitude,
            image_path=image_path,
        )

        db.session.add(new_report)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("report.html")

@app.route("/dashboard")
def dashboard():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template("dashboard.html", reports=reports)

# ------------------ CREATE DB ------------------
with app.app_context():
    db.create_all()

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)
