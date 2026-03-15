# 🚀 Vercel Deployment Guide - Complete Setup

## ✅ What Was Fixed

Your project wasn't deploying because three critical files were missing:

### 1. **vercel.json** - Build Configuration
- Tells Vercel HOW to build your Flask app
- Specifies Python builder (`@vercel/python`)
- Routes all requests to the API entry point

### 2. **api/index.py** - Entry Point
- Vercel requires serverless functions in the `/api` directory
- This file imports and exposes your Flask app
- Vercel runs this instead of `app.py` directly

### 3. **gunicorn in requirements.txt**
- Production-grade WSGI server
- Required for Vercel's Python runtime

---

## 🔧 Vercel Dashboard Setup (IMPORTANT!)

After pushing to GitHub, follow these steps in Vercel:

### Step 1: Environment Variables
1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Add these variables (copy from your `.env` file):
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   SECRET_KEY=your_production_secret_key
   ```

3. ⚠️ **CRITICAL FOR MONGODB**: Whitelist Vercel IPs
   - Go to MongoDB Atlas → Network Access
   - Add IP: `0.0.0.0/0` (allows all IPs from Vercel)
   - Or add specific Vercel IP ranges

### Step 2: Deployment Branch
1. Go to **Settings** → **Git** 
2. Ensure **Production** branch is set to `main`
3. Enable **Automatic deployments**

### Step 3: Redeploy
1. Go to **Deployments** tab
2. Click the three dots (...) on the latest deployment
3. Select **Redeploy** to trigger a new build
4. Watch the build logs for errors

---

## 🐛 Troubleshooting Build Failures

### Check Build Logs
1. Go to **Vercel Dashboard** → **Deployments**
2. Click on a failed deployment
3. Go to **Build Logs** tab
4. Look for error messages

### Common Issues & Fixes

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'app'` | Check that `api/index.py` imports correctly |
| `MongoDB connection timeout` | Whitelist 0.0.0.0/0 in MongoDB Atlas Network Access |
| `MAIL_USERNAME not set` | Add environment variables in Vercel Settings |
| `Flask app not found` | Ensure `api/index.py` exists in root directory |

### Testing Locally Before Deploy
```bash
# Install vercel CLI
npm install -g vercel

# Test locally
vercel dev

# This runs your app exactly as Vercel would
```

---

## 📋 Complete Vercel Setup Checklist

- [ ] Committed and pushed `vercel.json` to GitHub
- [ ] Committed and pushed `api/index.py` to GitHub
- [ ] Updated `requirements.txt` with gunicorn
- [ ] Added all environment variables in Vercel Settings
- [ ] Whitelisted `0.0.0.0/0` in MongoDB Atlas Network Access
- [ ] Enabled automatic deployments in Vercel
- [ ] Triggered a redeploy from Vercel dashboard
- [ ] Checked build logs for errors
- [ ] App is now running on Vercel domain

---

## 🔗 File Structure (Vercel expects this)
```
project-root/
├── vercel.json          ✅ NEW
├── api/
│   └── index.py         ✅ NEW
├── app.py               (imported by api/index.py)
├── models/
├── templates/
├── static/
└── requirements.txt     (updated with gunicorn)
```

---

## ⚡ After First Successful Deploy

1. **Monitor Performance**: Go to **Analytics** tab in Vercel
2. **Check Logs**: Go to **Logs** tab for runtime errors
3. **Set Custom Domain**: In Settings → Domains
4. **Enable Auto-scaling**: Already enabled by default

---

## 🚨 If Still Not Working

1. Open Vercel Dashboard
2. Go to **Deployments** 
3. Find the latest deployment
4. Click it and scroll to **Build Logs**
5. Copy the error message
6. Check this against the troubleshooting table above

---

## 💡 Pro Tips

- Disable "Build Command" in Settings - Vercel auto-detects Flask
- Use `vercel logs` CLI command to stream real-time logs
- Every GitHub push triggers auto-deploy (if configured)
- Rollback to previous version: Deployments → click previous → Redeploy

---

**Now push these changes and your app should deploy automatically!** 🎉
