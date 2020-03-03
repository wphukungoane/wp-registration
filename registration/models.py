from django.db import models

from django_countries.fields import CountryField

# Create your models here.
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
        ('unspecified', 'unspecified'),
    ]

    title = models.CharField(max_length=4, choices=TITLE_CHOICES)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    alt_email = models.EmailField()
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    genger = models.CharField(max_length=11, choices=GENDER_CHOICES)
    nationality = CountryField(blank_label='(select country)')
    institution = models.TextField()
