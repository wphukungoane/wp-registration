import math
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator

from markdown import markdown



class ProjectInfo(models.Model):
	disciplines = [
				('Astro', 'Astronomy'),
				('Bio',  'Bioinformatics'),
				('ML',  'Machine Learning'),
				('CMS',  'Chemistry and Material Science'),
				('CS',  'Computer Science'),
				('CSP', 'Computational Space Physics'),
				('CFD', 'Computational and Fluid Dynamics'),
				('Others', 'Other'),]
	Project_Owner = models.ForeignKey(User, related_name='projects')
	Name = models.CharField(max_length=255)
	Research_Area = models.CharField(max_length=15, choices=disciplines,default='', blank=True)
	Description = models.TextField(max_length=4000)
	Created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.Name

	def get_Description_as_markdown(self):
		return mark_safe(markdown(self.Description, safe_mode='escape'))
