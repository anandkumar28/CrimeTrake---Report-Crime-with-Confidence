# 🛠️ CrimeTrake Setup Guide

Complete step-by-step setup instructions for CrimeTrake project.

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Creating Sample Data](#creating-sample-data)
7. [Setting up External Services](#setting-up-external-services)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## 📦 Prerequisites

### Required Software
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **Git** - [Download](https://git-scm.com/)
- **Code Editor** - VS Code, PyCharm, or any editor

### Optional (Recommended)
- **virtualenv** - For isolated Python environment
- **PostgreSQL** - For production database
- **CMake** - Required for dlib (face recognition)

### Check Installed Versions
```bash
python --version   # Should be 3.10 or higher
pip --version
git --version
```

---

## 🚀 Local Development Setup

### Step 1: Clone the Repository
```bash
# Clone the project
git clone https://github.com/yourusername/crimetrake.git
cd crimetrake_project
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

#### Basic Installation (Without Face Recognition)
```bash
pip install Django==4.2.7
pip install pillow==10.1.0
pip install scikit-learn==1.3.2
pip install pandas==2.1.3
pip install numpy==1.26.2
```

#### Full Installation (With Face Recognition)
```bash
# Install all requirements
pip install -r requirements.txt
```

**Note**: Installing `dlib` (required for face recognition) can be tricky:

**On Windows**:
1. Install Visual Studio Build Tools
2. Or download pre-built wheel from [here](https://github.com/sachadee/Dlib)

**On macOS**:
```bash
brew install cmake
pip install dlib
```

**On Linux (Ubuntu)**:
```bash
sudo apt-get install build-essential cmake
pip install dlib
```

If face recognition fails, the app will work without it (with warning messages).

---

## ⚙️ Configuration

### Step 1: Create Environment File
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

### Step 2: Configure .env File
```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (For PostgreSQL in production)
DB_NAME=crimetrake_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Gmail SMTP)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# For production
DJANGO_ENV=development
```

### Step 3: Generate Secret Key
```python
# Run in Python shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and paste it in `.env` file as `SECRET_KEY`.

---

## 🗄️ Database Setup

### Using SQLite (Development - Default)
No additional setup required. Django will create `db.sqlite3` automatically.

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Using PostgreSQL (Production - Recommended)

#### Install PostgreSQL
```bash
# On Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# On macOS
brew install postgresql

# On Windows
# Download installer from postgresql.org
```

#### Create Database
```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE crimetrake_db;
CREATE USER crimetrake_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE crimetrake_db TO crimetrake_user;
\q
```

#### Update settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crimetrake_db',
        'USER': 'crimetrake_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Install psycopg2
```bash
pip install psycopg2-binary
```

#### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 👤 Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Fill in the details:
- Username: `admin`
- Email: `admin@crimetrake.com`
- Password: (create a strong password)

---

## 🏃 Running the Application

### Start Development Server
```bash
python manage.py runserver
```

The application will be available at:
- **Frontend**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### Running on Custom Port
```bash
python manage.py runserver 8080
```

### Running on Network (accessible from other devices)
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 📊 Creating Sample Data

### Option 1: Using Django Shell
```bash
python manage.py shell
```

```python
from accounts.models import User
from crimes.models import Crime
from datetime import datetime

# Create citizen
citizen = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='password123',
    role='CITIZEN',
    first_name='John',
    last_name='Doe',
    phone='1234567890',
    address='123 Main St'
)

# Create police officer
police = User.objects.create_user(
    username='officer_smith',
    email='smith@police.com',
    password='password123',
    role='POLICE',
    first_name='Sarah',
    last_name='Smith',
    badge_number='P1234',
    department='Central Police Station',
    is_verified=True
)

# Create sample crime
crime = Crime.objects.create(
    reporter=citizen,
    crime_type='THEFT',
    title='Laptop Stolen from Car',
    description='My laptop was stolen from my parked car near the mall.',
    location='City Mall Parking Lot',
    latitude=28.6139,
    longitude=77.2090,
    incident_date=datetime.now(),
    status='FILED',
    priority='MEDIUM'
)

print(f"Created crime: {crime.case_id}")
```

### Option 2: Using Fixtures (Recommended)
```bash
# Load sample data
python manage.py loaddata sample_data.json
```

---

## 🌐 Setting up External Services

### 1. Google Maps API (FREE)

#### Get API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable **Maps JavaScript API** and **Geocoding API**
4. Create credentials (API Key)
5. Copy API key and add to `.env`:
   ```env
   GOOGLE_MAPS_API_KEY=AIzaSy...your-key-here
   ```

#### Usage
The key will be automatically used in crime map template.

### 2. Gmail SMTP (FREE)

#### Enable App Password
1. Go to Google Account settings
2. Security → 2-Step Verification (enable it)
3. App passwords → Generate new password
4. Copy password and add to `.env`:
   ```env
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=generated-app-password
   ```

#### Test Email
```python
python manage.py shell

from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email from CrimeTrake',
    'your-email@gmail.com',
    ['recipient@example.com'],
)
```

---

## 🚀 Production Deployment

### Option 1: Deploy to Render (FREE)

#### Prerequisites
- GitHub account
- Code pushed to GitHub repository

#### Steps
1. **Prepare for Production**
   ```bash
   # Update settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['your-app.onrender.com']
   
   # Add to requirements.txt
   gunicorn==21.2.0
   whitenoise==6.6.0
   psycopg2-binary==2.9.9
   ```

2. **Update settings.py for Static Files**
   ```python
   MIDDLEWARE = [
       # ... other middleware
       'whitenoise.middleware.WhiteNoiseMiddleware',
   ]
   
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

3. **Create Procfile**
   ```
   web: gunicorn crimetrake.wsgi --log-file -
   ```

4. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn crimetrake.wsgi:application`
   - Add environment variables from `.env`
   - Click "Create Web Service"

5. **Set up Database**
   - Create PostgreSQL database on Render
   - Copy database URL
   - Add to environment variables

### Option 2: Deploy to Railway (FREE $5 credit)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "No module named 'django'"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall Django
pip install Django==4.2.7
```

#### 2. "dlib installation failed"
**Solution**: App will work without face recognition. To fix:
- Windows: Download pre-built wheel
- macOS: `brew install cmake` then `pip install dlib`
- Linux: `sudo apt-get install cmake` then `pip install dlib`

#### 3. "CSRF verification failed"
**Solution**: Clear browser cache and cookies

#### 4. "Static files not loading"
```bash
python manage.py collectstatic
```

#### 5. Database migration errors
```bash
# Delete migrations (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

#### 6. Port already in use
```bash
# Kill process on port 8000
# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -ti:8000 | xargs kill -9
```

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Python Documentation](https://docs.python.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Google Maps API](https://developers.google.com/maps)

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Virtual environment activated
- [ ] All packages installed
- [ ] Database migrations completed
- [ ] Superuser created
- [ ] Development server running
- [ ] Can access admin panel
- [ ] Can register new user
- [ ] Can report crime
- [ ] Email notifications work (if configured)

---

## 📞 Need Help?

If you encounter issues:
1. Check this troubleshooting guide
2. Search [Stack Overflow](https://stackoverflow.com/)
3. Open [GitHub Issue](https://github.com/yourusername/crimetrake/issues)
4. Contact: your.email@example.com

---

**Happy Coding! 🚀**
