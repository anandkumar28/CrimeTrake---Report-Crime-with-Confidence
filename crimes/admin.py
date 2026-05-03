from django.contrib import admin
from .models import Crime, Evidence, CaseUpdate, Suspect

@admin.register(Crime)
class CrimeAdmin(admin.ModelAdmin):
    """Admin interface for Crime model"""
    
    list_display = ['case_id', 'title', 'crime_type', 'status', 'priority', 'reporter', 'assigned_officer', 'created_at']
    list_filter = ['status', 'crime_type', 'priority', 'created_at']
    search_fields = ['case_id', 'title', 'description', 'location']
    readonly_fields = ['case_id', 'created_at', 'updated_at', 'ai_predicted_category', 'ai_confidence']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('case_id', 'reporter', 'crime_type', 'title', 'description')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Time Details', {
            'fields': ('incident_date', 'reported_date', 'created_at', 'updated_at')
        }),
        ('Investigation', {
            'fields': ('status', 'priority', 'assigned_officer')
        }),
        ('Additional Info', {
            'fields': ('is_anonymous', 'witness_count', 'suspect_description')
        }),
        ('AI Analysis', {
            'fields': ('ai_predicted_category', 'ai_confidence'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    """Admin interface for Evidence model"""
    
    list_display = ['crime', 'evidence_type', 'uploaded_by', 'faces_detected', 'uploaded_at']
    list_filter = ['evidence_type', 'uploaded_at']
    search_fields = ['crime__case_id', 'description']


@admin.register(CaseUpdate)
class CaseUpdateAdmin(admin.ModelAdmin):
    """Admin interface for CaseUpdate model"""
    
    list_display = ['crime', 'old_status', 'new_status', 'updated_by', 'created_at']
    list_filter = ['old_status', 'new_status', 'created_at']
    search_fields = ['crime__case_id', 'notes']


@admin.register(Suspect)
class SuspectAdmin(admin.ModelAdmin):
    """Admin interface for Suspect model"""
    
    list_display = ['crime', 'name', 'age_estimate', 'added_by', 'added_at']
    list_filter = ['added_at']
    search_fields = ['crime__case_id', 'name', 'description']
