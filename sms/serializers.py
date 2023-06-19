from rest_framework import serializers
from .models import Sms

class SmsSerializer(serializers.Serializer):
    phone = serializers.CharField()
    phone_from = serializers.CharField()
    text = serializers.CharField()

class NumberSerializer(serializers.Serializer):
    action = serializers.CharField(required=False)
    key = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    service = serializers.CharField(required=False)
    operator = serializers.CharField(required=False)
    sum = serializers.DecimalField(decimal_places=2, max_digits=20, required=False)
    activationId = serializers.IntegerField(required=False)
    status = serializers.IntegerField(required=False)
    exceptionPhoneSet = serializers.ListField(child=serializers.CharField(), required=False)
