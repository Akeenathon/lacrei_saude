from django.contrib import admin
from .models import HealthcareWorker


@admin.register(HealthcareWorker)
class HealthcareWorkersAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'preferred_name',
        'profession', 'phone', 'email',
        'created_at',
    )
    search_fields = (
        'name', 'preferred_name',
        'profession', 'phone',
    )
    list_filter = ('profession',)
    ordering = ('profession',)
    list_per_page = 20
