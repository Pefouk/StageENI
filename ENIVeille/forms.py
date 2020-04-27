from crispy_forms.helper import FormHelper
from django import forms


class FormConnexion(forms.Form):
    pseudo = forms.CharField(
        required=True,
        label="Pseudo :",
    )
    motDePasse = forms.CharField(
        label="Mot de passe :",
        required=True,
        max_length=32,
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super(FormConnexion, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'connexion'
        self.helper.form_method = 'post'
        self.helper.form_action = 'connexion'
