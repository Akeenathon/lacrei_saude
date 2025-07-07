from rest_framework import generics
from .models import MedicalConsultation
from .serializers import MedicalConsultationSerializer


class MedicalConsultationListCreateView(generics.ListCreateAPIView):
    queryset = MedicalConsultation.objects.all().order_by('-consultation_date')
    serializer_class = MedicalConsultationSerializer


class MedicalConsultationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalConsultation.objects.all()
    serializer_class = MedicalConsultationSerializer
