from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='project-home'),
    path('about/', views.about, name='project-about'),
    path('login_f/', views.login_f, name='login-faculty'),
    path('login_s/', views.login_s, name='login-student'),

]
