from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from .permissions import IsOwner
from .models import Applicant
from .serializers import ApplicantSerializer, UserSerializer

class ApplicantView(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
