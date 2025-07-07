from django.contrib import admin
from .models import MedicalConsultation


@admin.register(MedicalConsultation)
class MedicalConsultationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'patient_name', 'patient_preferred_name',
        'age', 'healthcare_worker', 'consultation_date',
        'created_at'
    )
    search_fields = (
        'id', 'patient_name', 'patient_preferred_name',
        'healthcare_worker__name', 'healthcare_worker__profession',
        'consultation_date'
    )
    list_filter = ('healthcare_worker', 'consultation_date', 'created_at')
    ordering = ('-consultation_date',)
    list_per_page = 20
