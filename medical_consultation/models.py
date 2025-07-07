from django.db import models
from healthcare_workers.models import HealthcareWorker


class MedicalConsultation(models.Model):
    patient_name = models.CharField(max_length=80)
    patient_preferred_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField()
    healthcare_worker = models.ForeignKey(HealthcareWorker, on_delete=models.PROTECT, related_name='medical_consultations')
    consultation_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.patient_preferred_name:
            return self.patient_preferred_name
        else:
            return self.patient_name
