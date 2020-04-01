from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES
from .models import Profile
from django.forms import ModelChoiceField

#class UserForm(UserCreationForm):
#    class Meta:
#        model = User
	#    fields = ('username', 'password1','password2' )

class SignUpForm(UserCreationForm):
	TITLE_CHOICES = [
		('Mr',  'Mr'),
		('Mrs', 'Mrs'),
		('Miss','Miss'),
		('Dr',  'Dr'),
		('Prof','Prof'),
		('Rev', 'Rev'),
	]
	GENDER_CHOICES = [
		('male',        'male'),
		('female',      'female'),
		('unspecified', 'unspecified'),]
	INSTITUTIONS = [
	('UCT',  'University of Cape Town'),
	('UKZN', 'University of Kwazulu Natal'),
	('UP','University of Pretoria'),
	('UWC',  'University of the Western Cape'),
	('SUN','Stellenbosch University'),
	('Wits', 'University of Witwatersrand'),
	('UL',  'University of Limpopo'),
	('UJ', 'University of Johannesburg'),
	('TUT','Tshwane University of Technology'),
	('UNISA',  'University of South Africa'),
	('CPUT',' Cape Peninsula University of Technology'),
	('UNIVEN', 'University of Venda'),
	('DUT',  'Durban University of Technology'),
	('VUT', 'Vaal University of Technology'),
	('WSU','Walter Sisulu University'),
	('NMMU',  'Nelson Mandela University'),
	('SMU','Sefako Makgatho Health Sciences University'),
	('UMP', 'Mpumalanga University'),
	('SPO',  'Sol Plaatjie University'),
	('UJ', 'University of Johannesburg'),
	('UFS','University of the Free State'),
	('RU',  'Rhodes University'),
	('NWU',' North-West University'),
	('UFH', 'University of Fort Hare')]

	title = forms.ChoiceField(choices=TITLE_CHOICES)
	first_name = forms.CharField(max_length=15, )
	last_name = forms.CharField(max_length=15, )
	email = forms.EmailField(max_length=150)
	alt_email = forms.EmailField(max_length=150)
	phone = forms.CharField(max_length=15 )
	mobile = forms.CharField(max_length=15 )
	gender = forms.ChoiceField(choices=GENDER_CHOICES)
	#nationality = forms.CountryField(blank_label='(select country)')
	institution = forms.ChoiceField( choices=INSTITUTIONS)

	class Meta:
		model = User
		fields =  ('username', 'password1','password2','title','first_name','last_name','gender', 'phone', 'mobile', 'email', 'alt_email', 'institution')


class UserInformationUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields =  ('title','first_name','last_name','gender', 'phone', 'mobile', 'email', 'alt_email', 'institution', 'nationality')
