# 🌐 External Services Setup Guide

Complete guide to set up Google Maps API and Gmail SMTP for CrimeTrake.

---

## 📍 Google Maps API Setup (100% FREE)

Google Maps is used for displaying crime locations on the interactive map.

### Step 1: Create Google Cloud Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Accept the Terms of Service

### Step 2: Create New Project

1. Click on the project dropdown (top left)
2. Click **"New Project"**
3. Enter project name: `CrimeTrake`
4. Click **"Create"**
5. Wait for project to be created (takes ~30 seconds)

### Step 3: Enable Required APIs

1. Go to **"APIs & Services"** → **"Library"**
2. Search and enable these APIs:
   - **Maps JavaScript API** (for displaying maps)
   - **Geocoding API** (for converting addresses to coordinates)
   - **Places API** (optional, for location search)

Click **"Enable"** for each API.

### Step 4: Create API Key

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"API Key"**
3. Your API key will be generated (looks like: `AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
4. **IMPORTANT**: Click **"Restrict Key"** for security

### Step 5: Restrict API Key (IMPORTANT)

1. Under **"Application restrictions"**:
   - Select **"HTTP referrers (web sites)"**
   - Add your website URLs:
     - `http://localhost:8000/*` (for development)
     - `https://your-domain.com/*` (for production)

2. Under **"API restrictions"**:
   - Select **"Restrict key"**
   - Check these APIs:
     - Maps JavaScript API
     - Geocoding API

3. Click **"Save"**

### Step 6: Add API Key to Project

1. Open `.env` file in your project
2. Add your API key:
   ```env
   GOOGLE_MAPS_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Step 7: Test the Map

1. Start your Django server:
   ```bash
   python manage.py runserver
   ```

2. Login and go to:
   ```
   http://localhost:8000/dashboard/map/
   ```

3. You should see an interactive map with crime markers!

### Free Tier Limits

Google Maps offers **$200 FREE credit per month**, which equals to:
- **28,000 map loads** per month
- More than enough for a student project!

---

## 📧 Gmail SMTP Setup (100% FREE)

Gmail SMTP is used to send email notifications to users about case updates.

### Step 1: Enable 2-Factor Authentication

**IMPORTANT**: You MUST enable 2FA first!

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click **"2-Step Verification"**
3. Click **"Get Started"**
4. Follow the steps to set up 2FA with:
   - Phone number (recommended)
   - Or authenticator app

### Step 2: Generate App Password

1. After enabling 2FA, go back to [Security Settings](https://myaccount.google.com/security)
2. Scroll to **"Signing in to Google"**
3. Click **"App passwords"**
   
   **Note**: If you don't see "App passwords":
   - Make sure 2FA is enabled
   - Try logging out and back in
   - Use this direct link: [App Passwords](https://myaccount.google.com/apppasswords)

4. Select app: **"Mail"**
5. Select device: **"Other (Custom name)"**
6. Enter name: `CrimeTrake Django`
7. Click **"Generate"**

8. **IMPORTANT**: Copy the 16-character password
   - Example: `abcd efgh ijkl mnop`
   - Remove spaces when using: `abcdefghijklmnop`
   - You can only see this ONCE!

### Step 3: Add to Django Settings

1. Open `.env` file
2. Add your email credentials:
   ```env
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   
   **Replace**:
   - `your-email@gmail.com` with your actual Gmail
   - `abcdefghijklmnop` with your generated app password (no spaces)

### Step 4: Test Email Sending

Run this test in Django shell:

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    subject='Test Email from CrimeTrake',
    message='This is a test email. If you received this, email setup is working!',
    from_email='your-email@gmail.com',
    recipient_list=['your-email@gmail.com'],  # Send to yourself for testing
    fail_silently=False,
)
```

If successful, you'll see: `1`

Check your Gmail inbox for the test email!

### Common Email Issues

**Issue 1: "Username and Password not accepted"**
- Make sure 2FA is enabled
- Regenerate app password
- Remove any spaces from password
- Use the app password, NOT your regular Gmail password

**Issue 2: "SMTPAuthenticationError"**
- Check if `EMAIL_HOST_USER` is correct
- Make sure you're using app password
- Try generating a new app password

**Issue 3: Email not received**
- Check spam/junk folder
- Make sure `from_email` matches `EMAIL_HOST_USER`
- Try sending to a different email address

### Free Tier Limits

Gmail SMTP is **100% FREE** with limits:
- **500 emails per day** (more than enough!)
- Perfect for student projects

---

## 🔧 Complete .env Configuration

Your final `.env` file should look like:

```env
# Django Settings
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
# No configuration needed for SQLite

