# 🐾 ResQPaws - Animal Rescue Management System

A professional, full-featured web application for coordinating animal rescues with role-based user management, real-time status tracking, and comprehensive analytics.

## ✨ Features

### 🔐 Multi-Role Authentication
- **Users/Reporters**: Submit injured animal reports with GPS location and images
- **Rescuers**: Discover, claim, and complete animal rescues
- **Admins**: Manage team, view analytics, track statistics

### 📱 User Dashboards
- Personal rescue reports with status tracking
- Real-time animal discovery and search
- Performance analytics and statistics
- Email notifications for rescue updates

### 📊 Advanced Analytics
- Rescue success rate visualization
- Animal type distribution charts
- Priority level breakdown
- Top-performing rescuers ranking
- System-wide statistics

### 🎨 Professional UI
- Modern Ant Design components
- Fully responsive (mobile, tablet, desktop)
- Beautiful gradients and animations
- Intuitive navigation
- Accessibility-first design

## 🚀 Quick Start

### Option 1: PowerShell (Recommended)
```powershell
cd e:\Projects\SARRS
.\start.ps1 -Install -CleanDB
```

### Option 2: Command Prompt
```cmd
cd e:\Projects\SARRS
start.bat
```

### Option 3: Manual Setup
```bash
# Navigate to project
cd e:\Projects\SARRS

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade -r requirements.txt

# Start application
python app.py
```

Then open **http://localhost:5000** in your browser.

## 📝 Test Accounts

### Create via Signup (User Account)
1. Go to http://localhost:5000/signup
2. Fill in details (default role: "user")
3. Login at http://localhost:5000/login with "User" role

### Admin Setup (First Time)
**Admin accounts must be created manually in database:**
```python
from app import app, db
from models.user import Admin
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = Admin(
        email="admin@example.com",
        password_hash=generate_password_hash("password123"),
        full_name="Admin User"
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")
```

## 🔄 User Workflows

### User (Reporter) Flow
```
Sign Up → Login → Create Report → Submit → Track Status → Receive Email
```

### Rescuer Flow
```
Login → View Pending → Search & Filter → Claim → Mark Rescued → Email Sent
```

### Admin Flow
```
Login → Dashboard → View Analytics → Add Rescuers → Manage Team
```

## 📁 Project Structure

```
ResQPaws/
├── app.py                          # Flask application (360+ lines)
├── requirements.txt                # Python dependencies
├── .env.template                   # Email configuration template
│
├── models/
│   ├── user.py                     # User, Rescuer, Admin models
│   └── report.py                   # Report model with relationships
│
├── templates/                      # HTML templates
│   ├── landing.html               # Homepage
│   ├── signup.html / login.html    # Authentication
│   ├── user/
│   │   ├── dashboard.html         # User reports
│   │   └── report.html            # Create report
│   ├── rescuer/
│   │   └── dashboard.html         # Rescuer portal
│   └── admin/
│       ├── dashboard.html         # Analytics
│       ├── add_rescuer.html       # Add rescuer
│       ├── manage_rescuers.html   # Manage team
│       └── view_reports.html      # All reports
│
├── static/
│   ├── css/
│   │   ├── antd-style.css        # Design system
│   │   ├── dashboard.css         # Layouts
│   │   └── style.css             # Custom styles
│   └── uploads/                   # Animal images
│
├── instance/
│   └── resqpaws.db               # SQLite database
│
└── scripts/
    └── seed_demo_data.py         # (Optional) Demo data
```

## ⚙️ Configuration

### 1. Setup Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Email (Optional)
Copy `.env.template` to `.env` and add your email:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

For Gmail: Generate App Password at https://myaccount.google.com/apppasswords

### 4. Run Application
```bash
python app.py
```

## 🗄️ Database Schema

### User Table
```python
User {
    id, email, password_hash, full_name, phone, 
    role="user", created_at
}
```

### Rescuer Table
```python
Rescuer {
    id, email, password_hash, full_name, phone,
    experience, location, animals_rescued, rating,
    role="rescuer", created_at
}
```

### Report Table
```python
Report {
    id, animal_type, condition, location, latitude, longitude,
    description, image_path, status, is_rescued, priority,
    rescuer_id, rescuer_name, rescuer_contact, rescuer_email,
    reporter_id, reporter_name, reporter_contact, reporter_email,
    claimed_at, completed_at, created_at, updated_at
}
```

