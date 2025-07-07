from rest_framework import serializers
from .models import HealthcareWorker


class HealthcareWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthcareWorker
        fields = '__all__'
