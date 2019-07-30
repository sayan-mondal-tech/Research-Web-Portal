from rest_framework import serializers
from portal.models import Slot, Application, Fee

class SlotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Slot
        #fields = ('start_date','end_date','duration','max_strength','present_strength','is_filled',)
        fields = '__all__'

class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class FeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'
