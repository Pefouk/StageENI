from django.db import models
from django.utils import timezone


# Create your models here.

class Utilisateur(models.Model):
    motDePasse = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    lienAvatar = models.CharField()
    pseudo = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    mailValidation = models.DateField(default=timezone.now)
    mailOublie = models.DateField(null=True)
    actif = models.BooleanField(default=False)
    administrateur = models.BooleanField(default=False)