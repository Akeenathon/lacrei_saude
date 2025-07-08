from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.utils.html import escape
from rest_framework.exceptions import ValidationError
from .models import MedicalConsultation
from .serializers import MedicalConsultationSerializer
import logging


logger = logging.getLogger('api')


class MedicalConsultationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MedicalConsultationSerializer

    def get_queryset(self):
        queryset = MedicalConsultation.objects.all().order_by('-consultation_date')

        logger.info(f"Usuário {self.request.user.id} ({self.request.user.username}) acessou lista de consultas")

        search = self.request.query_params.get('search')
        if search:
            search = escape(search.strip())
            if len(search) > 100:
                logger.warning(f"Busca muito longa rejeitada: {search[:50]}...")
                return queryset.none()

            logger.info(f"Busca realizada por usuário {self.request.user.id}: {search}")

            try:
                doctor_id = int(search)
                queryset = queryset.filter(
                    Q(healthcare_worker__id=doctor_id) |
                    Q(healthcare_worker__name__icontains=search) |
                    Q(healthcare_worker__preferred_name__icontains=search)
                )
            except ValueError:
                queryset = queryset.filter(
                    Q(healthcare_worker__name__icontains=search) |
                    Q(healthcare_worker__preferred_name__icontains=search)
                )

        return queryset

    def create(self, request, *args, **kwargs):
        logger.info(f"Usuário {request.user.id} ({request.user.username}) tentando criar nova consulta")

        if not request.data:
            logger.warning(f"Tentativa de criação sem dados por usuário {request.user.id}")
            return Response(
                {'error': 'Dados não fornecidos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Consulta criada com sucesso por usuário {request.user.id}: ID {response.data.get('id')}")
            return response

        except ValidationError as e:
            logger.warning(f"Validação falhou ao criar consulta por usuário {request.user.id}: {e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Erro ao criar consulta para usuário {request.user.id}: {str(e)}")
            return Response(
                {'error': 'Erro interno do servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MedicalConsultationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MedicalConsultation.objects.all()
    serializer_class = MedicalConsultationSerializer

    def retrieve(self, request, *args, **kwargs):
        consultation_id = kwargs.get('pk')
        logger.info(f"Usuário {request.user.id} visualizou consulta ID: {consultation_id}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        consultation_id = kwargs.get('pk')
        logger.info(f"Usuário {request.user.id} atualizou consulta ID: {consultation_id}")

        try:
            response = super().update(request, *args, **kwargs)
            logger.info(f"Consulta {consultation_id} atualizada com sucesso")
            return response

        except ValidationError as e:
            logger.warning(f"Validação falhou ao atualizar consulta {consultation_id} por usuário {request.user.id}: {e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Erro ao atualizar consulta {consultation_id}: {str(e)}")
            return Response(
                {'error': 'Erro interno do servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        consultation_id = kwargs.get('pk')
        logger.warning(f"Usuário {request.user.id} deletou consulta ID: {consultation_id}")

        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f"Consulta {consultation_id} deletada com sucesso")
            return response

        except Exception as e:
            logger.error(f"Erro ao deletar consulta {consultation_id}: {str(e)}")
            return Response(
                {'error': 'Erro interno do servidor'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
