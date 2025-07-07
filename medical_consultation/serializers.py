from rest_framework import serializers
from .models import MedicalConsultation


class MedicalConsultationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalConsultation
        fields = '__all__'

    # Função para garantir que não seja marcado consultas no mesmo dia e horario para o mesmo médico
    def validate(self, data):
        healthcare_worker = data.get('healthcare_worker')
        consultation_date = data.get('consultation_date')
        
        existing_consultation = MedicalConsultation.objects.filter(
            healthcare_worker=healthcare_worker,
            consultation_date=consultation_date
        ).first()
        
        if existing_consultation and existing_consultation.id != getattr(self.instance, 'id', None):
            raise serializers.ValidationError(
                'Este profissional já tem uma consulta marcada neste horário!'
            )
        
        return data
