from rest_framework import serializers
from .models import APIRequestLog

class APIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog
        fields = ['id', 'api_endpoint', 'method', 'request_body', 'response_body', 'status_code', 'created_at', 'ip_address']
