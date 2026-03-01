from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from functools import wraps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__)

# ==================== CONFIGURATION ====================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///resqpaws.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["SECRET_KEY"] = "your_secret_key_change_in_production"

# Email Configuration
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", True)
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "your_email@gmail.com")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", "your_password")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ==================== DATABASE & AUTH SETUP ====================
from models import db
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Import models after db initialization
from models.user import User, Rescuer, Admin
from models.report import Report

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== USER LOADERS ====================
@login_manager.user_loader
def load_user(user_id):
    # Try to load from User table first
    user = User.query.get(int(user_id))
    if user:
        return user
    # Try Rescuer
    rescuer = Rescuer.query.get(int(user_id))
    if rescuer:
        return rescuer
    # Try Admin
    admin = Admin.query.get(int(user_id))
    return admin

# ==================== DECORATORS ====================
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role != role:
                flash("You don't have permission to access this page", "error")
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==================== SEND EMAIL ====================
def send_email(recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = app.config["MAIL_USERNAME"]
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))
        
        server = smtplib.SMTP(app.config["MAIL_SERVER"], app.config["MAIL_PORT"])
        server.starttls()
        server.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ==================== AUTH ROUTES ====================
@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.role == "user":
            return redirect(url_for("user_dashboard"))
        elif current_user.role == "rescuer":
            return redirect(url_for("rescuer_dashboard"))
        elif current_user.role == "admin":
            return redirect(url_for("admin_dashboard"))
    return render_template("landing.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        full_name = request.form.get("full_name")
        phone = request.form.get("phone")
        
        # Validation
        if not email or not password or not full_name:
            flash("All fields are required", "error")
            return redirect(url_for("signup"))
        
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("signup"))
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "error")
            return redirect(url_for("signup"))
        
        # Create new user (default role: user)
        user = User(email=email, full_name=full_name, phone=phone, role="user")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("login"))
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "user")  # user, rescuer, admin
        
        user = None
        if role == "user":
            user = User.query.filter_by(email=email).first()
        elif role == "rescuer":
            user = Rescuer.query.filter_by(email=email).first()
        elif role == "admin":
            user = Admin.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        
        flash("Invalid email or password", "error")
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for("home"))

# ==================== USER ROUTES ====================
@app.route("/user/dashboard")
@login_required
@role_required("user")
def user_dashboard():
    reports = Report.query.filter_by(reporter_id=current_user.id).order_by(Report.created_at.desc()).all()
    stats = {
        "total_reports": len(reports),
        "rescued": len([r for r in reports if r.is_rescued]),
        "pending": len([r for r in reports if not r.is_rescued]),
    }
    return render_template("user/dashboard.html", reports=reports, stats=stats)

@app.route("/user/report", methods=["GET", "POST"])
@login_required
@role_required("user")
def user_report():
    if request.method == "POST":
        animal_type = request.form.get("animal_type")
        condition = request.form.get("condition")
        location = request.form.get("location")
        description = request.form.get("description")
        priority = request.form.get("priority", "Medium")
        
        latitude = None
        longitude = None
        try:
            lat_str = request.form.get("latitude", "").strip()
            lon_str = request.form.get("longitude", "").strip()
            if lat_str:
                latitude = float(lat_str)
            if lon_str:
                longitude = float(lon_str)
        except (ValueError, TypeError):
            pass

        image_path = None
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
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
            priority=priority,
            latitude=latitude,
            longitude=longitude,
            image_path=image_path,
            reporter_id=current_user.id,
            reporter_name=current_user.full_name,
            reporter_contact=current_user.phone,
            reporter_email=current_user.email,
        )

        db.session.add(new_report)
        db.session.commit()

        flash("Report submitted successfully! Rescuers will help soon.", "success")
        return redirect(url_for("user_dashboard"))

    return render_template("user/report.html")

