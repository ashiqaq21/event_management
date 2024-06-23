from rest_framework import serializers
from event.models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'organizer': {'required': False}
        }
    
    def update(self, instance, validated_data):
        validated_data.pop('organizer', None)
        return super().update(instance, validated_data)
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= '__all__'

class RegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields= '__all__'