from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Storage(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    amount = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.name
