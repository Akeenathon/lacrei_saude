from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import HealthcareWorker
from .serializers import HealthcareWorkerSerializer
import logging


logger = logging.getLogger('api')


class HealthcareWorkersListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HealthcareWorkerSerializer

    def get_queryset(self):
        queryset = HealthcareWorker.objects.all().order_by('name')
        
        # Log de acesso
        logger.info(f"Usuário {self.request.user.username} acessou lista de profissionais")
        
        # Busca simples
        search = self.request.query_params.get('search')
        if search:
            logger.info(f"Busca por: {search}")
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(profession__icontains=search)
            )
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Usuário {request.user.username} criando novo profissional")
        
        # Validação básica
        if not request.data:
            return Response(
                {'error': 'Dados não fornecidos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se nome está vazio
        if not request.data.get('name'):
            return Response(
                {'error': 'Nome é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se telefone está vazio
        if not request.data.get('phone'):
            return Response(
                {'error': 'Telefone é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Profissional criado com sucesso: {response.data.get('name')}")
            return response
        except Exception as e:
            logger.error(f"Erro ao criar profissional: {str(e)}")
            return Response(
                {'error': 'Erro ao criar profissional'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class HealthcareWorkersRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer
    
    def retrieve(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Usuário {request.user.username} visualizou profissional ID: {professional_id}")
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Usuário {request.user.username} atualizando profissional ID: {professional_id}")
        
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(f"Profissional {professional_id} atualizado com sucesso")
            return response
        except Exception as e:
            logger.error(f"Erro ao atualizar profissional: {str(e)}")
            return Response(
                {'error': 'Erro ao atualizar profissional'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Usuário {request.user.username} deletando profissional ID: {professional_id}")
        
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"Profissional {professional_id} deletado com sucesso")
            return response
        except Exception as e:
            logger.error(f"Erro ao deletar profissional: {str(e)}")
            return Response(
                {'error': 'Erro ao deletar profissional'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
