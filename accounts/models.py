from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from api.models import TokenModel
from portal.models import Slot  # later---enlists available choices

# Create your models here.

class Applicant(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	mobile_no = models.CharField(max_length=10,default='')
	TRAINING_CHOICES = (
		('T','Training'),
		('P','Project'),
	)
	DEPARTMENT_CHOICES = (
		('BT','Biotechnology'),
		('CE','Civil Engineering'),
		('CH','Chemical Engineering'),
		('CS','Computer Science & Engineering'),
		('EC','Electronics and Communication Engineering'),
		('EE','Electrical Engineering'),
		('IT','Information Technology'),
		('ME','Mechanical Engineering'),
		('MM','Metallurgical and Materials Engineering'),
	)
	internship_type = models.CharField(max_length=1, choices=TRAINING_CHOICES, default='T')
	duration = models.IntegerField(default=7)
	slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True)
	course = models.CharField(max_length=250, default='')
	department = models.CharField(max_length=2, choices=DEPARTMENT_CHOICES, default='CS')
	group_strength = models.IntegerField(default=1)
	reporting_date = models.DateTimeField(default=timezone.now)
	is_filled = models.BooleanField(default=False)
	is_group_formed = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse('accounts:dashboard', kwargs={'pk': self.pk})

	@receiver(post_save, sender=settings.AUTH_USER_MODEL)
	def create_auth_token(sender, instance=None, created=False, **kwargs):
	    if created:
	        TokenModel.objects.create(user=instance)

	def __str__(self):
		return self.user.username

class Official(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	mobile_no = models.CharField(max_length=10,default='')
	employee_id = models.CharField(max_length=10, default='')
	designation = models.CharField(max_length=100, default='')

	def get_absolute_url(self):
		return reverse('accounts:dashboard', kwargs={'pk': self.pk})

	def __str__(self):
		return self.user.username
