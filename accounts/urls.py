from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/citizen/', views.register_citizen, name='register_citizen'),
    path('register/police/', views.register_police, name='register_police'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.delete_account, name='delete_account'),
]
