# Conference Management System

A Django REST Framework application for managing conferences, sessions, attendees, and registrations.

## Features
- **Conferences**: Manage conference status (Upcoming, Ongoing, Completed) automatically.
- **Sessions**: Manage sessions with overlap validation and capacity checks.
- **Attendees & Registrations**: Register attendees, handle payments (mock), and track capacity.
- **Recommendations**: Recommend sessions based on attendee preferences (mock email).
- **Reports**: Analytics for conferences and sessions (revenue, attendance).
- **Logging**: Middleware logs all API requests and responses.

## Tech Stack
- Django 5.x / 6.x
- Django REST Framework
- Database: MySQL (Configured for Production) / SQLite (Dev Default)
- PyMySQL (MySQL Driver)

## Setup

1. **Clone the repository**
2. **Install Dependencies**
   ```bash
   pip install django djangorestframework pymysql cryptography
   ```
3. **Database Setup**
   - By default, the project uses `SQLite` for development ease.
   - To use **MySQL**:
     - Create a database `cms_db`.
     - Uncomment the MySQL database configuration in `cms_project/settings.py`.
     - Comment out the SQLite configuration.
4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Populate Sample Data**
   ```bash
   python manage.py populate_data
   ```
6. **Run Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Conferences
- `GET /api/conferences/` - List all
- `GET /api/conferences/{id}/` - Details
- `GET /api/conferences/upcoming/` - List upcoming conferences

### Registrations
- `POST /api/registrations/` - Register for a session
  ```json
  {
    "conference": 1,
    "session": 1,
    "attendee": 1
  }
  ```

### Payments
- `POST /api/payments/process/` - Process payment (simulated)
  ```json
  { "registration_id": 1 }
  ```

### Search
- `GET /api/search/?q=Keyword` - Search conferences and sessions

### Attendee Recommendations
- `GET /api/attendees/{id}/recommendations/?email=true` - Get recommended sessions and optionally send email.

### Reports
- `GET /api/reports/conferences/`
- `GET /api/reports/sessions/`

## Design Decisions
- **Clean Architecture**: Services layer (`conferences/services.py`) separates business logic from Views/Models.
- **Middleware**: `RequestLoggingMiddleware` ensures all API interactions are audited.
- **Validation**:
  - Model-level validation (`clean()`) ensures data integrity (e.g., date ranges, overlaps).
  - Serializer validation handles input format.
- **Scalability**: Database optimization via `select_related` (used in ViewSets/Serializers implicitly or can be added).

## Notes
- `pymysql` is used as the MySQL driver.
- The default database is set to SQLite to ensure the project runs immediately without local MySQL setup.
