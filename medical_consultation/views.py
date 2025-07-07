from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MedicalConsultation
from .serializers import MedicalConsultationSerializer


class MedicalConsultationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MedicalConsultation.objects.all().order_by('-consultation_date')
    serializer_class = MedicalConsultationSerializer


class MedicalConsultationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MedicalConsultation.objects.all()
    serializer_class = MedicalConsultationSerializer
