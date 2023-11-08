from datetime import datetime
from django.db import models

# Create your models here.
class Item(models.Model):
    id_for = models.CharField(max_length=1000)

class Review(models.Model):
    rating = models.CharField(max_length=1000000)
    body = models.CharField(max_length=1000000)
    created_at = models.DateTimeField(default = datetime.now(), blank=True)
    user = models.CharField(max_length=1000000)
    id_for = models.CharField(max_length=1000000)