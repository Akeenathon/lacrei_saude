import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

from .models import HealthcareWorker
from .serializers import HealthcareWorkerSerializer


class HealthcareWorkerAPITestCase(APITestCase):
    
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
        
        # Dados válidos para criação de profissional
        self.valid_worker_data = {
            'name': 'Dr. João Silva',
            'preferred_name': 'João',
            'profession': 'Clínico Geral',
            'address': 'Rua das Flores, 123 - Centro',
            'phone': '33999190106',
            'email': 'joao.silva@exemplo.com'
        }
        
        # URLs das APIs
        self.list_create_url = reverse('healthcareworkers_list')
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

    def test_list_healthcare_workers(self):
        """Testa listagem de profissionais de saúde"""
        # Criar alguns profissionais para teste
        HealthcareWorker.objects.create(
            name='Dr. João Silva',
            preferred_name='João',
            profession='Clínico Geral',
            address='Rua das Flores, 123',
            phone='33999190106'
        )
        
        HealthcareWorker.objects.create(
            name='Dra. Maria Santos',
            preferred_name='Maria',
            profession='Cardiologista',
            address='Av. Principal, 456',
            phone='33999290107'
        )
        
        self.authenticate()
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_healthcare_worker_success(self):
        """Testa criação bem-sucedida de profissional"""
        self.authenticate()
        
        response = self.client.post(self.list_create_url, self.valid_worker_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HealthcareWorker.objects.count(), 1)
        
        worker = HealthcareWorker.objects.first()
        self.assertEqual(worker.name, 'Dr. João Silva')
        self.assertEqual(worker.profession, 'Clínico Geral')

    def test_create_healthcare_worker_invalid_data(self):
        """Testa criação com dados inválidos"""
        self.authenticate()
        
        # Teste com nome muito curto
        invalid_data = self.valid_worker_data.copy()
        invalid_data['name'] = 'A'
        
        response = self.client.post(self.list_create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_healthcare_worker_empty_data(self):
        """Testa criação sem dados"""
        self.authenticate()
        
        response = self.client.post(self.list_create_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_healthcare_worker_missing_required_fields(self):
        """Testa criação sem campos obrigatórios"""
        self.authenticate()
        
        # Teste sem nome
        invalid_data = self.valid_worker_data.copy()
        del invalid_data['name']
        
        response = self.client.post(self.list_create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Teste sem telefone
        invalid_data = self.valid_worker_data.copy()
        del invalid_data['phone']
        
        response = self.client.post(self.list_create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_healthcare_worker(self):
        """Testa recuperação de profissional específico"""
        worker = HealthcareWorker.objects.create(
            name='Dr. João Silva',
            preferred_name='João',
            profession='Clínico Geral',
            address='Rua das Flores, 123',
            phone='33999190106'
        )
        
        self.authenticate()
        
        detail_url = reverse('healthcareworkers_detail', kwargs={'pk': worker.id})
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Dr. João Silva')

    def test_update_healthcare_worker(self):
        """Testa atualização de profissional"""
        worker = HealthcareWorker.objects.create(
            name='Dr. João Silva',
            preferred_name='João',
            profession='Clínico Geral',
            address='Rua das Flores, 123',
            phone='33999190106'
        )
        
        self.authenticate()
        
        detail_url = reverse('healthcareworkers_detail', kwargs={'pk': worker.id})
        update_data = {
            'name': 'Dr. João Santos Silva',
            'profession': 'Cardiologista'
        }
        
        response = self.client.patch(detail_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        worker.refresh_from_db()
        self.assertEqual(worker.name, 'Dr. João Santos Silva')

    def test_delete_healthcare_worker(self):
        """Testa exclusão de profissional"""
        worker = HealthcareWorker.objects.create(
            name='Dr. João Silva',
            preferred_name='João',
            profession='Clínico Geral',
            address='Rua das Flores, 123',
            phone='33999190106'
        )
        
        self.authenticate()
        
        detail_url = reverse('healthcareworkers_detail', kwargs={'pk': worker.id})
        response = self.client.delete(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HealthcareWorker.objects.count(), 0)

    def test_name_validation(self):
        """Testa validação do nome"""
        self.authenticate()
        
        # Teste com nome válido
        data = self.valid_worker_data.copy()
        data['name'] = 'Dr. João Silva'
        
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Teste com nome inválido
        data['name'] = 'A'
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phone_validation(self):
        """Testa validação do telefone"""
        self.authenticate()
        
        # Teste com telefone válido
        data = self.valid_worker_data.copy()
        data['phone'] = '33999190106'
        
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Teste com telefone inválido
        data['phone'] = '123456789'
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_str_representation(self):
        """Testa representação string do modelo"""
        # Teste com preferred_name
        worker1 = HealthcareWorker.objects.create(
            name='Dr. João Silva',
            preferred_name='João',
            profession='Clínico Geral',
            address='Rua das Flores, 123',
            phone='33999190106'
        )
        
        self.assertEqual(str(worker1), 'João')
        
        # Teste sem preferred_name
        worker2 = HealthcareWorker.objects.create(
            name='Dra. Maria Santos',
            profession='Cardiologista',
            address='Av. Principal, 456',
            phone='33999290107'
        )
        
        self.assertEqual(str(worker2), 'Dra. Maria Santos')
