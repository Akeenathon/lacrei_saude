from django.db import models


class HealthcareWorker(models.Model):
    name = models.CharField(max_length=60)
    preferred_name = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=50)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.preferred_name:
            return self.preferred_name
        else:
            return self.name
