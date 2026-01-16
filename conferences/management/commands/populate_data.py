from django.core.management.base import BaseCommand
from datetime import date, timedelta
from conferences.models import Conference, Session, Attendee, Registration

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Data Cleanup
        Conference.objects.all().delete()
        Attendee.objects.all().delete()

        # Create Conferences
        conf_upcoming = Conference.objects.create(
            conference_name="Global Business Summit 2026",
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=32),
            location="New York",
            description="The future of global business."
        )
        conf_upcoming.update_status()

        conf_ongoing = Conference.objects.create(
            conference_name="Leadership World 2026",
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
            location="San Francisco",
            description="Strategies for modern leadership."
        )
        conf_ongoing.update_status()

        conf_completed = Conference.objects.create(
            conference_name="Finance Expo 2025",
            start_date=date.today() - timedelta(days=100),
            end_date=date.today() - timedelta(days=98),
            location="London",
            description="Trends in finance."
        )
        conf_completed.update_status()

        # Create Sessions
        s1 = Session.objects.create(
            conference=conf_upcoming,
            session_name="Keynote: Market Trends",
            speaker="Jane Doe",
            start_time=f"{conf_upcoming.start_date} 09:00:00",
            end_time=f"{conf_upcoming.start_date} 10:00:00",
            max_attendees=500,
            price=150.00
        )
        s2 = Session.objects.create(
            conference=conf_upcoming,
            session_name="Sustainable Growth",
            speaker="John Smith",
            start_time=f"{conf_upcoming.start_date} 10:30:00",
            end_time=f"{conf_upcoming.start_date} 11:30:00",
            max_attendees=50,
            price=200.00
        )

        # Create Attendees
        a1 = Attendee.objects.create(
            attendee_name="Alice Smith",
            email="alice@example.com",
            phone_number="1234567890",
            organization="Tech Corp"
        )
        a1.preferences.add(s1)

        a2 = Attendee.objects.create(
            attendee_name="Bob Jones",
            email="bob@example.com",
            phone_number="0987654321",
            organization="StartUp Inc"
        )
        a2.preferences.add(s2)

        # Create Registrations
        Registration.objects.create(
            conference=conf_upcoming,
            session=s1,
            attendee=a1,
            payment_status='Paid'
        )
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
