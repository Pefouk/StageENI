from django.http import JsonResponse
from django.shortcuts import render

from ENIVeille.models import Publication, Utilisateur as User, Technologie
from ENIVeille.views.publications import sauvegarde


def admin(request, pseudo):
    if not request.user.is_superuser:
        error = 1
        administrateur = 0
    else:
        error = 0
        utilisateur = User.objects.filter(username__exact=pseudo).get()
        if not utilisateur.is_superuser:
            utilisateur.is_staff = True
            utilisateur.is_superuser = True
            administrateur = 1
        else:
            utilisateur.is_staff = False
            utilisateur.is_superuser = False
            administrateur = 0
        utilisateur.save()
    response = {
        'admin': administrateur,
        'error': error
    }
    print(response)
    return JsonResponse(response)


def sauvegarder(request, pseudo, idpublication):
    if not request.user.username == pseudo:
        save = 0
        error = 1
    else:
        publi = Publication.objects.filter(id=idpublication).get()
        user = User.objects.filter(username__exact=pseudo).get()
        if user.sauvegarde.filter(id=publi.id).exists():
            user.sauvegarde.remove(publi)
            save = 0
        else:
            user.sauvegarde.add(publi)
            save = 1
        error = 0
    response = {
        'save': save,
        'error': error,
        'id': idpublication
    }
    return JsonResponse(response)


def contenusauvegarde(request):
    publications = list(Publication.objects.filter(utilisateur__username__exact=request.user.username).all())
    return render(request, 'ENIVeille/publication/publication.html',
                  {'publications': publications, 'sauvegardes': publications})


def tout(request):
    publications = list(Publication.objects.all())
    return render(request, 'ENIVeille/publication/publication.html',
                  {'publications': publications, 'sauvegardes': sauvegarde(request.user.username)})


def contenuabonne(request):
    publications = list(Publication.objects.filter(technologie__abonné__username=request.user.username).all())
    return render(request, 'ENIVeille/publication/publication.html',
                  {'publications': publications, 'sauvegardes': sauvegarde(request.user.username)})


def sabonner(request, technologie):
    user = User.objects.filter(username__exact=request.user).get()
    if not user.abonnement.filter(titre__exact=Technologie.objects.filter(titre__exact=technologie).get()).exists():
        user.abonnement.add(Technologie.objects.filter(titre__exact=technologie).get())
        abonnement = 1
    else:
        user.abonnement.remove(Technologie.objects.filter(titre__exact=technologie).get())
        abonnement = 0
    response = {
        'abonnement': abonnement
    }
    return JsonResponse(response)
