from rest_framework import viewsets, status, views, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, F
from django.utils import timezone
from .models import Conference, Session, Attendee, Registration
from .serializers import (ConferenceSerializer, SessionSerializer, 
                          AttendeeSerializer, RegistrationSerializer, RegistrationCreateSerializer)
from .services import check_payment_status, get_attendee_recommendations, send_recommendation_email

class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.filter(is_deleted=False)
    serializer_class = ConferenceSerializer

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        today = timezone.now().date()
        upcoming = Conference.objects.filter(start_date__gt=today, is_deleted=False)
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.filter(is_deleted=False)
    serializer_class = SessionSerializer
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

class AttendeeViewSet(viewsets.ModelViewSet):
    # Added AttendeeViewSet just in case, good for management
    queryset = Attendee.objects.filter(is_deleted=False)
    serializer_class = AttendeeSerializer
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RegistrationCreateSerializer
        return RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registration = serializer.save()
        
        # Auto-process payment (Mock)
        headers = self.get_success_headers(serializer.data)
        return Response(RegistrationSerializer(registration).data, status=status.HTTP_201_CREATED, headers=headers)

class PaymentProcessView(views.APIView):
    def post(self, request):
        """
        Mock payment processing.
        Payload: {"registration_id": 1}
        """
        reg_id = request.data.get('registration_id')
        try:
            registration = Registration.objects.get(pk=reg_id)
            if registration.payment_status == 'Paid':
                return Response({"message": "Already paid"}, status=status.HTTP_400_BAD_REQUEST)
            
            payment_status = check_payment_status()
            registration.payment_status = payment_status
            registration.save()
            return Response({"status": payment_status, "registration_id": reg_id})
        except Registration.DoesNotExist:
            return Response({"error": "Registration not found"}, status=status.HTTP_404_NOT_FOUND)

class SearchAPIView(views.APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
             return Response({
            "conferences": [],
            "sessions": []
        })

        from django.db.models import Q
        
        conferences = Conference.objects.filter(
            Q(conference_name__icontains=query) | Q(description__icontains=query),
            is_deleted=False
        )
        
        sessions = Session.objects.filter(
            Q(session_name__icontains=query) | Q(speaker__icontains=query),
            is_deleted=False
        )
        
        return Response({
            "conferences": ConferenceSerializer(conferences, many=True).data,
            "sessions": SessionSerializer(sessions, many=True).data
        })

class AttendeeRecommendationView(views.APIView):
    def get(self, request, pk):
        try:
            attendee = Attendee.objects.get(pk=pk, is_deleted=False)
            recommendations = get_attendee_recommendations(attendee)
            send_email = request.query_params.get('email', 'false').lower() == 'true'
            
            if send_email:
                send_recommendation_email(attendee, recommendations)
                
            return Response(SessionSerializer(recommendations, many=True).data)
        except Attendee.DoesNotExist:
            return Response({"error": "Attendee not found"}, status=status.HTTP_404_NOT_FOUND)

# Reports
class ConferenceReportView(views.APIView):
    def get(self, request):
        data = []
        for conf in Conference.objects.filter(is_deleted=False):
            unique_attendees = Registration.objects.filter(conference=conf).values('attendee').distinct().count()
            data.append({
                "conference": conf.conference_name,
                "sessions": conf.sessions.filter(is_deleted=False).count(),
                "unique_attendees": unique_attendees
            })
        return Response(data)

class SessionReportView(views.APIView):
    def get(self, request):
        data = []
        for session in Session.objects.filter(is_deleted=False):
            registrations = Registration.objects.filter(session=session)
            total_registrations = registrations.count()
            paid_registrations = registrations.filter(payment_status='Paid').count()
            revenue = paid_registrations * session.price
            remaining_capacity = session.max_attendees - total_registrations
            
            data.append({
                "session": session.session_name,
                "total_registrations": total_registrations,
                "remaining_capacity": max(0, remaining_capacity),
                "revenue": revenue
            })
        return Response(data)
