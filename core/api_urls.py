from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import APIRequestLogViewSet

router = DefaultRouter()
router.register(r'logs', APIRequestLogViewSet, basename='apirequestlog')

urlpatterns = [
    path('core/', include(router.urls)), # Exposes api/v1/core/logs/
]
