from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
#from phonenumber_field.modelfields import PhoneNumberField


class Activation(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     created_at = models.DateTimeField(auto_now_add=True)
     code = models.CharField(max_length=20, unique=True)
     email = models.EmailField(blank=True)




class sign_up(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class newsletter(models.Model):

    email = models.EmailField(max_length=70)
    full_name = models.CharField(max_length=70)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name,self.email

    


# Create your models here.
