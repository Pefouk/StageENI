from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'ENIVeille/home.html', locals())
    return redirect(connexion)


def connexion(request):
    print(request.path)
    return render(request, 'ENIVeille/login.html', locals())


def deconnexion(request):
    alert = 1
    alert_type = 'danger'
    alert_msg = 'Vous êtes désormais déconecté ' + request.user.username + " !"
    logout(request)
    return render(request, 'ENIVeille/login.html', locals())
