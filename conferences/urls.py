from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ConferenceViewSet, RegistrationViewSet, PaymentProcessView, 
                    SearchAPIView, AttendeeRecommendationView, ConferenceReportView, SessionReportView)

router = DefaultRouter()
router.register(r'conferences', ConferenceViewSet, basename='conference')
router.register(r'registrations', RegistrationViewSet, basename='registration')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/process/', PaymentProcessView.as_view(), name='payment-process'),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('attendees/<int:pk>/recommendations/', AttendeeRecommendationView.as_view(), name='attendee-recommendations'),
    path('reports/conferences/', ConferenceReportView.as_view(), name='report-conferences'),
    path('reports/sessions/', SessionReportView.as_view(), name='report-sessions'),
]