# Email Configuration (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Google Maps API
GOOGLE_MAPS_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Application Settings
TIME_ZONE=Asia/Kolkata
```

---

## ✅ Verification Checklist

After setup, verify everything works:

### Google Maps
- [ ] API key created
- [ ] Maps JavaScript API enabled
- [ ] Geocoding API enabled
- [ ] API key restricted (for security)
- [ ] API key added to `.env`
- [ ] Map loads at `/dashboard/map/`
- [ ] Crime markers appear on map

### Gmail SMTP
- [ ] 2-Factor Authentication enabled
- [ ] App password generated
- [ ] Credentials added to `.env`
- [ ] Test email sent successfully
- [ ] Email received in inbox
- [ ] Case update emails working

---

## 🎯 Testing in Production

When deploying to production (Render, Railway, etc.):

1. **Add environment variables** to your hosting platform:
   - Go to Environment Variables section
   - Add `GOOGLE_MAPS_API_KEY`
   - Add `EMAIL_HOST_USER`
   - Add `EMAIL_HOST_PASSWORD`

2. **Update Google Maps restrictions**:
   - Add your production domain to allowed referrers
   - Example: `https://crimetrake.onrender.com/*`

3. **Test thoroughly** before going live

---

## 💰 Cost Breakdown (Both 100% FREE!)

| Service | Free Tier | Cost After |
|---------|-----------|------------|
| **Google Maps** | $200 credit/month (28,000 loads) | $7 per 1,000 loads |
| **Gmail SMTP** | 500 emails/day | Always free |

**For Student Projects**: You'll NEVER exceed free limits! 🎉

---

## 🆘 Troubleshooting

### Google Maps Not Loading

**Problem**: Blank map or error message

**Solutions**:
1. Check browser console (F12) for errors
2. Verify API key is correct in `.env`
3. Make sure Maps JavaScript API is enabled
4. Check API key restrictions
5. Clear browser cache

### Emails Not Sending

**Problem**: No emails received

**Solutions**:
1. Check spam folder
2. Verify app password (no spaces)
3. Test with Django shell command
4. Check `.env` file syntax
5. Restart Django server after `.env` changes

### "API Key Invalid" Error

**Solutions**:
1. Regenerate API key
2. Remove and re-add to `.env`
3. Check for extra spaces or quotes
4. Wait 5 minutes for Google to propagate changes

---

## 📚 Additional Resources

- [Google Maps Documentation](https://developers.google.com/maps/documentation)
- [Gmail SMTP Guide](https://support.google.com/mail/answer/7126229)
- [Django Email Documentation](https://docs.djangoproject.com/en/4.2/topics/email/)

---

## 🎓 Video Tutorials (Recommended)

If you prefer video guides:

**Google Maps API**:
1. Search YouTube: "Google Maps API Tutorial 2024"
2. Watch first 10 minutes for key setup

**Gmail SMTP**:
1. Search YouTube: "Gmail SMTP App Password 2024"
2. Follow along for app password generation

---

## ✨ Quick Setup Summary

**5-Minute Setup**:

1. **Google Maps** (2 minutes):
   - Create project → Enable APIs → Get API key → Add to `.env`

2. **Gmail SMTP** (3 minutes):
   - Enable 2FA → Generate app password → Add to `.env`

3. **Test** (1 minute):
   - Run server → Check map → Send test email

**Done! 🎉**

---

## 🔒 Security Best Practices

1. **Never commit `.env` to Git**
   - Already in `.gitignore`
   - Keep API keys secret!

2. **Use environment variables in production**
   - Don't hardcode keys in code
   - Use hosting platform's env vars

3. **Restrict API keys**
   - Limit to specific domains
   - Enable only needed APIs

4. **Rotate keys regularly**
   - Change app password every 3-6 months
   - Regenerate API keys if exposed

---

**Need Help?**
- Check the troubleshooting section
- Search for error messages on Google
- Ask in project discussion forums

**You've got this! 💪**
