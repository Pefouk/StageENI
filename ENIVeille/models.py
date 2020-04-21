from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class Technologie(models.Model):
    titre = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    wiki = models.URLField(max_length=50)

    class Meta:
        verbose_name = "technologie"
        ordering = ['titre']

    def __str__(self):
        return self.titre


class Categorie(models.Model):
    nom = models.CharField(max_length=25)
    titre = models.BooleanField()
    description = models.BooleanField()
    date = models.BooleanField()
    source = models.BooleanField()
    video = models.BooleanField()
    technologie = models.ForeignKey(Technologie, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "categorie"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Publication(models.Model):
    titre = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    date = models.DateField()
    source = models.URLField(max_length=50)
    video = models.CharField(max_length=200, null=True)
    datePublication = models.DateField(default=timezone.now)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    technologie = models.ForeignKey(Technologie, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "publication"
        ordering = ['datePublication']

    def __str__(self):
        return self.titre


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lienAvatar = models.CharField(max_length=520)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    mailValidation = models.DateField(default=timezone.now)
    mailOublie = models.DateField(null=True)
    actif = models.BooleanField(default=False)
    administrateur = models.BooleanField(default=False)
    moderation = models.ManyToManyField(Technologie, related_name="moderateur")
    abonnement = models.ManyToManyField(Technologie, related_name="abonné")
    sauvegarde = models.ManyToManyField(Publication)

    class Meta:
        verbose_name = "utilisateur"
        ordering = ['nom']

    def __str__(self):
        return self.nom + " " + self.prenom
