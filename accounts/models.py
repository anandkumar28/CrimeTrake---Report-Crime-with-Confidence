from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model with role-based access control
    Roles: CITIZEN, POLICE, ADMIN
    """
    
    ROLE_CHOICES = (
        ('CITIZEN', 'Citizen'),
        ('POLICE', 'Police Officer'),
        ('ADMIN', 'Administrator'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CITIZEN')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    badge_number = models.CharField(max_length=20, blank=True, null=True)  # For police
    department = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['-created_at']
        
    def is_citizen(self):
        return self.role == 'CITIZEN'
    
    def is_police(self):
        return self.role == 'POLICE'
    
    def is_admin_user(self):
        return self.role == 'ADMIN'
