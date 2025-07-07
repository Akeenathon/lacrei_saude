from django.urls import path
from .views import MedicalConsultationListCreateView, MedicalConsultationRetrieveUpdateDestroyView


urlpatterns = [
    path('medicalconsultation/', MedicalConsultationListCreateView.as_view(), name='medicalconsultation_list'),
    path('medicalconsultation/<int:pk>/', MedicalConsultationRetrieveUpdateDestroyView.as_view(), name='medicalconsultation_detail')
]
