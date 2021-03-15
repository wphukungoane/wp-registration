from django import forms
from django.contrib.auth.models import User
from .models import ProjectInfo


class NewProjectForm(forms.ModelForm):


	Project_Description = forms.CharField(
		widget=forms.Textarea(
			attrs={'rows': 5, 'placeholder': 'Description of your project or programme'}
		),
		max_length=4000,
		help_text='The max length of the text is 4000.'
	)

	def __init__(self, *args, **kwargs):
	  user = kwargs.pop('user','')
	  super(NewProjectForm, self).__init__(*args, **kwargs)
	  self.fields['Project_Name'].widget.attrs['placeholder'] = 'Preferred name for your project '
	  #self.fields['Project_Owner']=forms.ModelChoiceField(queryset= User.objects.filter(username=user))

	class Meta:
		model = ProjectInfo
		fields = [ 'Project_Owner','Project_Name','Research_Area','Project_Description']
		exclude = ['Project_Owner',]



#class BillingContactForm(forms.ModelForm):

#	def __init__(self, *args, **kwargs):
#	  super(BillingContactForm, self).__init__(*args, **kwargs)
#	  self.fields['contact_name'].widget.attrs['placeholder'] = 'Billing contact name'
#
#	class Meta:
#		model = BillingContact
#		fields = ['contact_name', 'address', 'region','city','country','postal_code']



class ComputeResourceForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
	  super(ComputeResourceForm, self).__init__(*args, **kwargs)

	class Meta:
		model = ProjectInfo
		fields = ['Number_CPU', 'Memory_required', 'Storage','OS_Type']