# ==================== RESCUER ROUTES ====================
@app.route("/rescuer/dashboard")
@login_required
@role_required("rescuer")
def rescuer_dashboard():
    # Get filter parameters
    location_filter = request.args.get("location", "")
    animal_filter = request.args.get("animal_type", "")
    priority_filter = request.args.get("priority", "")
    
    # Build query
    query = Report.query.filter(Report.is_rescued == False)
    
    if location_filter:
        query = query.filter(Report.location.ilike(f"%{location_filter}%"))
    if animal_filter:
        query = query.filter(Report.animal_type.ilike(f"%{animal_filter}%"))
    if priority_filter:
        query = query.filter(Report.priority == priority_filter)
    
    pending_reports = query.order_by(Report.created_at.desc()).all()
    claimed_reports = Report.query.filter_by(rescuer_id=current_user.id).order_by(Report.claimed_at.desc()).all()
    
    stats = {
        "pending": len(pending_reports),
        "claimed": len(claimed_reports),
        "rescued": current_user.animals_rescued,
    }
    
    return render_template("rescuer/dashboard.html", 
                         pending_reports=pending_reports,
                         claimed_reports=claimed_reports,
                         stats=stats)

@app.route("/rescuer/claim/<int:report_id>", methods=["POST"])
@login_required
@role_required("rescuer")
def claim_rescue(report_id):
    report = Report.query.get_or_404(report_id)
    
    if report.rescuer_id is not None:
        flash("This animal has already been claimed", "error")
        return redirect(url_for("rescuer_dashboard"))
    
    report.rescuer_id = current_user.id
    report.rescuer_name = current_user.full_name
    report.rescuer_contact = current_user.phone
    report.rescuer_email = current_user.email
    report.status = "In Progress"
    report.claimed_at = datetime.utcnow()
    report.updated_at = datetime.utcnow()
    
    db.session.commit()
    flash("Animal claimed successfully!", "success")
    return redirect(url_for("rescuer_dashboard"))

@app.route("/rescuer/update-status/<int:report_id>", methods=["POST"])
@login_required
@role_required("rescuer")
def update_rescue_status(report_id):
    report = Report.query.get_or_404(report_id)
    
    if report.rescuer_id != current_user.id:
        flash("You can only update your claimed animals", "error")
        return redirect(url_for("rescuer_dashboard"))
    
    is_rescued = request.form.get("is_rescued") == "true"
    
    if is_rescued and not report.is_rescued:
        report.is_rescued = True
        report.status = "Rescued"
        report.completed_at = datetime.utcnow()
        current_user.animals_rescued += 1
        
        # Send email to reporter
        email_body = f"""
        <h2>Great News! 🎉</h2>
        <p>Dear {report.reporter_name},</p>
        <p>We have wonderful news! The animal you reported has been successfully rescued!</p>
        <p><strong>Animal Details:</strong></p>
        <ul>
            <li>Type: {report.animal_type}</li>
            <li>Condition: {report.condition}</li>
            <li>Location: {report.location}</li>
        </ul>
        <p><strong>Rescued By:</strong> {current_user.full_name}</p>
        <p><strong>Rescuer Contact:</strong> {current_user.phone}</p>
        <p>Thank you for your immediate reporting and assistance in saving this precious life! 🐾</p>
        <p>Best regards,<br>ResQPaws Team</p>
        """
        send_email(report.reporter_email, "Animal Rescued Successfully! 🎉", email_body)
    else:
        report.is_rescued = False
        report.status = "In Progress"
    
    report.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash("Status updated successfully!", "success")
    return redirect(url_for("rescuer_dashboard"))

@app.route("/rescuer/unclaim/<int:report_id>", methods=["POST"])
@login_required
@role_required("rescuer")
def unclaim_rescue(report_id):
    report = Report.query.get_or_404(report_id)
    
    if report.rescuer_id != current_user.id:
        flash("You can only unclaim your claimed animals", "error")
        return redirect(url_for("rescuer_dashboard"))
    
    report.rescuer_id = None
    report.rescuer_name = None
    report.rescuer_contact = None
    report.rescuer_email = None
    report.status = "Pending"
    report.claimed_at = None
    report.updated_at = datetime.utcnow()
    
    db.session.commit()
    flash("Animal released successfully!", "success")
    return redirect(url_for("rescuer_dashboard"))

