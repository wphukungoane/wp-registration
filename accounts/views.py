from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView,  DetailView
from .models import Profile
from django.views.generic.base import TemplateView
from .forms import UserInformationUpdateForm, UserForm, ContactForm
from .tables import AccountsTable
from django_tables2 import SingleTableView
from django.utils.html import escape
#email imports for contact form
import logging
from django.views.generic import TemplateView, FormView, View
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
#import mail setting for registrations.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage


logger = logging.getLogger(__name__)
# database home page view
@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
	model = Profile
	context_object_name = 'profiles'
	template_name = 'home.html'
	paginate_by = 4
	ordering = ['institution']

class SignUpView(View):
	user_form_class = UserForm
	profile_form_class = UserInformationUpdateForm
	template_name = "registration.html"
	success_urls = reverse_lazy('home')


	def get(self, request):

		# Here I make instances of my form classes and pass them None
		# which tells them that there is no additional data to display (errors, for example)
		user_form = self.user_form_class(None)
		profile_form = self.profile_form_class(None)
		# and then just pass them to my template
		return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

	def post(self, request,):

		user_form = self.user_form_class(request.POST)
		profile_form = self.profile_form_class(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)
			user_profile = profile_form.save(commit=False)
			user.is_active = False

			username = user_form.cleaned_data['username'].replace(' ', '').lower()
			password = user_form.cleaned_data['password1']


			user.first_name = user_form.cleaned_data['first_name']
			user.last_name = user_form.cleaned_data['last_name']
			user.email = user_form.cleaned_data['email']
			user.set_password(password)
			user.Profile = user_profile
			user.save()


				#Saving extra info from profile_form into Profile Model
			user.Profile.Current_Position = profile_form.cleaned_data['Current_Position']
			user.Profile.institution = profile_form.cleaned_data['institution']
			user.Profile.Country = profile_form.cleaned_data['Country']
			user.Profile.address = profile_form.cleaned_data['address']
			user.Profile.city = profile_form.cleaned_data['city']
			user.Profile.phone = profile_form.cleaned_data['phone']
			user.Profile.postal_code = profile_form.cleaned_data['postal_code']
			user.Profile.region = profile_form.cleaned_data['region']
			user.Profile.save()


			logger.info('New user signed up: %s (%s)', user, user.email)

			current_site = get_current_site(request)
			mail_subject = 'Activate CHPC OpenStackDB account.'
			message = render_to_string('acc_active_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),
				'token':account_activation_token.make_token(user),
				})
			to_email = user_form.cleaned_data.get('email')
			email = EmailMessage(
							mail_subject, message, to=[to_email]
				)
			email.send()
			messages.success(request, 'We have sent you an email, please confirm your email address to complete registration.')
				# Automatically authenticate the user after user creation.
				#user_auth = authenticate(username=username, password=password)
				#login(request, user_auth)
			#return HttpResponse('Please confirm your email address to complete the registration'
				#return redirect('home')

		return render(request, self.template_name, { 'user_form': user_form, 'profile_form': profile_form })

#Used to update user account
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

#Used by the Normal users to update their profile details
@method_decorator(login_required, name='dispatch')
class UserUpdateView(FormView):
	form_class = UserInformationUpdateForm
	template_name = 'my_account.html'
	success_url = reverse_lazy('home')
	success_message = "Accounts successfully updated!"

	def get_initial(self):
		user = self.request.user
		profiles = user.Profile

		return {

			'Current_Position': profiles.Current_Position,
			'region': profiles.region,
			'phone': profiles.phone,
			'address': profiles.address,
			'city': profiles.city,
			'email': user.email,
			'postal_code': profiles.postal_code,
			'institution': profiles.institution,
			'Country':profiles.Country,

		}

	def form_valid(self, form):
		messages.add_message(self.request, messages.SUCCESS, 'Accounts successfully updated!')

		return super(UserUpdateView, self).form_valid(form)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		form.full_clean()

		if form.is_valid():
			user = request.user
			#user.first_name = form.cleaned_data['first_name']
			#user.last_name = form.cleaned_data['last_name']
			user.email = form.cleaned_data['email']
			user.save()

			user.Profile.address = form.cleaned_data['address']
			user.Profile.phone = form.cleaned_data['phone']
			user.Profile.post_code = form.cleaned_data['postal_code']
			user.Profile.region = form.cleaned_data['region']
			user.Profile.city = form.cleaned_data['city']
			user.Profile.institution = form.cleaned_data['institution']
			user.Profile.Country = form.cleaned_data['Country']
			user.Profile.Current_Position = form.cleaned_data['Current_Position']
			user.Profile.save()

			logger.info('Account Settings updated by %s', user)

			return self.form_valid(form)
		else:
			return self.form_invalid(form)

# this should be accessed by Admin users only
@method_decorator(login_required, name='dispatch')
class AccountsListView(ListView):
	model = Profile
	context_object_name = 'profiles'
	template_name = 'AccountsList.html'
	paginate_by = 10


def sendmail(request):
	if request.method =='GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			sender_email = form.cleaned_data['email']
			sender_name = form.cleaned_data['Name']
			institution = form.cleaned_data['Institutions']
			message = "Dear Cloud admin \n\n{0} from {1} at {2} has sent you a new message:\n\n{3}".format(sender_name,institution,sender_email, form.cleaned_data['message'])
			try:
				send_mail("CHPC Cloud Enquiries",message,'no-reply@openstackusers.chpc.ac.za',['wphukungoane@gmail.com'], )
				messages.success(request, 'Success! Thank you for your message.')
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect('help')
	return render(request, 'help.html', {'form': form})

@login_required
def contact_us(request):
	if request.method =='GET':
		form = ContactForm()
	else:
		form = ContactForm(request.POST)
		if form.is_valid():
			sender_email = form.cleaned_data['email']
			sender_name = form.cleaned_data['Name']
			institution = form.cleaned_data['Institutions']
			message = "Dear Cloud admin \n\n{0} from {1} at {2} has sent you a new message:\n\n{3}".format(sender_name,institution,sender_email, form.cleaned_data['message'])
			mail_subject = "CHPC Cloud Enquiries"
			try:
				send_mail(mail_subject,message,'no-reply@openstackusers.chpc.ac.za',['wphukungoane@gmail.com'], )
				messages.success(request, 'Success! Thank you for your message.')
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect('contact')
	return render(request, 'contact_us.html', {'form': form})

#@method_decorator(login_required, name='dispatch')
#class AccountDetailView(DetailView):
   # model = Profile
   # template_name = 'Acc_profile_detail.html'
   # context_object_name = "profiles"



    #def get_context_data(self, **kwargs):
     #   context = super(AccountDetailView, self).get_context_data(**kwargs)
      #  context['profiles'] = Profile.objects.filter(pk=self.kwargs['pk'])

       #return context
