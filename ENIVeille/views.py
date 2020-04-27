from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'ENIVeille/home.html', locals())
    messages.info(request, 'Merci de vous connecter !')
    return redirect(connexion)


def connexion(request):
    return render(request, 'ENIVeille/login.html', locals())


def deconnexion(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Vous êtes déja deconnecté !')
    else:
        messages.info(request, 'Vous êtes désormais deconnecté !')
    logout(request)
    return render(request, 'ENIVeille/login.html', locals())
