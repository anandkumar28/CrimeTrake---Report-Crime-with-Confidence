from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CitizenRegistrationForm(UserCreationForm):
    """Registration form for citizens"""
    
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'CITIZEN'
        if commit:
            user.save()
        return user


class PoliceRegistrationForm(UserCreationForm):
    """Registration form for police officers"""
    
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    badge_number = forms.CharField(max_length=20, required=True)
    department = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'badge_number', 'department', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'POLICE'
        user.is_verified = False  # Needs admin verification
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    """Custom login form with styling"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_image']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
