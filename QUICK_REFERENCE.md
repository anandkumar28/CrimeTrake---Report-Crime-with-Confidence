# ⚡ Quick Reference Guide - CrimeTrake

Essential commands and information for CrimeTrake project.

---

## 🚀 Quick Start Commands

### First Time Setup
```bash
# 1. Extract ZIP file
# 2. Open terminal in project folder

# 3. Create virtual environment
python -m venv venv

# 4. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Copy environment file
cp .env.example .env
# Edit .env with your settings

# 7. Run migrations
python manage.py makemigrations
python manage.py migrate

# 8. Create admin account
python manage.py createsuperuser

# 9. Start server
python manage.py runserver
```

### Daily Usage
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Start server
python manage.py runserver

# Access at http://localhost:8000
```

---

## 📁 Project URLs

| Page | URL | Access |
|------|-----|--------|
| **Homepage** | http://localhost:8000 | Everyone |
| **Login** | http://localhost:8000/accounts/login/ | Everyone |
| **Register Citizen** | http://localhost:8000/accounts/register/citizen/ | Everyone |
| **Register Police** | http://localhost:8000/accounts/register/police/ | Everyone |
| **Admin Panel** | http://localhost:8000/admin/ | Admin only |
| **Citizen Dashboard** | http://localhost:8000/dashboard/citizen/ | Citizens |
| **Police Dashboard** | http://localhost:8000/dashboard/police/ | Police |
| **Admin Dashboard** | http://localhost:8000/dashboard/admin/ | Admin |
| **Report Crime** | http://localhost:8000/crimes/report/ | Citizens |
| **Crime Map** | http://localhost:8000/dashboard/map/ | Police/Admin |
| **Analytics** | http://localhost:8000/dashboard/analytics/ | Police/Admin |

---

## 🔑 Default Credentials

After running `createsuperuser`, you can create test accounts:

### Admin Account
- Username: (you create this)
- Password: (you create this)
- Access: Full system access

### Test Citizen
Create via registration form or Django shell

### Test Police Officer
1. Register as police officer
2. Login to admin panel
3. Go to Users → Find the police user
4. Check "is_verified" checkbox
5. Save

---

## 🛠️ Common Django Commands

```bash
# Database
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply migrations
python manage.py dbshell         # Open database shell

# User Management
python manage.py createsuperuser # Create admin
python manage.py changepassword username  # Change password

# Server
python manage.py runserver       # Start dev server
python manage.py runserver 8080  # Custom port
python manage.py runserver 0.0.0.0:8000  # Network access

# Static Files
python manage.py collectstatic   # Collect static files

# Shell
python manage.py shell           # Django Python shell

# Testing
python manage.py test            # Run tests
python manage.py test accounts   # Test specific app

# Cleanup
python manage.py flush           # Clear database
```

---

## 📝 Environment Variables (.env)

```env
# Required
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (Optional but recommended)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Google Maps (Optional but recommended)
GOOGLE_MAPS_API_KEY=your-api-key
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Database Issues
```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Virtual Environment Not Activating
```bash
# Windows
python -m venv venv --clear
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv --clear
source venv/bin/activate
```

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Database Models Quick Reference

### User
- Roles: CITIZEN, POLICE, ADMIN
- Fields: username, email, phone, address

### Crime
- Fields: case_id, title, description, location
- Status: FILED, UNDER_INVESTIGATION, CASE_CLOSED
- Priority: LOW, MEDIUM, HIGH, CRITICAL

### Evidence
- Fields: file, evidence_type, description
- Types: IMAGE, VIDEO, DOCUMENT

### Suspect
- Fields: name, description, photo
- Face recognition data stored

---

## 🎨 Customization

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary: #FF6B35;     /* Main color */
    --secondary: #004E89;   /* Secondary color */
    --accent: #FFD23F;      /* Accent color */
}
```

### Change Site Name
Edit `templates/base.html`:
```html
<span>CrimeTrake</span>  <!-- Change this -->
```

---

## 📦 Project Structure

```
crimetrake_project/
├── accounts/        # User management
├── crimes/          # Crime reporting
├── dashboard/       # Dashboards
├── ml_engine/       # AI/ML features
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── media/           # User uploads
└── manage.py        # Django manager
```

---

## 🔐 User Roles & Permissions

### CITIZEN
- ✅ Report crimes
- ✅ Upload evidence
- ✅ Track own cases
- ❌ Update case status
- ❌ View other users' cases

### POLICE
- ✅ View assigned cases
- ✅ Update case status
- ✅ Add suspects
- ✅ View crime map
- ✅ View analytics
- ❌ Delete cases
- ❌ Manage users

### ADMIN
- ✅ Full system access
- ✅ Manage all users
- ✅ Verify police officers
- ✅ Assign cases
- ✅ View all statistics

---

## 📈 Performance Tips

### For Development
```python
# settings.py
DEBUG = True
```

### For Production
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Use PostgreSQL instead of SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ... config
    }
}
```

---

## 🧪 Testing Features

### Test Crime Classification
```python
python manage.py shell

from ml_engine.classifier import classify_crime

# Test
category, confidence = classify_crime("Someone stole my bike")
print(f"Category: {category}, Confidence: {confidence}")
```

### Test Face Recognition
```python
from ml_engine.face_recognition_engine import detect_faces

# Provide path to image
faces, encodings = detect_faces('/path/to/image.jpg')
print(f"Detected {faces} faces")
```

---

## 📚 Documentation Files

- **README.md** - Full project documentation
- **SETUP.md** - Detailed setup guide
- **EXTERNAL_SERVICES_SETUP.md** - Google Maps & Gmail setup
- **PROJECT_STRUCTURE.txt** - File organization
- **This file** - Quick reference

---

## 🆘 Get Help

1. Check README.md
2. Check SETUP.md
3. Check error messages
4. Search Google with error message
5. Check Django documentation

---

## ✅ Pre-Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS
- [ ] Use strong SECRET_KEY
- [ ] Set up PostgreSQL
- [ ] Configure email
- [ ] Add Google Maps key
- [ ] Run collectstatic
- [ ] Test all features
- [ ] Create backup

---

**Happy Coding! 🚀**
