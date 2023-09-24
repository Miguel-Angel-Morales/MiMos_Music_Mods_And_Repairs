from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.ForeignKey(
        "Specialty", on_delete=models.CASCADE, related_name='assigned_specialty')

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
