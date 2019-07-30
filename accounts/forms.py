from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Applicant, Official

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2',]

	def clean_email(self):
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError("Email id already exists")
		return self.cleaned_data['email']

class ApplicantForm(forms.ModelForm):
	class Meta:
		model = Applicant
		fields = ['mobile_no',]

class OfficialForm(forms.ModelForm):
	class Meta:
		model = Official
		fields = ['mobile_no','employee_id','designation',]

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email',]
		exclude = ['username','password1','password2',]