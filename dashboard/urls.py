from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.redirect_dashboard, name='redirect_dashboard'),
    path('citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    path('police/', views.police_dashboard, name='police_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('map/', views.crime_map, name='crime_map'),
    path('analytics/', views.analytics, name='analytics'),
]
