from crispy_forms.helper import FormHelper
from django import forms


class FormConnexion(forms.Form):
    pseudo = forms.CharField(
        required=True,
        label="Pseudo :",
        min_length=3,
        max_length=25,
    )
    motDePasse = forms.CharField(
        label="Mot de passe :",
        required=True,
        max_length=32,
        widget=forms.PasswordInput,
        min_length=6,
    )

    def __init__(self, *args, **kwargs):
        super(FormConnexion, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'connexion'
        self.helper.form_method = 'post'
        self.helper.form_action = 'connexion'


class FormEditProfil(forms.Form):
    pseudo = forms.CharField(
        required=True,
        label="Pseudo :",
        min_length=3,
        max_length=25,
    )
    email = forms.EmailField(
        required=True,
        label="Adresse email :",
        max_length=255,
    )
    emailConfirmation = forms.EmailField(
        required=True,
        label="Confirmez votre adresse email :",
        max_length=255,
    )
    nom = forms.CharField(
        required=True,
        label="Nom :",
        max_length=25,
    )
    prenom = forms.CharField(
        required=True,
        label="Prenom :",
        max_length=25,
    )

    def __init__(self, *args, **kwargs):
        super(FormEditProfil, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class FormInscription(forms.Form):
    pseudo = forms.CharField(
        required=True,
        label="Pseudo :",
        min_length=3,
        max_length=25,
    )
    motDePasse = forms.CharField(
        label="Mot de passe :",
        required=True,
        max_length=32,
        widget=forms.PasswordInput,
        min_length=6,
    )
    motDePasseConfimation = forms.CharField(
        label="Confirmez votre mot de passe :",
        required=True,
        max_length=32,
        widget=forms.PasswordInput,
        min_length=6,
    )
    email = forms.EmailField(
        required=True,
        label="Adresse email :",
        max_length=255,
    )
    emailConfirmation = forms.EmailField(
        required=True,
        label="Confirmez votre adresse email :",
        max_length=255,
    )
    nom = forms.CharField(
        required=True,
        label="Nom :",
        max_length=25,
    )
    prenom = forms.CharField(
        required=True,
        label="Prenom :",
        max_length=25,
    )

    def __init__(self, *args, **kwargs):
        super(FormInscription, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'connexion'
        self.helper.form_method = 'post'
        self.helper.form_action = 'connexion'
