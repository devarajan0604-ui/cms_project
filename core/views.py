from rest_framework import viewsets
from .models import APIRequestLog
from .serializers import APIRequestLogSerializer
from django.shortcuts import render

def home(request):
    return render(request, 'core/index.html')

class APIRequestLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = APIRequestLog.objects.all().order_by('-created_at')
    serializer_class = APIRequestLogSerializer
