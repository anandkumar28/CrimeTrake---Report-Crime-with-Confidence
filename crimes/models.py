from django.db import models
from django.conf import settings
import uuid
from datetime import datetime

class Crime(models.Model):
    """
    Crime Report Model
    Stores all crime reports filed by citizens
    """
    
    CRIME_TYPES = (
        ('THEFT', 'Theft'),
        ('ROBBERY', 'Robbery'),
        ('ASSAULT', 'Assault'),
        ('MURDER', 'Murder'),
        ('KIDNAPPING', 'Kidnapping'),
        ('CYBERCRIME', 'Cybercrime'),
        ('FRAUD', 'Fraud'),
        ('VANDALISM', 'Vandalism'),
        ('DOMESTIC_VIOLENCE', 'Domestic Violence'),
        ('DRUG_OFFENSE', 'Drug Offense'),
        ('OTHER', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('FILED', 'Filed'),
        ('UNDER_INVESTIGATION', 'Under Investigation'),
        ('EVIDENCE_COLLECTED', 'Evidence Collected'),
        ('SUSPECT_IDENTIFIED', 'Suspect Identified'),
        ('CASE_CLOSED', 'Case Closed'),
        ('REJECTED', 'Rejected'),
    )
    
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    )
    
    # Basic Information
    case_id = models.CharField(max_length=20, unique=True, editable=False)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_crimes')
    crime_type = models.CharField(max_length=20, choices=CRIME_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Location Details
    location = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Time Details
    incident_date = models.DateTimeField()
    reported_date = models.DateTimeField(auto_now_add=True)
    
    # Investigation Details
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='FILED')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_cases',
        limit_choices_to={'role': 'POLICE'}
    )
    
    # Additional Details
    is_anonymous = models.BooleanField(default=False)
    witness_count = models.IntegerField(default=0)
    suspect_description = models.TextField(blank=True)
    
    # AI Predicted Category (from ML)
    ai_predicted_category = models.CharField(max_length=20, blank=True)
    ai_confidence = models.FloatField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Crimes'
    
    def save(self, *args, **kwargs):
        if not self.case_id:
            # Generate unique case ID: CT-YYYY-XXXXXX
            year = datetime.now().year
            random_id = str(uuid.uuid4().hex[:6].upper())
            self.case_id = f'CT-{year}-{random_id}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.case_id} - {self.title}"


class Evidence(models.Model):
    """
    Evidence Model
    Stores all evidence files uploaded for a crime
    """
    
    EVIDENCE_TYPES = (
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('DOCUMENT', 'Document'),
        ('AUDIO', 'Audio'),
        ('OTHER', 'Other'),
    )
    
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, related_name='evidence')
    evidence_type = models.CharField(max_length=10, choices=EVIDENCE_TYPES)
    file = models.FileField(upload_to='evidence/%Y/%m/')
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Face detection results (if image)
    faces_detected = models.IntegerField(default=0)
    face_encodings = models.JSONField(null=True, blank=True)  # Store face recognition data
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Evidence'
    
    def __str__(self):
        return f"Evidence for {self.crime.case_id}"


class CaseUpdate(models.Model):
    """
    Case Update Model
    Track all updates made to a case
    """
    
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=30)
    new_status = models.CharField(max_length=30)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Update for {self.crime.case_id} by {self.updated_by.username}"


class Suspect(models.Model):
    """
    Suspect Model
    Store information about suspects
    """
    
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, related_name='suspects')
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='suspects/', null=True, blank=True)
    
    # Face recognition data
    face_encoding = models.JSONField(null=True, blank=True)
    
    # Additional details
    age_estimate = models.IntegerField(null=True, blank=True)
    height_estimate = models.CharField(max_length=20, blank=True)
    identifying_marks = models.TextField(blank=True)
    
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_at']
    
    def __str__(self):
        return f"Suspect for {self.crime.case_id}"
