from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import FormInscription, FormConnexion, FormEditProfil
from .models import Publication, Technologie, Utilisateur as User


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    publications = list(Publication.objects.all())
    sauvegardes = list(User.objects.filter(username__exact=request.user.username).get().sauvegarde.all())
    return render(request, 'ENIVeille/home.html', {'publications': publications, 'sauvegardes': sauvegardes})


def connexion(request):
    if request.method == 'POST':
        form = FormConnexion(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data.get('pseudo'), password=form.data.get('motDePasse'))
            if user is not None:
                login(request, user)
                messages.success(request, "Bienvenue " + user.username + " !")
                return redirect(home)
            else:
                messages.warning(request, "Combinaison pseudo et mot de passe incorrect !")
    else:
        form = FormConnexion()
    if request.user.is_authenticated:
        return redirect(home)
    return render(request, 'ENIVeille/user/login.html', {'form': form})


def deconnexion(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Vous êtes déja deconnecté !')
    else:
        logout(request)
    return redirect(connexion)


def inscription(request):
    if request.method == 'POST':
        form = FormInscription(request.POST)
        if form.is_valid and form.data.get('email') == form.data.get('emailConfirmation') and form.data.get(
                'motDePasseConfimation') == form.data.get('motDePasse'):
            try:
                user = User.objects.create_user(username=form.data.get('pseudo'), email=form.data.get('email'),
                                                password=form.data.get('motDePasse'))
                user.first_name = form.data.get('prenom')
                user.last_name = form.data.get('nom')
                user.save()
                login(request, user)
                return redirect(home)
            except IntegrityError:
                messages.error(request, "Email ou pseudo déja utilisé !")
                pass
        else:
            messages.info(request, 'Formulaire invalide')
    else:
        form = FormInscription()
    return render(request, 'ENIVeille/user/register.html', {'form': form})


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
    return render(request, 'ENIVeille/technologie.html',
                  {'techno': techno, 'publications': list(techno.publication_set.all()), 'sauvegardes': sauvegardes})


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


def profil(request, pseudo):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    if not User.objects.filter(username__exact=pseudo).exists():
        messages.info(request, 'Profil inexistant !')
        return redirect(home)
    user = User.objects.filter(username__exact=pseudo).get()
    return render(request, 'ENIVeille/user/profil.html', {'user': user})


def editprofil(request, pseudo):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    if request.user.username != pseudo and not request.user.is_superuser:
        messages.info(request, 'Vous ne pouvez pas modifier le profil de quelqu\'un d\'autre !')
        return redirect(home)
    if not User.objects.filter(username__exact=pseudo).exists():
        messages.info(request, 'Profil inexistant !')
        return redirect(home)
    user = User.objects.filter(username__exact=pseudo).get()
    if request.method == 'POST':
        form = FormEditProfil(request.POST)
        if form.is_valid and form.data.get('email') == form.data.get('emailConfirmation'):
            try:
                user.username = form.data.get('pseudo')
                user.first_name = form.data.get('nom')
                user.last_name = form.data.get('prenom')
                user.email = form.data.get('email')
                user.save()
                messages.success(request, 'Mise a jour du profil effectuée !')
                return redirect(profil, user.username)
            except:
                messages.error(request, 'Mise a jour du profil echouée !')
                return redirect(profil, pseudo)
        else:
            messages.error(request, 'Formulaire invalide !')
    else:
        form = FormEditProfil(initial={'prenom': user.last_name, 'pseudo': user.username, 'email': user.email,
                                       'emailConfirmation': user.email, 'nom': user.first_name})
        form.pseudo = user.username
        form.prenom = user.last_name
    return render(request, 'ENIVeille/user/editprofil.html', {'form': form, 'user': user})


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
