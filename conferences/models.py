from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import BaseModel

class Conference(BaseModel):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    conference_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    description = models.TextField(blank=True)

    def update_status(self):
        today = timezone.now().date()
        if self.status != 'Cancelled':
            if today < self.start_date:
                self.status = 'Upcoming'
            elif self.start_date <= today <= self.end_date:
                self.status = 'Ongoing'
            elif today > self.end_date:
                self.status = 'Completed'
            self.save()

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return self.conference_name

class Session(BaseModel):
    session_name = models.CharField(max_length=255)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='sessions')
    speaker = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_attendees = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("End time must be after start time.")
            
            # Check for overlaps within the same conference (excluding self)
            overlapping_sessions = Session.objects.filter(
                conference=self.conference,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
                is_deleted=False
            ).exclude(pk=self.pk)
            
            if overlapping_sessions.exists():
                raise ValidationError("This session overlaps with another session in the same conference.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.session_name} ({self.conference.conference_name})"

class Attendee(BaseModel):
    attendee_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    organization = models.CharField(max_length=255, blank=True)
    preferences = models.ManyToManyField(Session, blank=True, related_name='interested_attendees')

    def __str__(self):
        return self.attendee_name

class Registration(BaseModel):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('session', 'attendee')

    def clean(self):
        # 1. Capacity Check
        if self.pk is None: # New registration
             count = Registration.objects.filter(session=self.session, is_deleted=False).exclude(payment_status='Failed').count()
             if count >= self.session.max_attendees:
                 raise ValidationError(f"Session '{self.session.session_name}' is full.")

        # 2. Overlap Check for Attendee
        # Check if attendee is registered for any other session that overlaps with this one
        overlapping_registrations = Registration.objects.filter(
            attendee=self.attendee,
            session__start_time__lt=self.session.end_time,
            session__end_time__gt=self.session.start_time,
            is_deleted=False
        ).exclude(pk=self.pk).exclude(payment_status='Failed')

        if overlapping_registrations.exists():
             raise ValidationError("Attendee is already registered for an overlapping session.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attendee.attendee_name} -> {self.session.session_name}"
