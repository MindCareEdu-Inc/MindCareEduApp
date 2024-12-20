from django import forms
from .models import Address, Organization, City

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'number', 'neighborhood', 'cep', 'complement', 'city', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Popula o campo de cidade com as cidades existentes
        self.fields['city'].queryset = City.objects.all()
        

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'phone', 'email', 'active']