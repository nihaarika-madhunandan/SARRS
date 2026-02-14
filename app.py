from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ------------------ DATABASE CONFIG ------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reports.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------ DATABASE MODEL ------------------
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
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

        new_report = Report(
            animal_type=animal_type,
            condition=condition,
            location=location,
            description=description,
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
