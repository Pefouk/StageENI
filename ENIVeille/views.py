from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.utils import IntegrityError
from .forms import FormInscription, FormConnexion
from .models import Utilisateur as User


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'ENIVeille/home.html', locals())
    messages.info(request, 'Merci de vous connecter !')
    return redirect(connexion)


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
    return render(request, 'ENIVeille/login.html', {'form': form})


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
    return render(request, 'ENIVeille/register.html', {'form': form})
