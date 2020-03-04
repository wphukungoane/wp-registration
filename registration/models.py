from django.db import models

from django_countries.fields import CountryField

# User profile model
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

# Project models
class Project(models.Model):
    
    STATUS_CHOICES = [
        ('Approved','Approved'),
        ('Pending','Pending'),
        ('Finished','Finished'),
        ('Disabled','Disabled'),
    ]

    name = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    shortname = models.CharField(max_length=10)
    discipline = models.CharField(max_length=10)
    project_user = models.CharField(max_length=10)
    description = models.TextField() 
    date_created = models.DateField(auto_now=True)
    date_approved = models.DateField()
    
