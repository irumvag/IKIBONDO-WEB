from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Myuser
        fields = ['phone_number', 'email', 'first_name', 'last_name','gender', 'Age', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set a default password
        if not user.password:
            user.set_password('umwana123')  # Set a default password here
        if commit:
            user.save()
        return user

    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    #role = forms.ChoiceField(choices=Myuser.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=Myuser.GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    Age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}))
    #password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    #password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone_number

class CHWCreationForm(forms.ModelForm):
    class Meta:
        model = CHW
        fields = ['LocationId', 'HID']

    LocationId = forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    HID = forms.ModelChoiceField(queryset=Hospital.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

class Addlocation(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['LocationId', 'Country', 'Provence', 'District', 'Village', 'Streetcode']

    LocationId = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location ID'}))
    Country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}))
    Provence = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter province'}))
    District = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter district'}))
    Village = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter village'}))
    Streetcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter streetcode (optional)'}))
