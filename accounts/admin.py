from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    
    list_display = ['username', 'email', 'role', 'is_verified', 'created_at']
    list_filter = ['role', 'is_verified', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'address', 'badge_number', 'department', 'profile_image', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'address', 'badge_number', 'department', 'is_verified')
        }),
    )
    
    actions = ['verify_police_officers']
    
    def verify_police_officers(self, request, queryset):
        """Bulk action to verify police officers"""
        updated = queryset.filter(role='POLICE').update(is_verified=True)
        self.message_user(request, f'{updated} police officers verified successfully.')
    
    verify_police_officers.short_description = "Verify selected police officers"
