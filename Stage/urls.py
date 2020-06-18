from django.contrib import admin
from django.urls import path

from ENIVeille.views import publications, ajax, user, admin

urlpatterns = [
    # Back office
    path('admin', admin.home, name="admin"),
    path('admin/utilisateurs', admin.utilisateurs, name="admin_utilisateurs"),
    path('admin/<pseudo>/admin', ajax.admin, name="admin_utilisateurs_admin"),
    path('admin/technologies', admin.technologies, name="admin_technologies"),
    path('admin/nouvelleTechnologie', admin.creer_technologie, name="admin_creer_technologie"),
    path('admin/<technologie>/supprimer', admin.supprimer_technologie, name="admin_supprimer_technologie"),
    path('admin/<technologie>/categories', admin.categories, name="admin_liste_categories"),
    path('admin/<technologie>/categorie/nouvelle', admin.creer_categorie, name="admin_creer_categorie"),
    path('admin/categorie/supprimer/<id>', admin.supprimer_categorie, name="admin_supprimer_categorie"),

    # Page d'accueil
    path('', publications.home, name="home"),

    # Gestion profil
    path('connexion', user.connexion, name="connexion"),
    path('deconnexion', user.deconnexion, name="deconnexion"),
    path('inscription', user.inscription, name="inscription"),
    path('u/<pseudo>', user.profil, name="profil"),
    path('u/<pseudo>/supprimer', user.supprimer, name="supprimerprofil"),
    path('edit/u/<pseudo>', user.editprofil, name="editprofil"),
    path('sauvegarder/<pseudo>/<idpublication>', ajax.sauvegarder, name="sauvegarder"),

    # Technologie et publications
    path('technologies', publications.liste_technologies, name="listetechnologies"),
    path('t/<titre>', publications.technologie, name="technologie"),
    path('t/<titre>/p/<idpublication>', publications.publication, name="publication"),
    path('t/<technologie>/abonnement', ajax.sabonner, name="sabonne"),
    path('t/<titre>/modifier', admin.modifier_technologie, name="modifier_technologie"),
    path('t/<titre>/nouveau', publications.nouvelle_publication_techno, name="nouvelle_publication"),

    # Onglets page d'accueil
    path('contenuSauvegarde', ajax.contenusauvegarde, name="contenuSauvegarde"),
    path('contenuTout', ajax.tout, name="contenuTout"),
    path('contenuAbonne', ajax.contenuabonne, name="contenuAbonne"),
]
