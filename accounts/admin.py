from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, User

class UserprofileInline(admin.StackedInline):
    model = Profile
    can_delete =False
    Verbose_name_plural = "profile"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserprofileInline,)

#admin.site.register(Profile)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
