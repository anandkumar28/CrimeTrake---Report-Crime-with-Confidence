from django import forms
from .models import Crime, Evidence, CaseUpdate, Suspect

class CrimeReportForm(forms.ModelForm):
    """Form for filing a crime report"""
    
    class Meta:
        model = Crime
        fields = [
            'crime_type', 'title', 'description', 'location',
            'latitude', 'longitude', 'incident_date',
            'is_anonymous', 'witness_count', 'suspect_description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe what happened in detail...'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter crime location'}),
            'suspect_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the suspect(s) if any...'}),
            'incident_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes
        for field in self.fields:
            if field not in ['latitude', 'longitude', 'is_anonymous']:
                self.fields[field].widget.attrs['class'] = 'form-control'


class EvidenceUploadForm(forms.ModelForm):
    """Form for uploading evidence"""
    
    class Meta:
        model = Evidence
        fields = ['evidence_type', 'file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe this evidence...'}),
        }


class CaseUpdateForm(forms.ModelForm):
    """Form for updating case status (Police only)"""
    
    class Meta:
        model = CaseUpdate
        fields = ['new_status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter update notes...'}),
        }


class AssignOfficerForm(forms.ModelForm):
    """Form for assigning officer to case (Admin only)"""
    
    class Meta:
        model = Crime
        fields = ['assigned_officer', 'priority']


class SuspectForm(forms.ModelForm):
    """Form for adding suspect information"""
    
    class Meta:
        model = Suspect
        fields = ['name', 'description', 'photo', 'age_estimate', 'height_estimate', 'identifying_marks']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'identifying_marks': forms.Textarea(attrs={'rows': 3}),
        }
