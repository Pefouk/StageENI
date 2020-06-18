from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
import datetime

from ENIVeille.models import Publication, Technologie, Utilisateur as User, Categorie
from ENIVeille.views.user import connexion, home
from ENIVeille.forms import FormNouvellePublication


def liste_technologies(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    technologies = list(Technologie.objects.all())
    return render(request, 'ENIVeille/technologieliste.html', {'technologies': technologies})


def nouvelle_publication_techno(request, titre):
    if not (request.user.is_authenticated and (
            request.user.is_superuser or User.moderation.filter(technologie=titre).exists())):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(home)
    else:
        techno = Technologie.objects.filter(titre__exact=titre).get()
        if request.method == 'POST':
            form = FormNouvellePublication(request.POST)
            if form.is_valid():
                categorie = Categorie.objects.filter(id=3).get()
                print(form.data.get('date'))
                try:
                    actu = Publication.objects.create(
                        titre=form.data.get('titre'),
                        description=form.data.get('description'),
                        contenu=form.data.get('contenu'),
                        categorie=categorie,
                        source=form.data.get('source'),
                        technologie=techno
                    )
                    actu.save()
                    messages.success(request, 'Nouvelle actualité publiée !')
                    return redirect(publication, titre=titre, idpublication=actu.id)
                except Exception as e:
                    print(e)
                    messages.error(request, 'Erreur lors du traitement du formulaire, êtes vous sur de tous les '
                                            'champs remplis ?')
        else:
            form = FormNouvellePublication()
        return render(request, 'ENIVeille/publication/nouveau.html',
                      {'titre': titre, 'form': form})


def technologie(request, titre):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    if Technologie.objects.filter(titre__exact=titre).exists():
        techno = Technologie.objects.filter(titre__exact=titre).get()
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


def publication(request, idpublication, titre):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    if Publication.objects.filter(technologie__titre__exact=titre, id=idpublication).exists():
        post = Publication.objects.filter(technologie__titre__exact=titre, id=idpublication).get()
    else:
        messages.error(request, "Publication inexistante !")
        return redirect(home)
    return render(request, 'ENIVeille/publication.html',
                  {'publication': post})


def sauvegarde(username):
    sauvegardes = list(User.objects.filter(username__exact=username).get().sauvegarde.all())
    return sauvegardes
