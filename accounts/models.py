from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class Profile(models.Model):
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

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
	title = models.CharField(max_length=15, choices=TITLE_CHOICES)
	first_name = models.CharField(max_length=15, blank=True)
	last_name = models.CharField(max_length=15, blank=True)
	email = models.EmailField(max_length=150)
	alt_email = models.EmailField(max_length=150, blank=True, default='')
	phone = models.CharField(max_length=15, blank=True, default='')
	mobile = models.CharField(max_length=15, blank=True, default='')
	gender = models.CharField(max_length=15, choices=GENDER_CHOICES,default='', blank=True)
	nationality = CountryField(blank_label='(select country)',default='', blank=True)
	institution = models.CharField(max_length=14, choices=INSTITUTIONS, default='', blank=True)

	def __str__(self):
				 return self.user.username

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			user_profile = Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.Profile.save()
