from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Crime, Evidence, CaseUpdate, Suspect
from .forms import CrimeReportForm, EvidenceUploadForm, CaseUpdateForm, SuspectForm
from ml_engine.classifier import classify_crime
from ml_engine.face_recognition_engine import detect_faces

@login_required
def report_crime(request):
    """Crime reporting view for citizens"""
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            crime = form.save(commit=False)
            crime.reporter = request.user
            
            # Use ML to predict crime category
            try:
                predicted_category, confidence = classify_crime(crime.description)
                crime.ai_predicted_category = predicted_category
                crime.ai_confidence = confidence
            except Exception as e:
                print(f"ML Classification Error: {e}")
            
            crime.save()
            
            # Send confirmation email
            try:
                send_mail(
                    subject=f'Crime Report Filed - {crime.case_id}',
                    message=f'Your crime report has been filed successfully.\n\nCase ID: {crime.case_id}\nStatus: {crime.get_status_display()}\n\nYou can track your case status in your dashboard.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email Error: {e}")
            
            messages.success(request, f'Crime reported successfully! Case ID: {crime.case_id}')
            return redirect('crimes:case_detail', case_id=crime.case_id)
    else:
        form = CrimeReportForm()
    
    return render(request, 'crimes/report_crime.html', {'form': form})


@login_required
def case_detail(request, case_id):
    """View details of a specific case"""
    crime = get_object_or_404(Crime, case_id=case_id)
    
    # Check permissions
    if not (request.user == crime.reporter or request.user.is_police() or request.user.is_admin_user()):
        messages.error(request, 'You do not have permission to view this case.')
        return redirect('dashboard:citizen_dashboard')
    
    evidence_list = crime.evidence.all()
    updates = crime.updates.all()
    suspects = crime.suspects.all()
    
    context = {
        'crime': crime,
        'evidence_list': evidence_list,
        'updates': updates,
        'suspects': suspects,
    }
    
    return render(request, 'crimes/case_detail.html', context)


@login_required
def upload_evidence(request, case_id):
    """Upload evidence for a case"""
    crime = get_object_or_404(Crime, case_id=case_id)
    
    # Check permissions
    if not (request.user == crime.reporter or request.user.is_police() or request.user.is_admin_user()):
        messages.error(request, 'You do not have permission to upload evidence.')
        return redirect('crimes:case_detail', case_id=case_id)
    
    if request.method == 'POST':
        form = EvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.crime = crime
            evidence.uploaded_by = request.user
            
            # If image, run face detection
            if evidence.evidence_type == 'IMAGE' and evidence.file:
                try:
                    faces_detected, face_encodings = detect_faces(evidence.file.path)
                    evidence.faces_detected = faces_detected
                    evidence.face_encodings = face_encodings
                except Exception as e:
                    print(f"Face Detection Error: {e}")
            
            evidence.save()
            messages.success(request, 'Evidence uploaded successfully!')
            return redirect('crimes:case_detail', case_id=case_id)
    else:
        form = EvidenceUploadForm()
    
    return render(request, 'crimes/upload_evidence.html', {'form': form, 'crime': crime})


@login_required
def update_case(request, case_id):
    """Update case status (Police/Admin only)"""
    if not (request.user.is_police() or request.user.is_admin_user()):
        messages.error(request, 'Only police officers can update case status.')
        return redirect('crimes:case_detail', case_id=case_id)
    
    crime = get_object_or_404(Crime, case_id=case_id)
    
    if request.method == 'POST':
        form = CaseUpdateForm(request.POST)
        if form.is_valid():
            case_update = form.save(commit=False)
            case_update.crime = crime
            case_update.updated_by = request.user
            case_update.old_status = crime.status
            case_update.save()
            
            # Update crime status
            crime.status = case_update.new_status
            crime.save()
            
            # Send email notification to reporter
            try:
                send_mail(
                    subject=f'Case Update - {crime.case_id}',
                    message=f'Your case has been updated.\n\nCase ID: {crime.case_id}\nNew Status: {crime.get_status_display()}\n\nNotes: {case_update.notes}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[crime.reporter.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email Error: {e}")
            
            messages.success(request, 'Case updated successfully!')
            return redirect('crimes:case_detail', case_id=case_id)
    else:
        form = CaseUpdateForm()
    
    return render(request, 'crimes/update_case.html', {'form': form, 'crime': crime})


@login_required
def add_suspect(request, case_id):
    """Add suspect to a case (Police only)"""
    if not (request.user.is_police() or request.user.is_admin_user()):
        messages.error(request, 'Only police officers can add suspects.')
        return redirect('crimes:case_detail', case_id=case_id)
    
    crime = get_object_or_404(Crime, case_id=case_id)
    
    if request.method == 'POST':
        form = SuspectForm(request.POST, request.FILES)
        if form.is_valid():
            suspect = form.save(commit=False)
            suspect.crime = crime
            suspect.added_by = request.user
            
            # Extract face encoding if photo provided
            if suspect.photo:
                try:
                    faces_detected, face_encodings = detect_faces(suspect.photo.path)
                    if faces_detected > 0 and face_encodings:
                        suspect.face_encoding = face_encodings[0]  # Store first face
                except Exception as e:
                    print(f"Face Detection Error: {e}")
            
            suspect.save()
            messages.success(request, 'Suspect added successfully!')
            return redirect('crimes:case_detail', case_id=case_id)
    else:
        form = SuspectForm()
    
    return render(request, 'crimes/add_suspect.html', {'form': form, 'crime': crime})


@login_required
def my_reports(request):
    """View all reports filed by current user"""
    crimes = Crime.objects.filter(reporter=request.user)
    return render(request, 'crimes/my_reports.html', {'crimes': crimes})
