from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from .forms import FormConnexion


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
    return render(request, 'ENIVeille/login.html', {'form': form})


def deconnexion(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Vous êtes déja deconnecté !')
    else:
        logout(request)
    return redirect(connexion)