## 🔗 API Routes

### Authentication
- `POST /signup` - Register new user
- `POST /login` - Login with role selection
- `GET /logout` - Logout

### User Routes
- `GET /user/dashboard` - View personal reports
- `GET/POST /user/report` - Create new report
- `GET /api/stats` - Get statistics

### Rescuer Routes
- `GET /rescuer/dashboard` - View available animals
- `POST /rescuer/claim/<id>` - Claim animal
- `POST /rescuer/update-status/<id>` - Mark as rescued
- `POST /rescuer/unclaim/<id>` - Release animal

### Admin Routes
- `GET /admin/dashboard` - Analytics dashboard
- `GET/POST /admin/add-rescuer` - Add new rescuer
- `GET /admin/rescuers` - List all rescuers
- `GET /admin/reports` - View all reports

## 🎨 Design Features

### Professional UI Components
- Gradient backgrounds and color scheme
- Smooth hover effects and transitions
- Status badges and priority indicators
- Empty state illustrations
- Loading states and spinners
- Mobile-responsive grid layouts

### Responsive Breakpoints
- Desktop: 1024px+ (full layout)
- Tablet: 768px-1023px (adjusted spacing)
- Mobile: <768px (stacked layout, horizontal nav)

### Color Palette (Ant Design)
- Primary: #667eea (purple-blue)
- Secondary: #764ba2 (purple)
- Success: #52c41a (green)
- Danger: #f5222d (red)
- Warning: #faad14 (orange)

## 🐛 Troubleshooting

### Issue: SQLAlchemy TypeError on startup
```
AssertionError: Class directly inherits TypingOnly
```
**Solution:** Update packages
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Change port in app.py or kill existing process
```bash
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: Database errors
**Solution:** Delete database and restart
```bash
rm instance/resqpaws.db
python app.py
```

### Issue: Email not sending
**Solution:** Configure .env file with SMTP credentials

## 📚 Documentation Files

- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Complete feature documentation
- **[STATUS_CHECKLIST.md](STATUS_CHECKLIST.md)** - Implementation status and testing checklist
- **[.env.template](.env.template)** - Email configuration template

## 🔐 Security Features

- **Password Hashing**: Werkzeug generate_password_hash
- **Session Management**: Flask-Login with secure cookies
- **Role-Based Access**: Decorator-based authorization
- **CSRF Protection**: Flask default protection
- **Input Validation**: Form validation on backend

## 🚀 Production Deployment

### Recommended Changes
1. Use PostgreSQL instead of SQLite
2. Set `FLASK_ENV=production`
3. Change `SECRET_KEY` to random string
4. Use Gunicorn for production server
5. Setup nginx reverse proxy
6. Enable HTTPS with SSL certificate
7. Configure proper logging
8. Setup monitoring and alerts

### Deployment Options
- Heroku: `git push heroku main`
- AWS: EC2 + RDS
- Google Cloud: App Engine + Cloud SQL
- DigitalOcean: Droplet + Managed Database
- Docker: Containerize with Docker

## 🤝 Contributing

To add features:
1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

This project is provided as-is for educational and development purposes.

## 👨‍💻 Technical Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Flask | 2.3.3 |
| ORM | SQLAlchemy | 2.1.0 |
| Authentication | Flask-Login | 0.6.2 |
| Database | SQLite/PostgreSQL | - |
| Frontend | HTML5/CSS3/JS | - |
| UI Framework | Ant Design | - |
| Charts | Chart.js | 3.9.1 |
| Icons | Font Awesome | 6.4.0 |

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review documentation files
3. Check Flask/SQLAlchemy logs
4. Open browser console (F12) for frontend errors

## ✅ Completion Status

- ✅ Authentication system (100%)
- ✅ User portal (100%)
- ✅ Rescuer portal (100%)
- ✅ Admin dashboard (100%)
- ✅ Database models (100%)
- ✅ Email notifications (100%)
- ✅ Professional UI/UX (100%)
- ✅ Responsive design (100%)
- ⏳ Production deployment (0%)

---

**Version:** 1.0.0  
**Status:** Feature Complete - Ready for Testing ✅  
**Last Updated:** February 27, 2026

**Next Steps:** Run `.\start.ps1` to launch the application!