# ==================== ADMIN ROUTES ====================
@app.route("/admin/dashboard")
@login_required
@role_required("admin")
def admin_dashboard():
    # Get all statistics
    total_reports = Report.query.count()
    rescued_reports = Report.query.filter_by(is_rescued=True).count()
    pending_reports = Report.query.filter_by(is_rescued=False).count()
    total_rescuers = Rescuer.query.count()
    
    # Get rescuers with stats
    rescuers = Rescuer.query.all()
    rescuer_stats = []
    for rescuer in rescuers:
        claimed_reports = Report.query.filter_by(rescuer_id=rescuer.id).count()
        rescued = Report.query.filter_by(rescuer_id=rescuer.id, is_rescued=True).count()
        rescuer_stats.append({
            "id": rescuer.id,
            "name": rescuer.full_name,
            "email": rescuer.email,
            "phone": rescuer.phone,
            "animals_rescued": rescuer.animals_rescued,
            "claimed": claimed_reports,
            "rescued": rescued,
            "rating": rescuer.rating
        })
    
    # Get animal type statistics
    animal_stats = {}
    all_reports = Report.query.all()
    for report in all_reports:
        animal_type = report.animal_type
        if animal_type not in animal_stats:
            animal_stats[animal_type] = {"total": 0, "rescued": 0}
        animal_stats[animal_type]["total"] += 1
        if report.is_rescued:
            animal_stats[animal_type]["rescued"] += 1
    
    # Get priority statistics
    priority_stats = {}
    for report in all_reports:
        priority = report.priority
        if priority not in priority_stats:
            priority_stats[priority] = {"total": 0, "rescued": 0}
        priority_stats[priority]["total"] += 1
        if report.is_rescued:
            priority_stats[priority]["rescued"] += 1
    
    stats = {
        "total_reports": total_reports,
        "rescued_reports": rescued_reports,
        "pending_reports": pending_reports,
        "total_rescuers": total_rescuers,
        "rescue_rate": (rescued_reports / total_reports * 100) if total_reports > 0 else 0
    }
    
    return render_template("admin/dashboard.html", 
                         stats=stats,
                         rescuer_stats=rescuer_stats,
                         animal_stats=animal_stats,
                         priority_stats=priority_stats,
                         all_reports=all_reports)

@app.route("/admin/add-rescuer", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_rescuer():
    if request.method == "POST":
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        phone = request.form.get("phone")
        password = request.form.get("password", "default_password_123")
        
        if Rescuer.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return redirect(url_for("add_rescuer"))
        
        rescuer = Rescuer(
            email=email,
            full_name=full_name,
            phone=phone,
            role="rescuer"
        )
        rescuer.set_password(password)
        db.session.add(rescuer)
        db.session.commit()
        
        # Send email with credentials
        email_body = f"""
        <h2>Welcome to ResQPaws! 🐾</h2>
        <p>Dear {full_name},</p>
        <p>You have been added as a rescuer in the ResQPaws system.</p>
        <p><strong>Login Credentials:</strong></p>
        <ul>
            <li>Email: {email}</li>
            <li>Password: {password}</li>
        </ul>
        <p>Please login and update your password immediately for security.</p>
        <p>Start helping animals in need!</p>
        <p>Best regards,<br>ResQPaws Admin Team</p>
        """
        send_email(email, "Welcome to ResQPaws Rescuer Portal", email_body)
        
        flash("Rescuer added successfully!", "success")
        return redirect(url_for("admin_dashboard"))
    
    return render_template("admin/add_rescuer.html")

@app.route("/admin/rescuers")
@login_required
@role_required("admin")
def manage_rescuers():
    rescuers = Rescuer.query.all()
    return render_template("admin/manage_rescuers.html", rescuers=rescuers)

@app.route("/admin/reports")
@login_required
@role_required("admin")
def view_all_reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template("admin/view_reports.html", reports=reports)

# ==================== API ROUTES ====================
@app.route("/api/stats")
@login_required
@role_required("admin")
def get_stats():
    all_reports = Report.query.all()
    
    # Timeline data for line chart
    timeline = {}
    for report in all_reports:
        date = report.created_at.strftime("%Y-%m-%d")
        if date not in timeline:
            timeline[date] = {"reports": 0, "rescued": 0}
        timeline[date]["reports"] += 1
        if report.is_rescued:
            timeline[date]["rescued"] += 1
    
    return jsonify({
        "timeline": timeline,
    })

# ==================== INITIALIZE DB ====================
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
