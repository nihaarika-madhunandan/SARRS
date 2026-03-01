# 🚀 QUICK START GUIDE - ResQPaws 2.0

## ⚡ 5 Minute Setup (Windows/Mac/Linux)

### 1️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Get MongoDB Connection String

**Option A - Cloud (Easiest):**
- Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Sign up (free)
- Create a cluster
- Copy connection string

**Option B - Local:**
- Install [MongoDB Community](https://www.mongodb.com/try/download/community)
- Start: `mongod` (Windows) or `brew services start mongodb-community` (Mac)
- Use: `mongodb://localhost:27017/sarrs`

### 3️⃣ Create `.env` File
Create a file named `.env` in project root:

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/sarrs?retryWrites=true&w=majority
```

Replace with your actual MongoDB connection string.

### 4️⃣ Initialize Demo Data
```bash
python init_demo_data.py
```

### 5️⃣ Start Application
```bash
python app.py
```

**Open**: http://localhost:5000

## 🔐 Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@resqpaws.com | Admin@12345 |
| Rescuer | john.rescuer@resqpaws.com | Rescuer@12345 |
| User | user1@resqpaws.com | User@12345 |

**💡 TIP**: Just enter email + password. Role is auto-detected!

## 🎯 What to Try First

### As Admin
1. Login → See dashboard with statistics
2. Click "Recruit Rescuer" → Add new rescuer
3. View team performance metrics
4. Monitor all animal rescues

### As Rescuer
1. Login → See pending animal cases
2. Click "CLAIM" on any animal
3. Track it in "MY OPERATIONS" tab
4. Mark as rescued when done

### As User
1. Signup at signup page
2. Click "New Report" 
3. Select animal type, location, photo
4. Submit and watch rescuer progress

## 🐛 Troubleshooting

### "MongoDB Connection Error"
```
✅ Solution: Check .env file has correct MongoDB URI
           Make sure MongoDB is running
```

### "Email not registered"
```
✅ Solution: This email isn't in demo data
           Run: python init_demo_data.py again
           Or signup as new user
```

### Port 5000 already in use
```
✅ Solution: Edit app.py last line to: app.run(debug=True, port=5001)
```

## 📚 Full Documentation

See [MONGODB_SETUP.md](MONGODB_SETUP.md) for complete setup guide with:
- Database schema details
- Authentication flow
- Feature overview by role
- Deployment instructions

## ✨ Features Overview

✅ **Auto-detecting Login** - No more role selectors!
✅ **MongoDB** - Scalable NoSQL database
✅ **Admin Dashboard** - Real-time analytics & team management
✅ **Rescuer Mission Control** - Claim and track rescues
✅ **Professional UI** - Modern dark design
✅ **Email Notifications** - Alerts when animals are rescued
✅ **Image Uploads** - Add pictures of animals
✅ **GPS Mapping** - View animal locations

## 🚀 Next Steps

After first login:
1. **Explore each dashboard** - Get familiar with the interface
2. **Try all features** - Submit reports, claim rescues
3. **Check database** - View real data in MongoDB
4. **Customize** - Add your own features!

---

**Questions?** See MONGODB_SETUP.md for detailed docs!
