from unittest.test.test_result import __init__

from crispy_forms.helper import FormHelper
from django import forms

from ENIVeille.models import Technologie, Categorie


# FORM PROFILS/UTILISATEURS

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


class FormSuppression(forms.Form):
    pseudo = forms.CharField(
        required=True,
        label="Le pseudo du profil a supprimer :",
        min_length=3,
        max_length=25,
    )

    def __init__(self, *args, **kwargs):
        super(FormSuppression, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'suppression'
        self.helper.form_method = 'post'
        self.helper.form_action = 'suppression'


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


# FORMS PUBLICATION

DATE_INPUT_FORMATS = ['%d/%m/%Y']


class FormNouvellePublication(forms.Form):
    titre = forms.CharField(
        required=True,
        label="Titre :",
        min_length=3,
        max_length=255,
    )
    description = forms.CharField(
        required=True,
        label="Description :",
        min_length=20,
        max_length=255
    )
    contenu = forms.CharField(
        required=True,
        label="Contenu de l'actualité :",
        min_length=20,
        max_length=50000
    )
    source = forms.URLField(
        required=True,
        label="Source :",
        min_length=5,
        max_length=500
    )
    date = forms.DateField(
        required=True,
        label="Date de l'actualité :",
        widget=forms.SelectDateWidget
    )
    categorie = forms.ModelChoiceField(
        required=True,
        label="Catégorie de l'actualité :",
        queryset=Categorie.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(FormNouvellePublication, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


# FORMS ADMINISTRATEURS/TECHNOLOGIES

class FormCreerTechnologie(forms.Form):
    titre = forms.CharField(
        required=True,
        label="Titre ",
        min_length=2,
        max_length=255
    )
    description = forms.CharField(
        required=True,
        label="Description ",
        min_length=20,
        max_length=5000,
        widget=forms.TextInput
    )
    wiki = forms.URLField(
        required=True,
        label="Lien wikipedia",
        min_length=1,
        max_length=50
    )
    image = forms.URLField(
        required=True,
        label="Lien du logo ",
        min_length=1,
        max_length=500
    )

    def __init__(self, *args, **kwargs):
        super(FormCreerTechnologie, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'creation'
        self.helper.form_method = 'post'
        self.helper.form_action = 'creation'


class FormSuppressionTechnologie(forms.Form):
    pseudo = forms.CharField(
        required=True,
        label="Le titre de la technologie a supprimer :",
        min_length=3,
        max_length=25,
    )

    def __init__(self, *args, **kwargs):
        super(FormSuppressionTechnologie, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'suppression'
        self.helper.form_method = 'post'
        self.helper.form_action = 'suppression'


class FormSuppressionCategorie(forms.Form):
    pseudo = forms.CharField(
        required=True,
        label="Titre :",
        min_length=3,
        max_length=25,
    )

    def __init__(self, *args, **kwargs):
        super(FormSuppressionCategorie, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'suppression'
        self.helper.form_method = 'post'
        self.helper.form_action = 'suppression'
