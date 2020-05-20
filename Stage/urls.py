from django.contrib import admin
from django.urls import path

from ENIVeille.views import publications, ajax, user

urlpatterns = [
    path(r'admin/', admin.site.urls, name="admin"),
    path('', publications.home, name="home"),
    path('connexion', user.connexion, name="connexion"),
    path('deconnexion', user.deconnexion, name="deconnexion"),
    path('inscription', user.inscription, name="inscription"),
    path('t/<nomtechno>', publications.technologie, name="technologie"),
    path('t/<nomtechno>/p/<idpublication>', publications.publication, name="publication"),
    path('technologies', publications.listetechnologies, name="listetechnologies"),
    path('u/<pseudo>', user.profil, name="profil"),
    path('edit/u/<pseudo>', user.editprofil, name="editprofil"),
    path('sauvegarder/<pseudo>/<idpublication>', ajax.sauvegarder, name="sauvegarder"),
    path('contenuSauvegarde', ajax.contenusauvegarde, name="contenuSauvegarde"),
    path('contenuTout', ajax.tout, name="contenuTout"),
    path('contenuAbonne', ajax.contenuabonne, name="contenuAbonne"),
    path('t/<technologie>/abonnement', ajax.sabonner, name="sabonne")
]
