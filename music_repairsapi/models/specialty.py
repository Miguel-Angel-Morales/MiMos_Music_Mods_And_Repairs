from django.db import models

class Specialty(models.Model):
    specialty_name = models.CharField(max_length=55)