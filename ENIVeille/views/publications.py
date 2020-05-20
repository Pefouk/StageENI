from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from ENIVeille.models import Publication, Technologie, Utilisateur as User
from ENIVeille.views.user import connexion, home


def listetechnologies(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    technologies = list(Technologie.objects.all())
    return render(request, 'ENIVeille/technologieliste.html', {'technologies': technologies})


def technologie(request, nomtechno):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    if Technologie.objects.filter(titre__exact=nomtechno).exists():
        techno = Technologie.objects.filter(titre__exact=nomtechno).get()
    else:
        messages.error(request, "Technologie non existante !")
        return redirect(home)
    sauvegardes = list(User.objects.filter(username__exact=request.user.username).get().sauvegarde.all())
    user = User.objects.filter(username__exact=request.user.username).get()
    if user.abonnement.filter(titre__exact=techno.titre).exists():
        abonne = 0
    else:
        abonne = 1
    return render(request, 'ENIVeille/technologie.html',
                  {'techno': techno, 'publications': list(techno.publication_set.all()), 'sauvegardes': sauvegardes,
                   'abonne': abonne})


def publication(request, idpublication, nomtechno):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    if Publication.objects.filter(technologie__titre__exact=nomtechno, id=idpublication).exists():
        post = Publication.objects.filter(technologie__titre__exact=nomtechno, id=idpublication).get()
    else:
        messages.error(request, "Publication inexistante !")
        return redirect(home)
    return render(request, 'ENIVeille/publication.html',
                  {'publication': post})


def sauvegarde(username):
    sauvegardes = list(User.objects.filter(username__exact=username).get().sauvegarde.all())
    return sauvegardes
