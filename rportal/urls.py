"""rportal URL Configuration

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
from accounts.views import home_page,login_f,login_s
from portal.views import views_applicant


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page, name='home_page'),
    url(r'^login_f/$', login_f, name='login_f'),
    url(r'^login_s/$', login_s, name='login_s'),
    url(r'^about/$', views_applicant.about, name='about'),
    url(r'^contact/$', views_applicant.contact, name='contact'),
    url(r'^help/$', views_applicant.help_content, name='help'),
    url(r'^portal/', include('portal.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^api/', include('api.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
