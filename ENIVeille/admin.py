from django.contrib import admin

from .models import Publication, Technologie, Categorie, Utilisateur

# Register your models here.

admin.site.register(Categorie)
admin.site.register(Technologie)
admin.site.register(Publication)
admin.site.register(Utilisateur)
