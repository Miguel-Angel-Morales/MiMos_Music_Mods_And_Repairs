from django.db import models

class ServiceTicket(models.Model):
  
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    instrument = models.ForeignKey("Instrument", on_delete=models.CASCADE)
    description = models.CharField(max_length=20000, default="")
    notes = models.CharField(max_length=20000, default="")
    date = models.DateField(auto_now=False, auto_now_add=False)
    modification = models.BooleanField(default=False)  # Default value can be True or False
    repair = models.BooleanField(default=False)
    setup = models.BooleanField(default=False)
    priority = models.BooleanField(default=False)