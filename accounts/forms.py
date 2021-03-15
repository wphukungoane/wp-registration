from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.data import COUNTRIES
from .models import Profile
from django.forms import ModelChoiceField
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions
from django.core.exceptions import ValidationError
from .validators import validate_email_unique

class UserForm(UserCreationForm):
	email = forms.EmailField(max_length=100,validators=[validate_email_unique] )
	class Meta:
		model = User
		fields = ('username','first_name','last_name', 'email','password1','password2' )

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		#disabling field help_text
		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None


class UserInformationUpdateForm(forms.ModelForm):
	email = forms.EmailField(label='Email Address')


	class Meta:
		model = Profile
		fields =  ('email','Current_Position','institution','address','region','Country','city','postal_code','phone', 'postal_code' )



class ContactForm(forms.Form):
	Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' Dr Marumo Sithole'}))
	email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'placeholder': ' someone@mail.com'}))
	Institutions = forms.CharField( required=False, label='Affiliated Organisation',  widget=forms.TextInput(attrs={'placeholder': ' Centre for High Performance Computing'}))
	message = forms.CharField(widget=forms.Textarea(
		attrs={'cols': 50, 'rows': 6 ,'placeholder': 'How can we assist you with...?'}))

	def __init__ (self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class = 'col-xs-12 col-md-6'

		self. helper.layout = Layout(
			HTML('''
			{% if messages %}
			{% for message in messages %}
			<p {% if message.tags %} class="alert alert-{{ message.tags }}"\
			{% endif %}>{{ message }}</p>{% endfor %}{% endif %}
			</p>
			'''),
			Fieldset(
				Field('Name'),
				Field('email'),
				Field('Institutions'),
				Field('message'),
			),
			FormActions(Submit('submit', 'Send', css_class='pull-right'))
		)
