from django import forms
from .models import Address, Organization, Server, Student, City

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

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['code', 'name', 'phone', 'email', 'gender', 'photo', 'organization', 'active']

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'phone', 'email', 'role', 'organization', 'active']

        