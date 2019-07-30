from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from accounts.models import Applicant
from api.serializers.accounts_serializer import ApplicantSerializer, UserSerializer

class ApplicantView(viewsets.ModelViewSet):
    serializer_class = ApplicantSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        return Applicant.objects.filter(user=user)

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(username=user.username)
