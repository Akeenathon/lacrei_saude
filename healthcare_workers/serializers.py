from rest_framework import serializers
from .models import HealthcareWorker


class HealthcareWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthcareWorker
        fields = '__all__'

    def validate_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Nome deve ter pelo menos 2 caracteres."
            )
        
        return value.strip().title()

    def validate_profession(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Profissão deve ter pelo menos 3 caracteres."
            )
        
        return value.strip().title()

    def validate_address(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Endereço deve ter pelo menos 5 caracteres."
            )
        
        return value.strip()

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError(
                "Telefone é obrigatório."
            )
        
        # Remover caracteres especiais
        phone_digits = ''.join(filter(str.isdigit, value))
        
        # Verificar se tem entre 10 e 11 dígitos (formato brasileiro)
        if len(phone_digits) < 10 or len(phone_digits) > 11:
            raise serializers.ValidationError(
                "Telefone deve ter entre 10 e 11 dígitos."
            )
        
        return value

    # Verificar se email já existe
    def validate_email(self, value):
        if value:
            if HealthcareWorker.objects.filter(email=value).exclude(
                id=getattr(self.instance, 'id', None)
            ).exists():
                raise serializers.ValidationError(
                    "Este email já está cadastrado."
                )
        
        return value.lower() if value else value
