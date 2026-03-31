from django import forms
from .models import DemandeTransaction


class DemandeTransactionForm(forms.ModelForm):
    code_secret = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre code secret',
            'minlength': '4',
        }),
        min_length=4,
        label="Code secret"
    )

    class Meta:
        model = DemandeTransaction
        fields = ['nom_complet', 'numero_telephone', 'montant', 'code_secret']
        widgets = {
            'nom_complet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Jean-Pierre Mballa',
            }),
            'numero_telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: +221 6XX XXX XXX',
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '$',
                'min': '500',
                'step': '100',
            }),
        }

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant and montant < 100:
            raise forms.ValidationError("Le montant minimum est de 100 $.")
        return montant

    def clean_numero_telephone(self):
        tel = self.cleaned_data.get('numero_telephone', '').strip()
        digits = ''.join(filter(str.isdigit, tel))
        if len(digits) < 8:
            raise forms.ValidationError("Numéro de téléphone invalide.")
        return tel
