from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CitizenRegistrationForm, PoliceRegistrationForm, CustomLoginForm, ProfileUpdateForm
from .models import User

def register_citizen(request):
    """Citizen registration view"""
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to CrimeTrake.')
            return redirect('dashboard:citizen_dashboard')
    else:
        form = CitizenRegistrationForm()
    
    return render(request, 'accounts/register_citizen.html', {'form': form})


def register_police(request):
    """Police officer registration view"""
    if request.method == 'POST':
        form = PoliceRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration submitted! Your account is pending verification.')
            return redirect('accounts:login')
    else:
        form = PoliceRegistrationForm()
    
    return render(request, 'accounts/register_police.html', {'form': form})


def user_login(request):
    """Login view for all users"""
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Check if police officer is verified
                if user.is_police() and not user.is_verified:
                    messages.error(request, 'Your account is pending verification by admin.')
                    return redirect('accounts:login')
                
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Redirect based on role
                if user.is_admin_user():
                    return redirect('dashboard:admin_dashboard')
                elif user.is_police():
                    return redirect('dashboard:police_dashboard')
                else:
                    return redirect('dashboard:citizen_dashboard')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    
    return render(request, 'accounts/delete_account.html')
