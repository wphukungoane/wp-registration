from django.db import models
# Create your models here.
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField
from django.core.validators import validate_email, RegexValidator
from django_countries.fields import CountryField



class Profile(models.Model):
    """
    Model to store additional user informations. Extends User
    model.
    """

    qualification = [
    ('None',  'none'),
    ('diploma', 'Diploma'),
    ('bachelors', 'Bachelors'),
    ('honours', 'Honours'),
    ('masters', 'Masters'),
    ('doctorate', 'Doctorate'),
    ]

    INSTITUTIONS = [
    ('University of Cape Town',  'University of Cape Town'),
    ('University of Kwazulu Natal', 'University of Kwazulu Natal'),
    ('University of Pretoria','University of Pretoria'),
    ('University of the Western Cape',  'University of the Western Cape'),
    ('Stellenbosch University','Stellenbosch University'),
    ('University of Witwatersrand', 'University of Witwatersrand'),
    ('University of Limpopo',  'University of Limpopo'),
    ('University of Johannesburg', 'University of Johannesburg'),
    ('Tshwane University of Technology','Tshwane University of Technology'),
    ('University of South Africa',  'University of South Africa'),
    (' Cape Peninsula University of Technology',' Cape Peninsula University of Technology'),
    ('University of Venda', 'University of Venda'),
    ('Durban University of Technology',  'Durban University of Technology'),
    ('Vaal University of Technology', 'Vaal University of Technology'),
    ('Walter Sisulu University','Walter Sisulu University'),
    ('Nelson Mandela University',  'Nelson Mandela University'),
    ('SMU','Sefako Makgatho Health Sciences University'),
    ('Mpumalanga University', 'Mpumalanga University'),
    ('Sol Plaatjie University',  'Sol Plaatjie University'),
    ('University of Johannesburg', 'University of Johannesburg'),
    ('University of the Free State','University of the Free State'),
    ('Rhodes University',  'Rhodes University'),
    (' North-West University',' North-West University'),
    ('University of Fort Hare', 'University of Fort Hare'),
    ('South African Radio Astronomy Observatory','South African Radio Astronomy Observatory'),
    ('South African National Space Agency', 'South African National Space Agency'),
    ('South African Medical Research Council', 'South African Medical Research Council'),
    ('Council for Science and Industrial Research', 'Council for Science and Industrial Research'),
    ('Department of Health', 'Department of Health'),
    ('National Integrated CyberInfrastructure System', 'National Integrated CyberInfrastructure System') ]


    sorted_org = sorted(INSTITUTIONS, key=lambda x: x[1])
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    Current_Position = models.CharField(max_length=150, blank=True)
    phone = models.CharField(validators=[phone_regex],max_length=150,blank=True)
    address = models.CharField(max_length=150, blank=True, default='')
    city = models.CharField(max_length=150, blank=True, default='')
    region = models.CharField(verbose_name=u"Province ",max_length=150, blank=True, default='')
    postal_code = models.CharField(max_length=150, blank=True, default='')
    Country = CountryField(blank_label='(select country)',default='', blank=True)
    institution = models.CharField(max_length=150, choices=sorted_org, default='', blank=True)



    class Meta:
        
        ordering = ['-id']

    def __str__(self):
        return self.user.username


    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.Profile.save()
