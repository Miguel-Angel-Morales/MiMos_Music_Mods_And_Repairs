from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.ForeignKey("Specialty", on_delete=models.CASCADE, related_name='assigned_specialty')
    first_name= models.CharField(max_length=255, default="Employee_First_Name")
    last_name= models.CharField(max_length=255, default="Employee_Last_Name")
