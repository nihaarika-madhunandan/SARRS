# ResQPaws - Animal Rescue System

A modern Flask-based web application for reporting injured stray animals with real-time location tracking and image upload capabilities.

## 🎯 Features

### 1. **Modern UI/UX Design** ✨
- Clean, responsive interface with gradient designs
- Mobile-friendly layout that works on all devices
- Smooth animations and transitions
- Dark mode compatible color scheme
- Enhanced visual hierarchy

### 2. **Image Upload Functionality** 📸
- Upload animal photos in multiple formats (JPG, PNG, GIF, WebP)
- Real-time image preview before submission
- Images stored locally in `static/uploads/` directory
- Automatic filename timestamping to prevent conflicts
- Maximum file size: 16MB

### 3. **Live Location Feature** 📍
- Geolocation API integration using browser GPS
- Real-time coordinates capture (latitude, longitude)
- Automatic address lookup using OpenStreetMap Nominatim API
- Location accuracy information
- Google Maps integration for viewing report locations
- Fallback to manual location entry

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Flask
- Flask-SQLAlchemy
- werkzeug

### Installation

```bash
# Install dependencies
pip install flask flask-sqlalchemy pillow

# Run the application
python app.py
```

The application will start at `http://localhost:5000`

## 📁 Project Structure

```
SARRS/
├── app.py                    # Main Flask application
├── models/
│   └── report.py            # Database models
├── templates/
│   ├── index.html           # Home page
│   ├── report.html          # Report form page
│   └── dashboard.html       # Dashboard page
├── static/
│   ├── css/
│   │   └── style.css        # Modern CSS styling
│   └── uploads/             # User uploaded images
├── database/
│   └── db.sqlite3           # SQLite database
└── .gitignore               # Git ignore rules
```

## 🎨 Design Improvements

### Color Scheme
- **Primary**: Red/Coral (#ff6b6b) - Brand color
- **Secondary**: Teal (#4ecdc4) - Accent color
- **Success**: Green (#55efc4)
- **Warning**: Yellow (#ffeaa7)
- **Danger**: Orange (#fab1a0)

### Responsive Breakpoints
- Desktop: 1200px max width
- Tablet: 768px
- Mobile: 480px

## 💾 Database Schema

### Report Model
```python
- id: Primary Key
- animal_type: String (100)
- condition: String (200)
- location: String (300)
- latitude: Float (optional)
- longitude: Float (optional)
- description: Text
- image_path: String (path to uploaded image)
- status: String (Pending, In Progress, Rescued)
- created_at: DateTime
```

## 🌐 API Integration

### Geolocation
- Uses HTML5 Geolocation API
- Browser permission required
- Requires HTTPS in production

### Address Lookup
- OpenStreetMap Nominatim API (free, no API key needed)
- Converts coordinates to address
- Fallback to coordinates if address lookup fails

### Maps
- Google Maps integration for viewing report locations
- Dynamic map links generated from latitude/longitude

## 📱 Features by Page

### Home Page
- Hero section with call-to-action buttons
- Features showcase
- Navigation to report or dashboard

### Report Form Page
- Animal type input
- Condition description
- Live location button with GPS tracking
- Image upload with preview
- Location accuracy info display
- Form validation

### Dashboard Page
- Card-based layout with images
- Table view option
- Search functionality
- Status badges (Pending, In Progress, Rescued)
- Location links to Google Maps
- Timestamp display

## 🔒 Security Features

- File upload validation (allowed extensions)
- Secure filename sanitization
- File size limits (16MB max)
- SQL injection prevention via SQLAlchemy ORM
- CSRF protection ready

## 🚀 Future Enhancements

- User authentication system
- Real-time notifications
- Admin dashboard for status updates
- Email alerts
- Mobile app version
- Rescue team assignment system
- Social sharing integration

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues or questions, please contact the ResQPaws team.

---

**Built with ❤️ for animal rescue**
