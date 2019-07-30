from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from portal.models import Application, Fee, Slot
from api.serializers.portal_serializers import SlotSerializer, ApplicationSerializer, FeeSerializer

class SlotView(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    #permission_classes = (permissions.IsAuthenticated,)


class ApplicationView(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        return Application.objects.filter(user=user)

class FeeView(viewsets.ModelViewSet):
    serializer_class = FeeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user = self.request.user
        return Fee.objects.filter(user=user)
