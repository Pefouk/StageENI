from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render

from ENIVeille.forms import FormInscription, FormConnexion, FormEditProfil, FormSuppression
from ENIVeille.models import Utilisateur as User, Publication


def home(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Merci de vous connecter !')
        return redirect(connexion)
    publications = list(Publication.objects.all())
    return render(request, 'ENIVeille/home.html',
                  {'publications': publications, 'sauvegardes': sauvegarde(request.user.username)})


def supprimer(request, pseudo):
    if not request.user.is_superuser or request.user.username != pseudo:
        messages.info(request, 'Vous n\'avez pas accès a cette page !')
        return redirect(home)
    else:
        if request.method == 'POST':
            form = FormSuppression(request.POST)
            if form.is_valid() and form.data.get('pseudo') == pseudo:
                User.objects.filter(username=pseudo).delete()
                messages.success(request, 'Compte supprimé avec succés !')
                if pseudo == request.user.username:
                    logout(request)
                return redirect(home)
            else:
                messages.warning(request, 'Pseudo incorrect !')
        else:
            form = FormSuppression()
        return render(request, 'ENIVeille/user/suppression.html', {'form': form, 'pseudo': pseudo})


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


def sauvegarde(username):
    sauvegardes = list(User.objects.filter(username__exact=username).get().sauvegarde.all())
    return sauvegardes
