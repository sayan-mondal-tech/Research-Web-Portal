from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
import datetime
import re
from portal.models import Application, Fee, Slot
from accounts.models import Applicant, Official
from portal.forms import ApplicationRemarksForm, SlotForm, FeeRemarksForm

#official views

@login_required
def create_slot(request):
	try:
		if request.user.official:
			if request.method == 'POST':
				form = SlotForm(request.POST)
				if form.is_valid():
					form.save()
					return redirect('portal:all-slots')
			else:
				form = SlotForm()
			return render(request, 'official/create_slot.html', {'form':form})
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

@login_required
def edit_slot(request,pk):
	try:
		if request.user.official:
			slot = get_object_or_404(Slot, pk=pk)
			if request.method == 'POST':
				form = SlotForm(request.POST, instance=slot)
				if form.is_valid():
					form.save()
					return redirect('portal:all-slots')
			else:
				form = SlotForm(instance=slot)
			return render(request, 'official/create_slot.html', {'form':form})
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

@login_required
def all_slots(request):
	try:
		if request.user.official:
			#slots = Slot.objects.all().order_by('start_date')
			slots = Slot.objects.filter(employee_code=request.user.official.employee_id)
			return render(request, 'official/all_slots.html', {'slots':slots})
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

@method_decorator(login_required, name='dispatch')
class DeleteSlot(DeleteView):
    model = Slot
    template_name = 'official/slot_confirm_delete.html'
    success_url = reverse_lazy('portal:all-slots')

@login_required
def all_applications(request):
	try:
		if request.user.official:
			query = request.GET.get("q")
			if query:
				match_app_no = re.match(r'\d{2}[a-zA-Z]{2}\d{4}', query)
				if match_app_no:
					try:
						application = Application.objects.get(application_no=query)
						return render(request, 'official/all_applications.html', {'search_app':application})
					except Application.DoesNotExist:
						messages.error(request, "No application found with {}".format(query))
				else:
					messages.error(request, "Invalid application number")
			applications = Application.objects.all().order_by('pk')
			return render(request, 'official/all_applications.html', {'applications':applications})
	except Official.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def application_details(request,pk):
	try:
		if request.user.official:
			application = get_object_or_404(Application, pk=pk)
			return render(request, 'official/application_details.html', {'application':application})
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

@login_required
def application_verify(request,pk):
	try:
		if request.user.official:
			application = get_object_or_404(Application, pk=pk)
			if application.is_application_filled == True:
				application.verified = True
				application.remarks = "Application accepted"
				application.save()
				applications = Application.objects.filter(user=application.user)
				fee = Fee.objects.create(application=application)
				fee.fees = 200.00
				fee.save()
				messages.success(request,"Application verified")
				return redirect('portal:application-details',pk=pk)
			else:
				messages.error(request,"Application not filled yet")
				return redirect('portal:index')
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

@login_required
def application_reject(request,pk):
	try:
		if request.user.official:
			application = get_object_or_404(Application , pk=pk)
			if request.method == 'POST':
				form = ApplicationRemarksForm(request.POST)
				if form.is_valid():
					application.remarks = form.cleaned_data['remarks']
					application.is_application_filled = False
					application.save()
					messages.info(request, "Application rejected")
					return redirect('portal:application-details',pk=pk)
			else:
				form = ApplicationRemarksForm()
			return render(request, 'official/remarks.html', {'form':form})
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

@login_required
def all_fees(request):
	try:
		if request.user.official:
			query = request.GET.get("q")
			if query:
				try:
					transaction = Fee.objects.get(transaction_no=query)
					return render(request, 'official/all_fees.html', {'transaction':transaction})
				except Fee.DoesNotExist:
					messages.error(request, "No transaction found with {}".format(query))
			fees = Fee.objects.filter(is_fees_paid=True).order_by('pk')
			return render(request, 'official/all_fees.html', {'fees':fees})
	except Official.DoesNotExist:
		messages.error(request,"Not authorized")
		return redirect('portal:index')

@login_required
def fee_details(request,pk):
	try:
		if request.user.official:
			fee = get_object_or_404(Fee, pk=pk)
			return render(request, 'official/fee_details.html', {'fee':fee})
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

@login_required
def fee_verify(request,pk):
	try:
		if request.user.official:
			fee = get_object_or_404(Fee, pk=pk)
			if fee.is_fees_paid == True:
				fee.verified = True
				fee.remarks = "Application accepted"
				fee.save()
				applications = Application.objects.filter(user=fee.application.user)
				applicant_of_app = fee.application.user.applicant
				fees_no = 0
				for app in applications:
					try:
						if app.fee:
							if app.fee.verified:
								fees_no += 1
					except:
						pass
				if fees_no == applications.count():
					applicant_of_app.reporting_date = str(applicant_of_app.slot.start_date) + " " + str(datetime.time(hour=10, minute=0))
					applicant_of_app.is_group_formed = True
				applicant_of_app.save()
				messages.success(request,"Fee payment details verified")
				return redirect('portal:fee-details',pk=pk)
			else:
				messages.error(request,"Fee not paid yet")
				return redirect('portal:index')
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')

@login_required
def fee_reject(request,pk):
	try:
		if request.user.official:
			fee = get_object_or_404(Fee , pk=pk)
			if request.method == 'POST':
				form = FeeRemarksForm(request.POST)
				if form.is_valid():
					fee.remarks = form.cleaned_data['remarks']
					fee.is_fees_paid = False
					fee.save()
					messages.info(request, "Fee payment rejected")
					return redirect('portal:fee-details',pk=pk)
			else:
				form = FeeRemarksForm()
			return render(request, 'official/remarks.html', {'form':form})
	except Official.DoesNotExist:
		messages.error(request, "Not authorized")
		return redirect('portal:index')
