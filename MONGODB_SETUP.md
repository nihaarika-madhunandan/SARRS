# ResQPaws - MongoDB Restructure Guide

## Overview
This project has been completely restructured to use **MongoDB** instead of SQLite, with improved authentication and professional role-based dashboards.

## Key Changes

### 1. **MongoDB Integration**
- ✅ Migrated from SQLAlchemy/SQLite to PyMongo
- ✅ Removed all SQL database dependencies
- ✅ Collections: `users`, `rescuers`, `admins`, `reports`

### 2. **Improved Authentication**
- ✅ **Auto-Detection**: Login with email + password, role is automatically detected
- ✅ Removed role selector from login page
- ✅ Seamless redirect to appropriate dashboard (User/Rescuer/Admin)

### 3. **Professional Dashboard Redesigns**
- ✅ **Admin Dashboard**: Command center with analytics, team management, and statistics
- ✅ **Rescuer Dashboard**: Clean mission control interface with real-time status tracking
- ✅ Modern UI/UX with role-specific features

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up MongoDB Connection

#### Option A: MongoDB Atlas (Cloud - Recommended)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a new project and cluster
4. Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/dbname?retryWrites=true&w=majority`)
5. Create a `.env` file in your project root:

```bash
cp .env.example .env
```

6. Edit `.env` and add your MongoDB URI:

```
MONGODB_URI=mongodb+srv://your_username:your_password@your_cluster.mongodb.net/sarrs?retryWrites=true&w=majority
```

#### Option B: Local MongoDB
1. Install MongoDB Community Edition: https://docs.mongodb.com/manual/installation/
2. Start MongoDB:
   - **Windows**: `mongod` (in MongoDB bin folder)
   - **Mac**: `brew services start mongodb-community`
   - **Linux**: `sudo systemctl start mongod`
3. Create `.env`:

```
MONGODB_URI=mongodb://localhost:27017/sarrs
```

### Step 3: Initialize Demo Data

Run the demo data initialization script:

```bash
python init_demo_data.py
```

This will create:
- ✅ 1 Admin account
- ✅ 5 Rescuer accounts
- ✅ 3 User accounts
- ✅ 8 Sample animal rescue reports

### Step 4: Run the Application

```bash
python app.py
```

Access the application at `http://localhost:5000`

## Demo Login Credentials

### Admin
```
Email: admin@resqpaws.com
Password: Admin@12345
```

### Rescuer
```
Email: john.rescuer@resqpaws.com
Password: Rescuer@12345
```

### User (Reporter)
```
Email: user1@resqpaws.com
Password: User@12345
```

**Note**: The role is automatically detected during login. Just enter email and password!

## Project Structure

```
SARRS/
├── app.py                    # Main Flask application
├── models/
│   ├── __init__.py          # MongoDB connection setup
│   ├── user.py              # User, Rescuer, Admin models
│   └── report.py            # Report model
├── templates/
│   ├── login.html           # Improved login page (no role selector)
│   ├── signup.html          # User registration
│   ├── admin/
│   │   ├── dashboard.html   # Admin command center
│   │   ├── add_rescuer.html
│   │   ├── manage_rescuers.html
│   │   └── view_reports.html
│   ├── rescuer/
│   │   └── dashboard.html   # Professional rescuer dashboard
│   └── user/
│       ├── dashboard.html   # User dashboard
│       └── report.html      # Report creation form
├── static/
│   ├── css/
│   │   └── *.css           # Stylesheets
│   └── uploads/            # User-uploaded images
├── init_demo_data.py        # Demo data initialization
├── .env.example             # Environment template
└── requirements.txt         # Python dependencies
```

## Key Features by Role

### 👤 Admin Account
- 📊 Command center dashboard with real-time analytics
- 📈 Statistics on rescued animals, pending cases, success rates
- 🧑‍💼 Manage rescuers (add, view, edit)
- 📋 View all reports and cases
- 🎯 Monitor rescuer performance and ratings

