from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from healthcare_workers.models import HealthcareWorker
from .models import MedicalConsultation


class MedicalConsultationAPITestCase(APITestCase):

    def setUp(self):
        """Configuração inicial para todos os testes"""

        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='akeenathon',
            password='djangomaster',
            email='test@example.com'
        )

        # Gerar token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Criar profissional de saúde
        self.healthcare_worker = HealthcareWorker.objects.create(
            name='Dr. João',
            preferred_name='Silva',
            profession='Clínico Geral',
            address='Rodolfo de abreu, 436',
            phone='33999190106'
        )

        # Data futura para consultas (dentro do horário comercial: 8h às 18h)
        tomorrow = timezone.now().date() + timedelta(days=1)
        self.future_date = timezone.make_aware(
            datetime.combine(tomorrow, datetime.min.time().replace(hour=10, minute=0))
        )

        # Dados válidos para criação de consulta
        self.valid_consultation_data = {
            'patient_name': 'Maria Santos',
            'patient_preferred_name': 'Maria',
            'age': 35,
            'healthcare_worker': self.healthcare_worker.id,
            'consultation_date': self.future_date.isoformat(),
            'phone': '33999999999'
        }

        # URLs das APIs
        self.list_create_url = reverse('medicalconsultation_list')
        self.token_url = reverse('token_obtain_pair')

    def authenticate(self):
        """Método para autenticar as requisições"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_jwt_token(self):
        """Testa obtenção do token JWT"""
        response = self.client.post(self.token_url, {
            'username': 'akeenathon',
            'password': 'djangomaster'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_unauthenticated_access_denied(self):
        """Testa que requisições sem autenticação são negadas"""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_medical_consultations(self):
        """Testa listagem de consultas médicas"""
        # Criar algumas consultas para teste
        MedicalConsultation.objects.create(
            patient_name='João Silva',
            age=30,
            healthcare_worker=self.healthcare_worker,
            consultation_date=self.future_date
        )

        MedicalConsultation.objects.create(
            patient_name='Ana Santos',
            age=25,
            healthcare_worker=self.healthcare_worker,
            consultation_date=self.future_date + timedelta(hours=1)
        )

        self.authenticate()
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_medical_consultation_success(self):
        """Testa criação bem-sucedida de consulta médica"""
        self.authenticate()

        response = self.client.post(self.list_create_url, self.valid_consultation_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalConsultation.objects.count(), 1)

        consultation = MedicalConsultation.objects.first()
        self.assertEqual(consultation.patient_name, 'Maria Santos')

    def test_create_medical_consultation_invalid_data(self):
        """Testa criação com dados inválidos"""
        self.authenticate()

        # Teste com nome muito curto
        invalid_data = self.valid_consultation_data.copy()
        invalid_data['patient_name'] = 'A'

        response = self.client.post(self.list_create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_medical_consultation_empty_data(self):
        """Testa criação sem dados"""
        self.authenticate()

        response = self.client.post(self.list_create_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_medical_consultation_missing_required_fields(self):
        """Testa criação sem campos obrigatórios"""
        self.authenticate()

        # Teste sem nome do paciente
        invalid_data = self.valid_consultation_data.copy()
        del invalid_data['patient_name']

        response = self.client.post(self.list_create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_medical_consultation(self):
        """Testa recuperação de consulta específica"""
        consultation = MedicalConsultation.objects.create(
            patient_name='João Silva',
            age=30,
            healthcare_worker=self.healthcare_worker,
            consultation_date=self.future_date
        )

        self.authenticate()

        detail_url = reverse('medicalconsultation_detail', kwargs={'pk': consultation.id})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient_name'], 'João Silva')

    def test_update_medical_consultation(self):
        """Testa atualização de consulta médica"""
        consultation = MedicalConsultation.objects.create(
            patient_name='João Silva',
            age=30,
            healthcare_worker=self.healthcare_worker,
            consultation_date=self.future_date
        )

        self.authenticate()

        detail_url = reverse('medicalconsultation_detail', kwargs={'pk': consultation.id})
        update_data = {
            'patient_name': 'João Santos Silva',
            'age': 31
        }

        response = self.client.patch(detail_url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        consultation.refresh_from_db()
        self.assertEqual(consultation.patient_name, 'João Santos Silva')

    def test_delete_medical_consultation(self):
        """Testa exclusão de consulta médica"""
        consultation = MedicalConsultation.objects.create(
            patient_name='João Silva',
            age=30,
            healthcare_worker=self.healthcare_worker,
            consultation_date=self.future_date
        )

        self.authenticate()

        detail_url = reverse('medicalconsultation_detail', kwargs={'pk': consultation.id})
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicalConsultation.objects.count(), 0)

    def test_patient_name_validation(self):
        """Testa validação do nome do paciente"""
        self.authenticate()

        # Teste com nome válido
        data = self.valid_consultation_data.copy()
        data['patient_name'] = 'João Silva'

        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste com nome inválido
        data['patient_name'] = 'A'
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_str_representation(self):
        """Testa representação string do modelo"""
        consultation = MedicalConsultation.objects.create(
            patient_name='João Silva',
            patient_preferred_name='João',
            age=30,
            healthcare_worker=self.healthcare_worker,
            consultation_date=self.future_date
        )

        self.assertEqual(str(consultation), 'João')
