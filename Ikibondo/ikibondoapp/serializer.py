from rest_framework import serializers
from .models import *

class Notificationserializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=['user','message','is_read','timestamp']
