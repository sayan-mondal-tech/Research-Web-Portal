"""portalsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from api.views import views_portal, views_accounts, views_authentication

router = routers.DefaultRouter()
router.register('slot',views_portal.SlotView, base_name="slotList")
router.register('application', views_portal.ApplicationView, base_name="applicationList")
router.register('fee', views_portal.FeeView, base_name="feeList")
router.register('applicant', views_accounts.ApplicantView, base_name="applicatnList")
router.register('user', views_accounts.UserView, base_name="userList")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^login/$', views_authentication.LoginView.as_view(), name='api_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', views_authentication.LogoutView.as_view(), name='api_logout'),
]
