from django import forms
<<<<<<< HEAD
from .models import Address, Organization, Student, City
=======
from .models import Address, Organization, City
>>>>>>> 4c39874e420e0759272f3da8c8317543df187f22

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
<<<<<<< HEAD
        fields = ['name', 'phone', 'email', 'active']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['code', 'name', 'phone', 'email', 'gender', 'photo', 'organization', 'active']
        
=======
        fields = ['name', 'phone', 'email', 'active']
>>>>>>> 4c39874e420e0759272f3da8c8317543df187f22
