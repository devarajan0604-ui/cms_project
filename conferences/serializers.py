from rest_framework import serializers
from .models import Conference, Session, Attendee, Registration
from rest_framework.validators import UniqueTogetherValidator


class SessionSerializer(serializers.ModelSerializer):
    conference_name = serializers.CharField(source='conference.conference_name', read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'session_name', 'conference', 'conference_name', 'speaker', 'start_time', 'end_time', 'max_attendees', 'price']

class ConferenceSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)

    class Meta:
        model = Conference
        fields = ['id', 'conference_name', 'start_date', 'end_date', 'location', 'status', 'description', 'sessions']

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'attendee_name', 'email', 'phone_number', 'organization', 'preferences']

class RegistrationSerializer(serializers.ModelSerializer):
    attendee_name = serializers.CharField(source='attendee.attendee_name', read_only=True)
    session_name = serializers.CharField(source='session.session_name', read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'conference', 'session', 'attendee', 'attendee_name', 'session_name', 'registration_date', 'payment_status']
        read_only_fields = ['payment_status', 'registration_date']

class RegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['conference', 'session', 'attendee']
        validators = [
            UniqueTogetherValidator(
                queryset=Registration.objects.all(),
                fields=['session', 'attendee'],
                message="This attendee is already registered for the selected session."
            )
        ]

    def validate(self, data):
        # Additional validation can go here if not covered by model
        return data