### 🚑 Rescuer Account
- 🆘 See pending animals needing rescue
- ✅ Claim rescue missions
- 🚀 Track active operations
- 📝 Mark animals as rescued
- 📍 View GPS coordinates and maps
- 🏆 Track personal rescue statistics

### 👥 User Account
- 📝 Submit animal rescue reports
- 🐾 Upload pictures of animals
- 📍 Add location and GPS coordinates
- 📊 Track status of submitted reports
- 💬 View rescue details and rescuer info

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password_hash": "hashed_password",
  "full_name": "User Name",
  "phone": "+1-555-0000",
  "role": "user",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Rescuers Collection
```json
{
  "_id": ObjectId,
  "email": "rescuer@example.com",
  "password_hash": "hashed_password",
  "full_name": "Rescuer Name",
  "phone": "+1-555-0000",
  "role": "rescuer",
  "experience": "5 years",
  "location": "Downtown",
  "animals_rescued": 25,
  "rating": 4.8,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Admins Collection
```json
{
  "_id": ObjectId,
  "email": "admin@example.com",
  "password_hash": "hashed_password",
  "full_name": "Admin Name",
  "role": "admin",
  "created_at": ISODate
}
```

### Reports Collection
```json
{
  "_id": ObjectId,
  "animal_type": "Dog",
  "condition": "Injured leg",
  "location": "Central Park",
  "latitude": 40.785,
  "longitude": -73.968,
  "description": "Found limping...",
  "image_path": "uploads/20240301_120000_dog.jpg",
  "status": "In Progress",
  "is_rescued": false,
  "priority": "High",
  "reporter_id": ObjectId,
  "reporter_name": "Alice Smith",
  "reporter_contact": "+1-555-0000",
  "reporter_email": "user@example.com",
  "rescuer_id": ObjectId,
  "rescuer_name": "John Martinez",
  "rescuer_contact": "+1-555-0000",
  "rescuer_email": "rescuer@example.com",
  "claimed_at": ISODate,
  "completed_at": ISODate,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

## Authentication Flow

1. User enters email and password on login page
2. System checks which collection contains the email:
   - First checks `admins` collection
   - Then checks `rescuers` collection
   - Finally checks `users` collection
3. Password is verified
4. User is logged in and redirected to their role-specific dashboard
5. Roles are stored in session and checked on protected routes

## Troubleshooting

### MongoDB Connection Error
```
Error: MongoDB Connection Error: [error message]
```
**Solution**: 
- Verify your `MONGODB_URI` in `.env`
- Check your MongoDB instance is running
- Ensure IP whitelist in MongoDB Atlas includes your IP

### "Email not registered"
**Solution**: 
- You must be registered in the system first
- Use demo credentials or run `init_demo_data.py`
- Sign up as a new user

### Port already in use
```
OSError: [Errno 48] Address already in use
```
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use 5001 instead of 5000
```

## Email Configuration (Optional)

To enable email notifications for rescued animals:

1. Create a Gmail app password: https://support.google.com/accounts/answer/185833
2. Update `.env`:

```
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

## Next Steps

### Customization Ideas
1. **Add more animal types** with emoji/icons
2. **Implement rating system** for rescuers
3. **Add SMS notifications** for urgent cases
4. **Create mobile app** using React Native
5. **Add AI-powered image recognition** for animal detection
6. **Implement real-time updates** with WebSockets

### Deployment
1. Deploy to Heroku, AWS, or Google Cloud
2. Set up production MongoDB instance
3. Configure proper email service (SendGrid, AWS SES)
4. Enable SSL/HTTPS
5. Set up monitoring and logging

## Support & Contributing

For issues or questions:
1. Check existing documentation
2. Review code comments
3. Check MongoDB documentation: https://docs.mongodb.com
4. Check Flask documentation: https://flask.palletsprojects.com

---

**Last Updated**: March 1, 2026  
**Version**: 2.0 (MongoDB Edition 
