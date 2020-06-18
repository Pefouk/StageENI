from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from ENIVeille.forms import FormSuppressionTechnologie, FormCreerTechnologie, FormSuppressionCategorie
from ENIVeille.views import user, publications
from ENIVeille.models import Utilisateur, Technologie, Categorie


def categories(request, technologie):
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    return render(request, 'ENIVeille/admin/categories.html',
                  {'categories': list(Categorie.objects.filter(technologie__titre__exact=technologie).all()),
                   'technologie': technologie})


def creer_categorie(request, technologie):
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    else:
        if request.method == 'POST':
            form = FormSuppressionCategorie(request.POST)
            if form.is_valid():
                try:
                    categorie = Categorie.objects.create(nom=form.data.get('pseudo'),
                                                         titre=1,
                                                         description=1,
                                                         date=1,
                                                         source=1,
                                                         video=1,
                                                         technologie=Technologie.objects.filter(
                                                             titre=technologie).get())
                    categorie.save()
                    messages.success(request, categorie.nom + ' à été créée avec succès !')
                    return redirect(home)
                except Exception as e:
                    print(e)
                    messages.warning(request,
                                     'Erreur lors de la création de la catégorie ! Êtes vous sur de tous les champs '
                                     'du formulaire ?')
            else:
                messages.warning(request, 'Formulaire invalide !')
        else:
            form = FormSuppressionCategorie()
        return render(request, 'ENIVeille/admin/creer_categorie.html', {'form': form, 'technologie': technologie})


def supprimer_categorie(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    else:
        categorie = Categorie.objects.filter(id=id).get()
        if request.method == 'POST':
            form = FormSuppressionCategorie(request.POST)
            if form.is_valid() and form.data.get('pseudo') == categorie.nom:
                categorie.delete()
                messages.success(request, 'Catégorie supprimé avec succés !')
                return redirect(home)
            else:
                messages.warning(request, 'Nom de la catégorie incorrect !')
        else:
            form = FormSuppressionCategorie()
        return render(request, 'ENIVeille/admin/supprimer_categorie.html', {'categorie': categorie, 'form': form})


def supprimer_technologie(request, technologie):
    utilisateur = Utilisateur.objects.filter(username__exact=request.user.username).get()
    if not (request.user.is_authenticated and (
            request.user.is_superuser or utilisateur.moderation.filter(technologie=technologie).exists())):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    else:
        if request.method == 'POST':
            form = FormSuppressionTechnologie(request.POST)
            if form.is_valid() and form.data.get('pseudo') == technologie:
                Technologie.objects.filter(titre=technologie).delete()
                messages.success(request, 'Technologie supprimé avec succés !')
                return redirect(home)
            else:
                messages.warning(request, 'Nom de la technologie incorrect !')
        else:
            form = FormSuppressionTechnologie()
        return render(request, 'ENIVeille/admin/supprimer_technologie.html', {'technologie': technologie, 'form': form})


def modifier_technologie(request, titre):
    utilisateur = Utilisateur.objects.filter(username__exact=request.user.username).get()
    if not (request.user.is_authenticated and (
            request.user.is_superuser or utilisateur.moderation.filter(technologie=titre).exists())):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    else:
        technologie = Technologie.objects.filter(titre__exact=titre).get()
        if request.method == 'POST':
            form = FormCreerTechnologie(request.POST)
            if form.is_valid():
                try:
                    technologie.titre = form.data.get('titre')
                    technologie.description = form.data.get('description')
                    technologie.wiki = form.data.get('wiki')
                    technologie.image = form.data.get('image')
                    technologie.save()
                    messages.success(request, 'Mise a jour de ' + technologie.titre + ' réussie !')
                    return redirect(publications.technologie, nomtechno=technologie.titre)
                except Exception as e:
                    print(e)
                    messages.error(request, 'Erreur lors du traitement du formulaire, êtes vous sur de tous les '
                                            'champs remplis ?')
        else:
            form = FormCreerTechnologie(initial={
                'titre': technologie.titre,
                'wiki': technologie.wiki,
                'image': technologie.image,
                'description': technologie.description
            })
        return render(request, 'ENIVeille/admin/modifier_technologie.html',
                      {'technologie': technologie, 'form': form})


def creer_technologie(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    else:
        if request.method == 'POST':
            form = FormCreerTechnologie(request.POST)
            if form.is_valid():
                try:
                    technologie = Technologie.objects.create(titre=form.data.get('titre'),
                                                             description=form.data.get('description'),
                                                             wiki=form.data.get('wiki'),
                                                             image=form.data.get('image'))
                    technologie.save()
                    categorie = Categorie.objects.create(nom="General",
                                                         titre=1,
                                                         description=1,
                                                         date=1,
                                                         source=1,
                                                         video=1,
                                                         technologie=technologie)
                    categorie.save()
                    messages.success(request, technologie.titre + ' à été créée avec succès !')
                    return redirect(user.home)
                except Exception as e:
                    print(e)
                    messages.warning(request,
                                     'Erreur lors de la création de la technologie ! Êtes vous sur de tous les champs '
                                     'du formulaire ?')
            else:
                messages.warning(request, 'Formulaire invalide !')
        else:
            form = FormCreerTechnologie
        return render(request, 'ENIVeille/admin/creer_technologie.html', {'form': form})


def home(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    return render(request, 'ENIVeille/admin/home.html')


def technologies(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    return render(request, 'ENIVeille/admin/technologies.html', {'technologies': list(Technologie.objects.all())})


def utilisateurs(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.warning(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(user.home)
    return render(request, 'ENIVeille/admin/utilisateurs.html', {'utilisateurs': list(Utilisateur.objects.all())})
