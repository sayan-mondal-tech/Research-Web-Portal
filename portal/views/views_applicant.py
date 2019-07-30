# Named as views_applicant but provides some views of official as well.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import datetime
import re
from portal.models import Application, Slot, Fee
from accounts.models import Applicant
from portal.forms import InternshipForm, ApplicationForm, FeeForm, FeePayForm

# Create your views here.

def about(request):
	return render(request, 'applicant/about.html',)

def help_content(request):
	return render(request, 'applicant/help.html',)

def contact(request):
	return render(request, 'applicant/contact.html',)

#@login_required
def index(request):
	try:
		if request.user.applicant:
			profile = get_object_or_404(Applicant, pk=request.user.applicant.id)
			return render(request, 'applicant/applicant_index.html', {'profile':profile})
	except:
		pass
	try:
		if request.user.official:
			#applications = Application.objects.all().order_by('pk')
			applications = Application.objects.filter(application_no__icontains = request.user.official.employee_id)
			fees = Fee.objects.all().order_by('pk')
			return render(request,'official/official_index.html', {'applications':applications,'fees':fees})
	except:
		pass
	return render(request, 'applicant/applicant_index.html',{})

@login_required
def internship_form(request):
	try:
		if request.user.applicant:
			if request.method == 'POST':
				form = InternshipForm(request.POST)
				if form.is_valid():
						slot = get_object_or_404(Slot, pk=form.cleaned_data['slot'].pk)
						slot.save()
						applicant = get_object_or_404(Applicant, pk=request.user.applicant.id)
						applicant.is_filled = True
						applicant.slot = form.cleaned_data['slot']
						applicant.department = form.cleaned_data['department']
						applicant.save()
						application = Application.objects.create(user=request.user)
						application.application_no =  str(datetime.date.today().year)[-2:]+applicant.department+slot.employee_code+str(format(application.id, "04"))
						application.slot = form.cleaned_data['slot']
						application.department = form.cleaned_data['department']
						application.save()
						return redirect('portal:internship-details')
			else:

				form = InternshipForm()
			return render(request, 'applicant/internship_form.html', {'form':form})
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def edit_internship(request):
	try:
		if request.user.applicant:
			if request.user.applicant.is_filled:
				applicant = get_object_or_404(Applicant, pk=request.user.applicant.id)
				slot = get_object_or_404(Slot, pk=request.user.applicant.slot.id)
				slot.present_strength = slot.present_strength - applicant.group_strength
				slot.save()
				Application.objects.filter(user=request.user).delete()
				return redirect('portal:internship-form')
			else:
				messages.error(request, "Please fill the form first")
				return redirect('portal:internship-form')
	except Applicant.DoesNotExist:
		messages.error(request,"No authorized")
		return redirect('portal:index')

