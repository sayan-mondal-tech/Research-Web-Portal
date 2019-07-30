from django import forms
from .models import Application, Slot, Fee
from accounts.models import Applicant
import datetime

class InternshipForm(forms.ModelForm):
	slot = forms.ModelChoiceField(queryset=Slot.objects.all())
	class Meta:
		model = Applicant
		fields = ['slot','department']
		widgets = {'department':forms.Select(),'slot':forms.Select()}

class ApplicationForm(forms.ModelForm):
	class Meta:
		model = Application
		fields = ['applicant_name','gender','mobile_no','email','date_of_birth','year_of_study','applicant_photo','cv']
		widgets = {'gender':forms.RadioSelect(),'date_of_birth':forms.SelectDateWidget(years=range(1980,2018)),'year_of_study':forms.RadioSelect()}

class ApplicationRemarksForm(forms.ModelForm):
	class Meta:
		model = Application
		fields = ['remarks',]

class SlotForm(forms.ModelForm):
 	class Meta:
 		model = Slot
 		fields = ['title','start_date', 'end_date','duration', 'max_strength','employee_code']
 		widgets = {'start_date':forms.SelectDateWidget(years=range(datetime.date.today().year,datetime.date.today().year + 1)), 'end_date':forms.SelectDateWidget(years=range(datetime.date.today().year,datetime.date.today().year + 2))}

class FeePayForm(forms.ModelForm):
	class Meta:
		model = Fee
		fields = ['fee_type']
		widgets = {'fee_type':forms.RadioSelect()}

class FeeForm(forms.ModelForm):
	class Meta:
		model = Fee
		fields = ['transaction_no','fees','paid_on','fee_receipt']


class FeeRemarksForm(forms.ModelForm):
	class Meta:
		model = Fee
		fields = ['remarks',]
