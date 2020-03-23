from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from .models import Profile
from .forms import SignUpForm, UserInformationUpdateForm, UserForm


class HomePage(TemplateView):

    template_name = 'base_home.html'



def signup(request):
    if request.method == 'POST' :
        profile_form = SignUpForm(data=request.POST)
        user_form = UserForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            messages.success(request, ('Your profile was successfully updated.!'))
            return redirect('home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm()
        profile_form = SignUpForm()
    return render(request, 'registration.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    form_class = UserInformationUpdateForm
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        
        return self.request.user
