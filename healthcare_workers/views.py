from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import HealthcareWorker
from .serializers import HealthcareWorkerSerializer


class HealthcareWorkersListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HealthcareWorker.objects.all().order_by('name')
    serializer_class = HealthcareWorkerSerializer


class HealthcareWorkersRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer
