from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('healthcare_workers.urls')),
    path('api/v1/', include('medical_consultation.urls')),
]
