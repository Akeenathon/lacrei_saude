from rest_framework import generics
from .models import HealthcareWorker
from .serializers import HealthcareWorkerSerializer


class HealthcareWorkersListCreateView(generics.ListCreateAPIView):
    queryset = HealthcareWorker.objects.all().order_by('name')
    serializer_class = HealthcareWorkerSerializer


class HealthcareWorkersRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer
