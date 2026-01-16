import random
from datetime import date
from django.db.models import Sum
from .models import Session, Registration, Conference

def check_payment_status():
    """Simulate payment processing."""
    # 80% success rate
    return 'Paid' if random.random() < 0.8 else 'Failed'

def get_attendee_recommendations(attendee):
    """
    Suggest sessions based on attendee preferences.
    If attendee has liked sessions `preferences`, recommend other sessions 
    in the same conferences that they haven't registered for.
    """
    preferred_sessions = attendee.preferences.all()
    if not preferred_sessions.exists():
        return []

    # Get conferences of interest
    conference_ids = preferred_sessions.values_list('conference_id', flat=True)
    
    # Get registered session IDs
    registered_session_ids = Registration.objects.filter(attendee=attendee).values_list('session_id', flat=True)

    # Get list of preferred speakers and session name keywords (simulating topics)
    preferred_speakers = preferred_sessions.values_list('speaker', flat=True)
    preferred_keywords = []
    for name in preferred_sessions.values_list('session_name', flat=True):
        preferred_keywords.extend(name.split())
    
    # Filter generic common words
    stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'of', 'and', 'session', 'workshop'}
    preferred_keywords = [k for k in preferred_keywords if k.lower() not in stop_words and len(k) > 3]

    # Find candidates
    # 1. Same Speaker
    # 2. Similar Topic (matching keywords in session name)
    from django.db.models import Q
    
    query = Q(speaker__in=preferred_speakers)
    for keyword in preferred_keywords:
        query |= Q(session_name__icontains=keyword)

    recommendations = Session.objects.filter(query).filter(
        conference_id__in=conference_ids,
        is_deleted=False
    ).exclude(
        id__in=registered_session_ids
    ).exclude(
        id__in=preferred_sessions.values_list('id', flat=True)
    ).distinct().order_by('start_time')[:5]

    return recommendations

def send_recommendation_email(attendee, recommendations):
    """
    Simulate sending an email.
    """
    if not recommendations:
        return
    
    subject = f"Session Recommendations for {attendee.attendee_name}"
    body = "Based on your interests, we recommend:\n"
    for session in recommendations:
        body += f"- {session.session_name} at {session.start_time}\n"
    
    # Store in log or print
    print(f"--- EMAIL TO {attendee.email} ---\nSubject: {subject}\n{body}\n----------------------------------")

def calculate_conference_revenue(conference_id):
    registrations = Registration.objects.filter(
        conference_id=conference_id, 
        payment_status='Paid'
    )
    # Sum of session prices
    revenue = 0
    for reg in registrations:
        revenue += reg.session.price
    return revenue

def update_conference_statuses():
    """
    Updates status of all conferences. 
    Ideally run via Celery or Cron.
    """
    today = date.today()
    for conf in Conference.objects.exclude(status__in=['Cancelled', 'Completed']):
        conf.update_status()
