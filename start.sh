#!/bin/bash

# CrimeTrake Quick Start Script
# This script sets up the project automatically

echo "🚀 CrimeTrake Quick Start Script"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install Django==4.2.7 pillow==10.1.0 scikit-learn==1.3.2 pandas==2.1.3 numpy==1.26.2

echo ""
echo "⚠️  Note: Face recognition packages (opencv-python, face-recognition) are optional."
echo "   The app will work without them. Install manually if needed."
echo ""

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ Please edit .env file with your settings"
fi

# Run migrations
echo "🗄️  Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "👤 Create admin account:"
python manage.py createsuperuser

# Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 To start the server:"
echo "   python manage.py runserver"
echo ""
echo "🌐 Access the application at:"
echo "   Frontend: http://localhost:8000"
echo "   Admin: http://localhost:8000/admin"
echo ""
echo "📚 Read README.md and SETUP.md for more information"
echo ""
