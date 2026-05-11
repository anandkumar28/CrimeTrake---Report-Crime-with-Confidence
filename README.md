# 🚔 CrimeTrake: Digital Crime Reporting & Investigation System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An AI-powered crime reporting and investigation management system built with Django, Machine Learning, and Face Recognition technology.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [AI/ML Features](#aiml-features)
- [Screenshots](#screenshots)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

CrimeTrake is a comprehensive digital crime reporting and investigation system designed for BTech final year projects. It enables citizens to report crimes online, police officers to manage investigations, and administrators to oversee the entire system with advanced analytics.

### Key Highlights
- **Role-Based Access Control** (Citizen, Police, Admin)
- **AI-Powered Crime Classification** using NLP
- **Face Recognition** for suspect identification
- **Real-time Crime Mapping** with GPS integration
- **Email Notifications** for case updates
- **Predictive Analytics** for crime patterns

---

## ✨ Features

### For Citizens
- ✅ Online crime reporting with evidence upload
- ✅ Anonymous reporting option
- ✅ Real-time case status tracking
- ✅ Email notifications on case updates
- ✅ GPS-enabled location capture

### For Police Officers
- ✅ Case management dashboard
- ✅ Evidence review and analysis
- ✅ Suspect management with face recognition
- ✅ Status updates and case notes
- ✅ Priority-based case filtering

### For Administrators
- ✅ Complete system oversight
- ✅ User management (verify police officers)
- ✅ Crime statistics and analytics
- ✅ Geographic crime mapping
- ✅ Monthly trend analysis

### AI/ML Features
- 🤖 **Crime Classification**: Automatic categorization using NLP
- 👤 **Face Recognition**: Match suspects with evidence photos
- 📊 **Predictive Analytics**: Identify crime patterns and hotspots
- 🗺️ **Location Analysis**: Geographic clustering of crimes

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2
- **Language**: Python 3.10+
- **Database**: SQLite (Development) / PostgreSQL (Production)

### Machine Learning
- **scikit-learn**: Crime classification
- **Pandas & NumPy**: Data processing
- **OpenCV**: Image processing
- **face_recognition**: Facial recognition

### Frontend
- **HTML5, CSS3, JavaScript**
- **Font Awesome Icons**
- **Google Fonts** (Syne, DM Sans)
- **Responsive Design**

### External APIs
- **Google Maps API**: Crime location mapping
- **Gmail SMTP**: Email notifications

---

## 📁 Project Structure

```
crimetrake_project/
│
├── crimetrake/              # Main Django project
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config
│
├── accounts/                # User management app
│   ├── models.py            # Custom User model
│   ├── views.py             # Auth views
│   ├── forms.py             # Registration forms
│   └── templates/           # Auth templates
│
├── crimes/                  # Crime reporting app
│   ├── models.py            # Crime, Evidence, Suspect models
│   ├── views.py             # Crime management views
│   ├── forms.py             # Crime forms
│   └── templates/           # Crime templates
│
├── dashboard/               # Dashboard app
│   ├── views.py             # Dashboard views
│   ├── templates/           # Dashboard templates
│   └── urls.py              # Dashboard URLs
│
├── ml_engine/               # Machine Learning
│   ├── classifier.py        # Crime classification
│   ├── face_recognition_engine.py  # Face detection
│   └── models/              # Trained ML models
│
├── templates/               # Global templates
│   ├── base.html            # Base template
│   └── home.html            # Homepage
│
├── static/                  # Static files
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   └── js/
│       └── main.js          # JavaScript
│
├── media/                   # User uploads
│   ├── evidence/            # Evidence files
│   ├── profiles/            # Profile images
│   └── suspects/            # Suspect photos
│
├── requirements.txt         # Python dependencies
├── manage.py                # Django management
├── README.md                # This file
└── SETUP.md                 # Setup instructions
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git
- Virtualenv (recommended)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/crimetrake.git
   cd crimetrake_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Frontend: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

For detailed setup instructions, see [SETUP.md](SETUP.md)

---

## 📖 Usage

### For Citizens
1. Register as a citizen
2. Login to your account
3. Click "Report Crime" button
4. Fill in crime details with location and evidence
5. Track your case status in dashboard

### For Police Officers
1. Register as a police officer
2. Wait for admin verification
3. Login after verification
4. View assigned cases
5. Update case status and add investigation notes

### For Administrators
1. Login with superuser credentials
2. Verify pending police registrations
3. Assign cases to officers
4. View analytics and crime maps
5. Monitor system activity

---

## 🤖 AI/ML Features

### 1. Crime Classification
The system uses Natural Language Processing (NLP) to automatically categorize crime reports:

- **Algorithm**: TF-IDF + Naive Bayes / Logistic Regression
- **Categories**: Theft, Robbery, Assault, Cybercrime, Vandalism, etc.
- **Confidence Score**: Provides prediction confidence (0-1)

**How it works**:
```python
description = "Someone stole my laptop from my car"
category, confidence = classify_crime(description)
# Output: ("THEFT", 0.87)
```

### 2. Face Recognition
Automatically detects and matches faces in evidence photos:

- **Library**: face_recognition (dlib + OpenCV)
- **Process**: 
  1. Detect faces in uploaded images
  2. Extract 128-dimensional face encodings
  3. Compare with suspect database
  4. Alert if match found

**Features**:
- Multiple face detection per image
- Tolerance-based matching (adjustable)
- JSON storage of face encodings

### 3. Crime Mapping
Geographic visualization of crime locations:

- **Integration**: Google Maps JavaScript API
- **Features**:
  - Cluster analysis
  - Heatmap visualization
  - Filter by crime type and date

---

## 📸 Screenshots

### Homepage
"C:\Users\thaku\OneDrive\Pictures\CrimeTrake_Homepage.png"

### Citizen Dashboard
"C:\Users\thaku\OneDrive\Pictures\Citizen_dashboard.png"

### Crime Reporting
"C:\Users\thaku\OneDrive\Pictures\crime_reporting.png"

### Crime Map
"C:\Users\thaku\OneDrive\Pictures\crime_map.png"

---

## 🔐 Security Features

- **Password Hashing**: bcrypt algorithm
- **CSRF Protection**: Django built-in
- **Role-Based Access**: Strict permission checks
- **SQL Injection Prevention**: Django ORM
- **XSS Protection**: Template auto-escaping
- **File Upload Validation**: Type and size checks

---

## 📊 Database Schema

### User Model
- username, email, password
- role (CITIZEN/POLICE/ADMIN)
- phone, address, badge_number
- is_verified (for police)

### Crime Model
- case_id (auto-generated)
- reporter, crime_type, title, description
- location, latitude, longitude
- incident_date, status, priority
- assigned_officer
- ai_predicted_category, ai_confidence

### Evidence Model
- crime (foreign key)
- evidence_type, file
- faces_detected, face_encodings

---

## 🌐 Deployment

### Render (Recommended)
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set environment variables
5. Deploy!

### Railway
1. Install Railway CLI
2. Run `railway init`
3. Run `railway up`

### Manual (VPS)
See [SETUP.md](SETUP.md) for detailed deployment instructions.

---

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

With coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

- **Your Name** - *Initial work* - (https://github.com/anandkumar28)

---

## 🙏 Acknowledgments

- Font Awesome for icons
- Google for Maps API
- Django community
- scikit-learn documentation
- face_recognition library by Adam Geitgey

---

## 📞 Contact

For questions or support:
- Email: thakur.anand15154@gmail.com
- GitHub Issues: [Create Issue](https://github.com/anandkumar28/crimetrake/issues)

---

## 🔮 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] SMS notifications via Twilio
- [ ] Advanced ML models (LSTM, BERT)
- [ ] Real-time chat between citizens and police
- [ ] Blockchain for evidence integrity
- [ ] Multi-language support

---

**Made with ❤️ for BTech Final Year Project**
