from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Applicant

class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Applicant
        #fields = ('start_date','end_date','duration','max_strength','present_strength','is_filled',)
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)
