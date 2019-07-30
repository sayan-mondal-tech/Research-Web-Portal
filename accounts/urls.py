from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

app_name = 'accounts'

urlpatterns = [
	url(r'^$', views.home_page, name='home_page'),
	url(r'^signup/$', views.signup, name="signup"),
	url(r'^signup-official/$', views.signup_official, name="signup-official"),
	url(r'^login_f/$', views.login_f, name="login_f"),
	url(r'^login_s/$',views.login_s, name="login_s"),
	url(r'^logout/$', views.logout_view, name="logout"),
	url(r'^dashboard/$', views.dashboard, name="dashboard"),
	url(r'^edit-profile/$', views.edit_profile, name="edit-profile"),
	url(r'^edit-official/$', views.edit_official, name="edit-official"),
	url(r'^password-reset/$', PasswordResetView.as_view(template_name='accounts/password_reset_form.html', email_template_name='accounts/password_reset_email.html', success_url='password-reset-done'), name='password-reset'),
    url(r'^password-reset/password-reset-done/$', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password-reset-done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', success_url='done'), name='password-reset-confirm'),
    url(r'^password-reset/confirm/MTc/set-password/done/$', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password-reset-complete'),
]
