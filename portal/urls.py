from django.conf.urls import url
from . import views
from portal.views import views_applicant as applicant
from portal.views import views_official as official

app_name = 'portal'

urlpatterns = [
	#applicant urls
	url(r'^index/$', applicant.index, name="index"),
	url(r'^internship/form/$', applicant.internship_form, name="internship-form"),
	url(r'^internship/details/$', applicant.internship_details, name="internship-details"),
	url(r'^internship/edit/$', applicant.edit_internship, name="internship-edit"),
	url(r'^applications/$', applicant.application_home, name="applications"),
	url(r'^application/form/(?P<pk>\d+)/$', applicant.application_form, name="application-form"),
	url(r'^application/filled/(?P<pk>\d+)/$', applicant.application_filled, name="application-filled"),
	url(r'^application/status/$', applicant.application_status, name='application-status'),
	url(r'^final/list/$', applicant.final_list, name="final-list"),
	url(r'^get/documents/(?P<pk>\d+)/$', applicant.get_documents, name="get-documents"),
	#official urls
	url(r'^application/all/$', official.all_applications, name="all-applications"),
	url(r'^application/(?P<pk>\d+)/$', official.application_details, name="application-details"),
	url(r'^application/verify/(?P<pk>\d+)/$', official.application_verify, name="application-verify"),
	url(r'^application/reject/(?P<pk>\d+)/$', official.application_reject, name="application-reject"),
	url(r'^slot/new/$', official.create_slot, name="create-slot"),
	url(r'^slot/(?P<pk>\d+)/edit/$', official.edit_slot, name="edit-slot"),
	url(r'^slot/all/$', official.all_slots, name="all-slots"),
	url(r'^slot/(?P<pk>\d+)/delete/$', official.DeleteSlot.as_view(), name='delete-slot'),
	#docs
	url(r'^acknowledgement/(?P<pk>\d+)/$', applicant.acknowledgement_slip, name="acknowledgement"),
	url(r'^acceptance/(?P<pk>\d+)/$', applicant.acceptance_letter, name="acceptance"),
	url(r'^temp-pass/(?P<pk>\d+)/$', applicant.temp_pass, name="temp-pass"),
	url(r'^attendance/(?P<pk>\d+)/$', applicant.attendance_letter, name="attendance"),
	url(r'^clearance/(?P<pk>\d+)/$', applicant.clearance_letter, name="clearance"),
	url(r'^bond/(?P<pk>\d+)/$', applicant.bond_format, name="bond"),
	url(r'^rules/$', applicant.rules, name="rules"),
]
