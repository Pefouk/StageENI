import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Technologie(models.Model):
    titre = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    wiki = models.URLField(max_length=50)
    image = models.URLField(max_length=500, default="https://i.imgur.com/cy81Ptj.jpg")

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
    date = models.DateField(default=datetime.date.today)
    source = models.URLField(max_length=50)
    video = models.CharField(max_length=200, null=True)
    datePublication = models.DateField(default=datetime.date.today)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    technologie = models.ForeignKey(Technologie, on_delete=models.CASCADE)
    image = models.URLField(null=True)
    contenu = models.TextField(max_length=12000, default="Locati fecisse de quis amici amicitia excusatio rem ut excusatio oporteat in ut longe prospicere turpes de spatio prospicere Fanni curriculoque se loco longe aliquantum consuetudo consuetudo in eo sanciatur publicam contra nec Etenim ut causa rei quis est casus causa Deflexit amici in loco rogati contra nos turpes consuetudo Scaevola Etenim neque excusatio amici nec prospicere faciamus enim minime cum fateatur in spatio in longe Turpis cum cum Scaevola loco cum est et igitur nos amici maiorum Etenim rei sanciatur futuros nos se curriculoque futuros res aliquantum minime res nec peccatis aliquantum peccatis eo locati neque prospicere de in.")

    class Meta:
        verbose_name = "publication"
        ordering = ['-datePublication']

    def __str__(self):
        return self.titre


class Utilisateur(AbstractUser):
    lienAvatar = models.CharField(max_length=520)
    mailOublie = models.DateField(null=True, auto_now_add=True)
    moderation = models.ManyToManyField(Technologie, related_name="moderateur")
    abonnement = models.ManyToManyField(Technologie, related_name="abonné")
    sauvegarde = models.ManyToManyField(Publication)
    email = models.EmailField(blank=False, unique=True)
