from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, time
from .models import MedicalConsultation


class MedicalConsultationSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalConsultation
        fields = '__all__'

    def validate_consultation_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "A data da consulta não pode ser no passado."
            )
        return value

    # Verificar se contém apenas letras e espaços
    def validate_patient_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Nome do paciente deve ter pelo menos 2 caracteres."
            )
        
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                "Nome do paciente deve conter apenas letras e espaços."
            )
        
        return value.strip().title()

    def validate_patient_phone(self, value):
        if value:
            # Remover caracteres especiais
            phone_digits = ''.join(filter(str.isdigit, value))
            
            # Verificar se tem entre 10 e 11 dígitos (formato brasileiro)
            if len(phone_digits) < 10 or len(phone_digits) > 11:
                raise serializers.ValidationError(
                    "Telefone deve ter entre 10 e 11 dígitos."
                )
        
        return value

    # Verificar formato básico de email
    def validate_patient_email(self, value):
        if value:
            if '@' not in value or '.' not in value.split('@')[-1]:
                raise serializers.ValidationError(
                    "Email deve ter um formato válido."
                )
        
        return value.lower() if value else value

    def validate(self, data):
        healthcare_worker = data.get('healthcare_worker')
        consultation_date = data.get('consultation_date')
        
        # Validar se não há consulta no mesmo horário para o mesmo médico
        if healthcare_worker and consultation_date:
            existing_consultation = MedicalConsultation.objects.filter(
                healthcare_worker=healthcare_worker,
                consultation_date=consultation_date
            ).first()
            
            if existing_consultation and existing_consultation.id != getattr(self.instance, 'id', None):
                raise serializers.ValidationError(
                    'Este profissional já tem uma consulta marcada neste horário!'
                )

        # Validar horário comercial (8h às 18h)
        if consultation_date:
            hour = consultation_date.hour
            if hour < 8 or hour > 18:
                raise serializers.ValidationError(
                    'Consultas só podem ser marcadas entre 8h e 18h.'
                )

        # Validar se paciente tem nome e pelo menos um contato
        patient_name = data.get('patient_name')
        patient_phone = data.get('patient_phone')
        patient_email = data.get('patient_email')
        
        if patient_name and not (patient_phone or patient_email):
            raise serializers.ValidationError(
                'É necessário fornecer pelo menos um contato (telefone ou email) do paciente.'
            )
        
        return data

    # Não permitir alterar consultas já finalizadas
    def update(self, instance, validated_data):
        if instance.status == 'completed':
            raise serializers.ValidationError(
                'Não é possível alterar consultas já finalizadas.'
            )
        
        return super().update(instance, validated_data)
