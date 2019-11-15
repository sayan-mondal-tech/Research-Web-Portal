from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobsapp.urls')),
    path('', include('accounts.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    path('api/', include([
        path('', include('jobsapp.api.urls')),
    ])),
]
