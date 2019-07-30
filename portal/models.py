from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from .validators import validate_file_size
import datetime

# Create your models here.
class Slot(models.Model):
	title = models.CharField(max_length = 100, default = '')
	start_date = models.DateField(default=timezone.now, null=True)
	end_date = models.DateField(default=timezone.now, null=True)
	duration = models.IntegerField(default=7,null=True)
	max_strength = models.IntegerField(default=10,null=True)
	present_strength = models.IntegerField(default=0,null=True)
	is_filled = models.BooleanField(default=False)
	employee_code = models.CharField(max_length=10, default='')
	def get_absolute_url(self):
		return reverse('portal:all-slots')

	#def __str__(self):
		#return str(self.start_date) + " - " + str(self.end_date) + " :: " + str(self.present_strength) + " filled"

	def __str__(self):
		return str(self.title)

class Application(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	application_no = models.CharField(max_length=11, default='00XX0000')
	applicant_name = models.CharField(max_length=250, default='')
	GENDER_CHOICES = (
		('M','Male'),
		('F','Female'),
	)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
	mobile_no = models.CharField(max_length=10,default='')
	date_of_birth = models.DateField(default=timezone.now)
	email = models.EmailField(null=True)
	applicant_photo = models.FileField(null=True, help_text="upload jpg, jpeg, png files only", validators=[FileExtensionValidator(['jpg','png','jpeg']),validate_file_size])
	cv = models.FileField(null=True,help_text="upload only pdf files", validators=[FileExtensionValidator(['pdf']),validate_file_size])
	slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True)
	YEAR_CHOICES = (
		('1', 'First'),
		('2', 'Second'),
		('3', 'Third'),
		('4','Fourth'),
	)
	year_of_study = models.CharField(max_length=1, choices =YEAR_CHOICES, default='1')
	department = models.CharField(max_length=250, default='')
	is_application_filled = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)
	remarks = models.TextField(null=True)

	def get_absolute_url(self):
		return reverse('portal:application-filled')

	def __str__(self):
		return self.application_no

class Fee(models.Model):
	application = models.OneToOneField(Application, on_delete=models.CASCADE)
	fee_receipt = models.FileField(null=True,help_text="upload pdf,jpg,jpeg,png files only with size less than 2mb")
	FEE_CHOICES = (
		('O', 'Online'),
		('C', 'Challan'),
	)
	fee_type = models.CharField(max_length=1, choices=FEE_CHOICES, default='O')
	transaction_no = models.CharField(max_length=20,default='')
	fees = models.FloatField(default=200.0)
	paid_on = models.DateTimeField(default=timezone.now,help_text="enter only date in yyyy/mm/dd format")
	is_fees_paid = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)
	remarks = models.TextField(null=True)

	def get_absolute_url(self):
		return reverse('portal:applications')

	def __str__(self):
		return str(self.transaction_no)
