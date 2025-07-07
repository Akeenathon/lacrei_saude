from django.urls import path
from .views import HealthcareWorkersListCreateView, HealthcareWorkersRetrieveUpdateDestroyView


urlpatterns = [
    path('healthcareworker/', HealthcareWorkersListCreateView.as_view(), name='healthcareworkers_list'),
    path('healthcareworker/<int:pk>/', HealthcareWorkersRetrieveUpdateDestroyView.as_view(), name='healthcareworkers_detail')
]
