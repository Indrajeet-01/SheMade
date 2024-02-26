from django.db import models
from django.core.validators import RegexValidator

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10,validators=[RegexValidator(r'^\d{10}$', message='Phone number must be 10 digits')])
    email = models.EmailField()
    message = models.TextField(blank=True)
    def __str__(self):
        return self.name
    

class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email 
