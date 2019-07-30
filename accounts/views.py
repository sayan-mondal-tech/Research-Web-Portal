from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Applicant, Official
from .forms import UserForm, ApplicantForm, OfficialForm, UserEditForm

# Create your views here.

def home_page(request):
    return render(request,'accounts/index.html')



def login_f(request):
	if request.method == 'POST':
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('portal:index')
	    else:
	    	messages.error(request, "Invalid username or password")
	form = AuthenticationForm()
	return render(request,'accounts/login_f.html', {'form' : form})

def login_s(request):
	if request.method == 'POST':
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('portal:index')
	    else:
	    	messages.error(request, "Invalid username or password")
	form = AuthenticationForm()
	return render(request,'accounts/login_s.html', {'form' : form})

@login_required
def logout_view(request):
	logout(request)
	return redirect('accounts:home_page')

def signup(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST,request.FILES)
		profile_form = ApplicantForm(request.POST,request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password2'])
			new_user.save()
			profile=Applicant.objects.create(user=new_user)
			profile.mobile_no = profile_form.cleaned_data['mobile_no']
			profile.save()
			return redirect('accounts:login')
	else:
		user_form = UserForm()
		profile_form = ApplicantForm()
	return render(request, 'accounts/register.html', {'user_form':user_form, 'profile_form':profile_form})

def signup_official(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST, request.FILES)
		profile_form = OfficialForm(request.POST, request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password2'])
			new_user.save()
			profile = Official.objects.create(user=new_user)
			profile.mobile_no = profile_form.cleaned_data['mobile_no']
			profile.employee_id = profile_form.cleaned_data['employee_id']
			profile.designation = profile_form.cleaned_data['designation']
			profile.save()
			return redirect('accounts:login')
	else:
		user_form = UserForm()
		profile_form = OfficialForm()
	return render(request, 'accounts/official_register.html', {'user_form':user_form, 'profile_form':profile_form})

@login_required
def edit_official(request):
	profile = get_object_or_404(Official, pk=request.user.official.id)
	if request.method == 'POST':
		user_form = UserEditForm(request.POST, request.FILES, instance=request.user)
		profile_form = OfficialForm(request.POST, request.FILES, instance=profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('accounts:dashboard')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = OfficialForm(instance=profile)
	return render(request, 'accounts/edit_profile.html', {'user_form':user_form, 'profile_form':profile_form})

@login_required
def edit_profile(request):
	profile = get_object_or_404(Applicant, pk=request.user.applicant.id)
	if request.method == 'POST':
		user_form = UserEditForm(request.POST, request.FILES, instance=request.user)
		profile_form = ApplicantForm(request.POST, request.FILES, instance=profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('accounts:dashboard')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ApplicantForm(instance=profile)
	return render(request, 'accounts/edit_profile.html', {'user_form':user_form, 'profile_form':profile_form})

@login_required
def dashboard(request):
	try:
		if request.user.applicant:
			profile = get_object_or_404(Applicant,pk=request.user.applicant.id)
	except:
		pass
	try:
		if request.user.official:
			profile = get_object_or_404(Official,pk=request.user.official.id)
	except:
		pass
	return render(request,'accounts/dashboard.html',{'profile':profile})
