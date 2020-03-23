from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES
from .models import Profile

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class SignUpForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields =  ('title','first_name','last_name','gender', 'phone', 'mobile', 'email', 'alt_email', 'institution', 'nationality')


class UserInformationUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields =  ('title','first_name','last_name','gender', 'phone', 'mobile', 'email', 'alt_email', 'institution', 'nationality')
