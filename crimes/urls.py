from django.urls import path
from . import views

app_name = 'crimes'

urlpatterns = [
    path('report/', views.report_crime, name='report_crime'),
    path('case/<str:case_id>/', views.case_detail, name='case_detail'),
    path('case/<str:case_id>/upload-evidence/', views.upload_evidence, name='upload_evidence'),
    path('case/<str:case_id>/update/', views.update_case, name='update_case'),
    path('case/<str:case_id>/add-suspect/', views.add_suspect, name='add_suspect'),
    path('my-reports/', views.my_reports, name='my_reports'),
]