@login_required
def internship_details(request):
	try:
		if request.user.applicant:
			if request.user.applicant.is_filled:
				profile = get_object_or_404(Applicant, pk=request.user.applicant.id)
				return render(request, 'applicant/internship_details.html', {'profile':profile})
			else:
				messages.error(request, 'Please fill the details first')
				return redirect('portal:internship-form')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def application_home(request):
	try:
		if request.user.applicant:
			applications = Application.objects.filter(user=request.user)
			if applications != {}:
				print('Not empty')
				print(applications)
			return render(request, 'applicant/application_home.html', {'applications':applications,'applicant':request.user.applicant,})
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def application_form(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			if application.user == request.user:
				if application.is_application_filled:
					messages.error(request, "Application already filled")
					return redirect('portal:applications')
				if request.method == 'POST':
					form = ApplicationForm(request.POST, request.FILES,instance=application)
					if form.is_valid():
						form.save()
						application.is_application_filled = True
						application.save()
						return redirect('portal:application-filled',pk=application.id)
				else:
					form = ApplicationForm(instance=application)
				return render(request, 'applicant/application_form.html', {'form':form})
			else:
				messages.error(request,"Not authorized")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:applications')

@login_required
def application_filled(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			if application.user == request.user:
				return render(request, 'applicant/application_filled.html', {'application':application})
			else:
				messages.error(request, "Not authorized")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

def application_status(request):
	query = request.GET.get("q")
	if query:
		match_app_no = re.match(r'\d{2}[a-zA-Z]{2}\d{4}', query)
		if match_app_no:
			try:
				application = Application.objects.get(application_no=query)
				return render(request, 'applicant/application_status.html', {'application':application})
			except Application.DoesNotExist:
				messages.error(request, "No application found with {}".format(query))
				return redirect('portal:application-status')
		else:
			messages.error(request, "Invalid application number")
			return redirect('portal:application-status')
	else:
		return render(request, 'applicant/application_status.html',)

@login_required
def acknowledgement_slip(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			if application.user == request.user:
				if application.verified:
					fee = get_object_or_404(Fee, pk=application.fee.id)
					return render(request,'applicant/acknowledgement.html',{'application':application,'fee':fee})
				return render(request,'applicant/acknowledgement.html',{'application':application})
			else:
				messages.error(request, "Not authorized")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def pay_fees(request,pk):
	try:
		if request.user.applicant:
			fee = get_object_or_404(Fee, pk=pk)
			if fee.application.user == request.user:
				if request.method == 'POST':
					form = FeePayForm(request.POST, instance=fee)
					if form.is_valid():
						if form.cleaned_data['fee_type'] == 'O':
							fee.fee_type = form.cleaned_data['fee_type']
							fee.save()
							return redirect('portal:pay-fee-online', pk=pk)
						elif form.cleaned_data['fee_type'] == 'C':
							fee.fee_type = form.cleaned_data['fee_type']
							fee.save()
							return redirect('portal:pay-fee-challan', pk=pk)
						else:
							messages.error(request, 'Error paying fees. Choose correct option')
				else:
					form = FeePayForm(instance=fee)
				return render(request, 'applicant/pay_fees.html', {'fee':fee,'form':form})
			else:
				messages.error(request,"Not authorized")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')


@login_required
def pay_fee_online(request, pk):
	try:
		if request.user.applicant:
			fee = get_object_or_404(Fee, pk=pk)
			if fee.application.user == request.user:
				if fee.is_fees_paid == True:
					if fee.verified == True:
						messages.success(request, "Fees already paid. Please proceed with next steps")
						return redirect('portal:applications')
					else:
						messages.info(request, "Fees paid. Please wait for verificatioon or contact officials")
						return redirect('portal:applications')
				return render(request, 'applicant/pay_fee_online.html', {'fee':fee})
			else:
				messages.error(request,"Not authorized")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')


@login_required
def pay_fee_challan(request, pk):
	try:
		if request.user.applicant:
			fee = get_object_or_404(Fee, pk=pk)
			if fee.application.user == request.user:
				if fee.is_fees_paid == True:
					if fee.verified == True:
						messages.success(request, "Fees already paid. Please proceed with next steps")
						return redirect('portal:applications')
					else:
						messages.info(request, "Fees paid. Please wait for verificatioon or contact officials")
						return redirect('portal:applications')
				else:
					if request.method == 'POST':
						form = FeeForm(request.POST,request.FILES, instance=fee)
						if form.is_valid():
							form.save()
							fee.is_fees_paid = True
							fee.save()
							return redirect('portal:fees-paid', pk=pk)
					else:
						form = FeeForm(instance=fee)
					return render(request, 'applicant/pay_fee_challan.html', {'fee':fee,'form':form})
			else:
				messages.error(request,"Not authorized")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def fees_paid(request,pk):
	try:
		if request.user.applicant:
			fee = get_object_or_404(Fee, pk=pk)
			if fee.application.user == request.user:
				if fee.is_fees_paid == True:
					return render(request, 'applicant/fees_paid.html', {'fee':fee})
				else:
					messages.error(request,"Fees not yet paid. Please pay fees")
					return redirect('portal:pay-fee',pk=pk)
			else:
				messages.error(request,"Not authorized")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')


@login_required
def final_list(request):
	try:
		if request.user.applicant:
			if request.user.applicant.is_group_formed == True:
				applicant = get_object_or_404(Applicant, pk=request.user.applicant.id)
				applications = Application.objects.filter(user=request.user)
				return render(request, 'applicant/final_list.html',{'applicant':applicant,'applications':applications})
			else:
				messages.error(request, "Fill the applications and fees before getting the documents")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def get_documents(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			if application.user == request.user:
				return render(request, 'applicant/get_documents.html', {'application':application})
			else:
				messages.error(request, "Fill the applications and fees before getting the documents")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def acceptance_letter(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			applications = Application.objects.filter(user=request.user)
			if application.user == request.user:
				return render(request, 'applicant/acceptance.html', {'application':application,'applications':applications})
			else:
				messages.error(request, "Fill the applications and fees before getting the documents")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def clearance_letter(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			if application.user == request.user:
				fee = get_object_or_404(Fee, pk=application.fee.id)
				return render(request, 'applicant/clearance_letter.html', {'application':application,'fee':fee})
			else:
				messages.error(request, "Fill the applications and fees before getting the documents")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def attendance_letter(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			if application.user == request.user:
				return render(request, 'applicant/attendance_letter.html', {'application':application,'duration':range(1,application.duration+1)})
			else:
				messages.error(request, "Fill the applications and fees before getting the documents")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def temp_pass(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			if application.user == request.user:
				return render(request, 'applicant/temp_pass.html', {'application':application})
			else:
				messages.error(request, "Fill the applications and fees before getting the documents")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def bond_format(request,pk):
	try:
		if request.user.applicant:
			application = get_object_or_404(Application, pk=pk)
			if application.user == request.user:
				return render(request, 'applicant/indemnity_bond_format.html', {'application':application})
			else:
				messages.error(request, "Fill the applications and fees before getting the documents")
				return redirect('portal:index')
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def rules(request):
	try:
		if request.user.applicant:
			return render(request, 'applicant/rules_regulations.html',)
	except Applicant.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')
