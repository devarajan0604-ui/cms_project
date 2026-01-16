# Conference Management System

A robust Django REST Framework application for managing professional conferences, sessions, attendees, and registrations. This system is built with best practices in mind, including **Universal API Responses**, **JWT Authentication**, and **API Versioning**.

## Features

### Core Functionality
- **Conferences**: Full CRUD. Status updates automatically (Upcoming, Ongoing, Completed) based on date.
- **Sessions**: Full CRUD. Includes strict validation for:
  - **Overlaps**: Prevents sessions from overlapping in the same conference.
  - **Capacity**: Enforces attendee limits per session.
- **Attendees & Registrations**: Register attendees with validation for double-booking.
- **Search**: Advanced search across Conference names/descriptions and Session names/speakers.
- **Reports**: Analytical endpoints for conference attendance and session revenue.

### Advanced Features
- **JWT Authentication**: Secure access using `Bearer` tokens.
- **API Versioning**: All endpoints are namespaced under `/api/v1/`.
- **Universal Response Format**: All API responses (success or error) follow a consistent JSON structure.
- **Logging**: Middleware logs every API request/response to the database (`APIRequestLog`).
- **Soft Deletes**: Entities are soft-deleted (`is_deleted`) to preserve data integrity.
- **Dynamic Recommendations**: Smart session suggestions based on attendee preferences (Speaker/Topic match).

## Tech Stack
- **Framework**: Django 5+, Django REST Framework
- **Auth**: SimpleJWT
- **Database**: MySQL (Production ready) / SQLite (Dev default)
- **Utilities**: PyMySQL, Cryptography

## Setup

### 1. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```
*Dependencies include: `django`, `djangorestframework`, `djangorestframework-simplejwt`, `pymysql`, `cryptography`.*

### 2. Database Configuration
The project is pre-configured for **MySQL**. Ensure you have a MySQL server running and create a database named `cms_db`.
*(To switch to SQLite for quick testing, modify `cms_project/settings.py`)*.

### 3. Migrations
Initialize the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 5. Populate Sample Data
Run the custom management command to seed the database with professional sample data:
```bash
python manage.py populate_data
```

### 6. Run Server
```bash
python manage.py runserver
```

## API Documentation

The API uses **JWT Authentication** and versioning (`v1`).
**Base URL**: `http://127.0.0.1:8000/api/v1/`

### Authentication
All protected endpoints require the header: `Authorization: Bearer <access_token>`

1.  **Login (Get Token)**
    -   `POST /api/v1/token/`
    -   Payload: `{ "username": "admin", "password": "..." }`
2.  **Refresh Token**
    -   `POST /api/v1/token/refresh/`

### Endpoints (v1)

| Resource | Methods | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Conferences** | CRUD | `/conferences/` | Manage conferences. |
| | GET | `/conferences/upcoming/` | List future conferences with details. |
| **Sessions** | CRUD | `/sessions/` | Manage sessions. |
| **Attendees** | CRUD | `/attendees/` | Manage attendees. |
| | GET | `/attendees/{id}/recommendations/` | Get tailored session suggestions. |
| **Registrations** | CRUD | `/registrations/` | Register user for session. |
| **Payments** | POST | `/payments/process/` | Simulate payment for registration. |
| **Search** | GET | `/search/?q=Keyword` | Search across Conferences and Sessions. |
| **Logs** | GET | `/core/logs/` | View system API logs (Admin only). |
| **Reports** | GET | `/reports/conferences/` | Attendance analytics. |
| | GET | `/reports/sessions/` | Revenue and capacity analytics. |

### Universal Response Format
**Success**:
```json
{
  "status": "success",
  "message": "Operation successful",
  "data": { ... }
}
```

**Error**:
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": { "field": ["Error detail"] }
}
```

## Postman Collection
A full Postman collection is included in the root directory: `cms_api_collection.json`.
1.  Import into Postman.
2.  Run the **"Auth > Login"** request first to automatically set your environment token.
3.  Enjoy testing!
