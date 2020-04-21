from django.contrib import admin

from .models import Profil, Publication, Technologie, Categorie

# Register your models here.

admin.site.register(Profil)
admin.site.register(Categorie)
admin.site.register(Technologie)
admin.site.register(Publication)
