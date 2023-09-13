from django.db import models

class Instrument(models.Model):
    instrument_name = models.CharField(max_length=55)