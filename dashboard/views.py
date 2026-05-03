from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.conf import settings
from crimes.models import Crime, Evidence
from accounts.models import User
from datetime import datetime, timedelta

@login_required
def citizen_dashboard(request):
    """Dashboard for citizens"""
    if not request.user.is_citizen():
        return redirect('dashboard:redirect_dashboard')
    
    # Get user's reported crimes
    my_crimes = Crime.objects.filter(reporter=request.user)
    
    # Statistics
    total_reports = my_crimes.count()
    active_cases = my_crimes.filter(status__in=['FILED', 'UNDER_INVESTIGATION', 'EVIDENCE_COLLECTED']).count()
    closed_cases = my_crimes.filter(status='CASE_CLOSED').count()
    
    # Recent crimes
    recent_crimes = my_crimes[:5]
    
    context = {
        'total_reports': total_reports,
        'active_cases': active_cases,
        'closed_cases': closed_cases,
        'recent_crimes': recent_crimes,
    }
    
    return render(request, 'dashboard/citizen_dashboard.html', context)


@login_required
def police_dashboard(request):
    """Dashboard for police officers"""
    if not request.user.is_police():
        return redirect('dashboard:redirect_dashboard')
    
    # Get assigned cases
    assigned_cases = Crime.objects.filter(assigned_officer=request.user)
    
    # Statistics
    total_assigned = assigned_cases.count()
    under_investigation = assigned_cases.filter(status='UNDER_INVESTIGATION').count()
    pending_cases = assigned_cases.filter(status='FILED').count()
    solved_cases = assigned_cases.filter(status='CASE_CLOSED').count()
    
    # High priority cases
    high_priority = assigned_cases.filter(priority__in=['HIGH', 'CRITICAL']).order_by('-created_at')[:5]
    
    # Recent unassigned cases in officer's department
    unassigned_cases = Crime.objects.filter(
        assigned_officer__isnull=True,
        status='FILED'
    ).order_by('-created_at')[:5]
    
    # Crime statistics by type
    crime_by_type = assigned_cases.values('crime_type').annotate(count=Count('id')).order_by('-count')
    
    context = {
        'total_assigned': total_assigned,
        'under_investigation': under_investigation,
        'pending_cases': pending_cases,
        'solved_cases': solved_cases,
        'high_priority': high_priority,
        'unassigned_cases': unassigned_cases,
        'crime_by_type': crime_by_type,
    }
    
    return render(request, 'dashboard/police_dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Dashboard for administrators"""
    if not request.user.is_admin_user():
        return redirect('dashboard:redirect_dashboard')
    
    # Overall statistics
    total_crimes = Crime.objects.count()
    total_users = User.objects.count()
    total_police = User.objects.filter(role='POLICE').count()
    total_citizens = User.objects.filter(role='CITIZEN').count()
    
    # Case statistics
    active_cases = Crime.objects.filter(status__in=['FILED', 'UNDER_INVESTIGATION']).count()
    closed_cases = Crime.objects.filter(status='CASE_CLOSED').count()
    unassigned_cases = Crime.objects.filter(assigned_officer__isnull=True).count()
    
    # Pending police verifications
    pending_police = User.objects.filter(role='POLICE', is_verified=False).count()
    
    # Recent crimes
    recent_crimes = Crime.objects.all().order_by('-created_at')[:10]
    
    # Crime statistics by type
    crime_by_type = Crime.objects.values('crime_type').annotate(count=Count('id')).order_by('-count')
    
    # Crime statistics by status
    crime_by_status = Crime.objects.values('status').annotate(count=Count('id'))
    
    # Monthly crime trends (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_crimes = Crime.objects.filter(
        created_at__gte=six_months_ago
    ).extra(
        select={'month': 'strftime("%%Y-%%m", created_at)'}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    context = {
        'total_crimes': total_crimes,
        'total_users': total_users,
        'total_police': total_police,
        'total_citizens': total_citizens,
        'active_cases': active_cases,
        'closed_cases': closed_cases,
        'unassigned_cases': unassigned_cases,
        'pending_police': pending_police,
        'recent_crimes': recent_crimes,
        'crime_by_type': crime_by_type,
        'crime_by_status': crime_by_status,
        'monthly_crimes': monthly_crimes,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def redirect_dashboard(request):
    """Redirect to appropriate dashboard based on user role"""
    if request.user.is_admin_user():
        return redirect('dashboard:admin_dashboard')
    elif request.user.is_police():
        return redirect('dashboard:police_dashboard')
    else:
        return redirect('dashboard:citizen_dashboard')


@login_required
def crime_map(request):
    """View crime map with location markers"""
    # Get all crimes with location data
    crimes = Crime.objects.exclude(latitude__isnull=True, longitude__isnull=True)
    
    # Filter by crime type if specified
    crime_type = request.GET.get('crime_type')
    if crime_type:
        crimes = crimes.filter(crime_type=crime_type)
    
    # Filter by date range
    days = request.GET.get('days', 30)
    try:
        days = int(days)
        start_date = datetime.now() - timedelta(days=days)
        crimes = crimes.filter(created_at__gte=start_date)
    except:
        pass
    
    # Prepare data for map
    crime_data = []
    for crime in crimes:
        crime_data.append({
            'case_id': crime.case_id,
            'title': crime.title,
            'crime_type': crime.get_crime_type_display(),
            'latitude': float(crime.latitude),
            'longitude': float(crime.longitude),
            'status': crime.get_status_display(),
            'date': crime.created_at.strftime('%Y-%m-%d'),
        })
    
    context = {
        'crime_data': crime_data,
        'crime_types': Crime.CRIME_TYPES,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    }
    
    return render(request, 'dashboard/crime_map.html', context)


@login_required
def analytics(request):
    """Analytics and statistics page"""
    # Only accessible by police and admin
    if not (request.user.is_police() or request.user.is_admin_user()):
        messages.error(request, 'You do not have permission to view analytics.')
        return redirect('dashboard:citizen_dashboard')
    
    # Get crime statistics
    total_crimes = Crime.objects.count()
    
    # Crime by type
    crime_by_type = Crime.objects.values('crime_type').annotate(count=Count('id')).order_by('-count')
    
    # Crime by status
    crime_by_status = Crime.objects.values('status').annotate(count=Count('id'))
    
    # Crime by priority
    crime_by_priority = Crime.objects.values('priority').annotate(count=Count('id'))
    
    # Monthly trends (last 12 months)
    twelve_months_ago = datetime.now() - timedelta(days=365)
    monthly_crimes = Crime.objects.filter(
        created_at__gte=twelve_months_ago
    ).extra(
        select={'month': 'strftime("%%Y-%%m", created_at)'}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Location-based statistics
    crimes_with_location = Crime.objects.exclude(latitude__isnull=True).count()
    
    context = {
        'total_crimes': total_crimes,
        'crime_by_type': crime_by_type,
        'crime_by_status': crime_by_status,
        'crime_by_priority': crime_by_priority,
        'monthly_crimes': monthly_crimes,
        'crimes_with_location': crimes_with_location,
    }
    
    return render(request, 'dashboard/analytics.html', context)
