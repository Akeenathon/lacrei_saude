from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.utils.html import escape
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
        logger.info(f"Usuário {self.request.user.id} ({self.request.user.username}) acessou lista de profissionais")
        
        # Sanitização do parâmetro search
        search = self.request.query_params.get('search')
        if search:
            search = escape(search.strip())
            
            # Valida tamanho do input
            if len(search) > 100:
                logger.warning(f"Busca muito longa rejeitada: {search[:50]}...")
                return queryset.none()
            
            # Log da busca
            logger.info(f"Busca realizada por usuário {self.request.user.id}: {search}")
            
            # Busca segura usando Django ORM
            try:
                professional_id = int(search)
                queryset = queryset.filter(
                    Q(id=professional_id) |
                    Q(name__icontains=search) |
                    Q(preferred_name__icontains=search) |
                    Q(profession__icontains=search)
                )
            except ValueError:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(preferred_name__icontains=search) |
                    Q(profession__icontains=search) |
                    Q(email__icontains=search)
                )
        
        return queryset
    
    # Override para adicionar logs de criação
    def create(self, request, *args, **kwargs):
        logger.info(f"Usuário {request.user.id} ({request.user.username}) tentando criar novo profissional")
        
        try:
            # Validação extra dos dados
            if not request.data:
                logger.warning(f"Tentativa de criação sem dados por usuário {request.user.id}")
                return Response(
                    {'error': 'Dados não fornecidos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validação de campos obrigatórios
            required_fields = ['name', 'profession', 'address', 'phone']
            missing_fields = []
            
            for field in required_fields:
                if not request.data.get(field):
                    missing_fields.append(field)
            
            if missing_fields:
                logger.warning(f"Campos obrigatórios ausentes: {', '.join(missing_fields)}")
                return Response(
                    {'error': f'Campos obrigatórios: {", ".join(missing_fields)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            response = super().create(request, *args, **kwargs)
            
            # Log de sucesso
            logger.info(f"Profissional criado com sucesso por usuário {request.user.id}: ID {response.data.get('id')}")
            return response
            
        except Exception as e:
            # Log de erro
            logger.error(f"Erro ao criar profissional para usuário {request.user.id}: {str(e)}")
            return Response(
                {'error': 'Erro interno do servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HealthcareWorkersRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HealthcareWorker.objects.all()
    serializer_class = HealthcareWorkerSerializer
    
    # Log de visualização
    def retrieve(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Usuário {request.user.id} visualizou profissional ID: {professional_id}")
        
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro ao visualizar profissional {professional_id}: {str(e)}")
            return Response(
                {'error': 'Profissional não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Log de atualização
    def update(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.info(f"Usuário {request.user.id} atualizou profissional ID: {professional_id}")
        
        try:
            # Validação extra dos dados
            if not request.data:
                logger.warning(f"Tentativa de atualização sem dados por usuário {request.user.id}")
                return Response(
                    {'error': 'Dados não fornecidos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            response = super().update(request, *args, **kwargs)
            logger.info(f"Profissional {professional_id} atualizado com sucesso")
            return response
            
        except Exception as e:
            logger.error(f"Erro ao atualizar profissional {professional_id}: {str(e)}")
            return Response(
                {'error': 'Erro interno do servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # Log de exclusão
    def destroy(self, request, *args, **kwargs):
        professional_id = kwargs.get('pk')
        logger.warning(f"Usuário {request.user.id} deletou profissional ID: {professional_id}")
        
        try:
            # Verificar se profissional tem consultas associadas
            instance = self.get_object()
            if hasattr(instance, 'medicalconsultation_set') and instance.medicalconsultation_set.exists():
                logger.warning(f"Tentativa de deletar profissional {professional_id} com consultas associadas")
                return Response(
                    {'error': 'Não é possível deletar profissional com consultas associadas'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"Profissional {professional_id} deletado com sucesso")
            return response
            
        except Exception as e:
            logger.error(f"Erro ao deletar profissional {professional_id}: {str(e)}")
            return Response(
                {'error': 'Erro interno do servidor'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )