# Conference Management System - API Guide

**Version:** 1.0  
**Date:** January 16, 2026

---

## 1. Introduction
The **Conference Management System (CMS)** is a robust RESTful API built with Django and Django REST Framework. It provides comprehensive management for professional conferences, including session scheduling, attendee registration, payment simulation, and analytical reporting.

This guide details the setup, authentication, and usage of the API versions `v1`.

---

## 2. Setup & Installation

### Prerequisites
- Python 3.10+
- MySQL Server (Optional, SQLite is strictly default)

### Installation Steps
1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd cms_project
    ```
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Key Libraries: `django`, `djangorestframework`, `djangorestframework-simplejwt`, `pymysql`.*

3.  **Initialize Database**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Seed Data**
    Populate the database with sample conferences and attendees:
    ```bash
    python manage.py populate_data
    ```

5.  **Run Server**
    ```bash
    python manage.py runserver
    ```
    The API will be available at: `http://127.0.0.1:8000/api/v1/`

---

## 3. Authentication
The API uses **JWT (JSON Web Token)** for security. All endpoints (except login and public pages) require a valid token.

### Headers
Every authenticated request must include the following header:
```
Authorization: Bearer <your_access_token>
```

### 3.1 Login (Get Token)
*   **Endpoint**: `POST /api/v1/token/`
*   **Description**: Authenticate a user and receive an access/refresh token pair.
*   **Request Body**:
    ```json
    {
        "username": "admin",
        "password": "your_password"
    }
    ```
*   **Response**:
    ```json
    {
        "status": "success",
        "message": "Operation successful",
        "data": {
            "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
            "access": "eyJ0eXAiOiJKV1QiLCJh..."
        }
    }
    ```

### 3.2 Refresh Token
*   **Endpoint**: `POST /api/v1/token/refresh/`
*   **Request Body**:
    ```json
    {
        "refresh": "your_refresh_token"
    }
    ```

---

## 4. Universal Response Format
All API responses follow a strict, predictable structure.

**Success Response**:
```json
{
    "status": "success",
    "message": "Operation successful",
    "data": { ... result object or list ... }
}
```

**Error Response**:
```json
{
    "status": "error",
    "message": "Validation failed",
    "errors": {
        "field_name": ["Error detail"]
    }
}
```

---

## 5. API Reference

### 5.1 Conferences

#### List All Conferences
*   **Endpoint**: `GET /api/v1/conferences/`
*   **Response**: List of all conferences.

#### List Upcoming Conferences
*   **Endpoint**: `GET /api/v1/conferences/upcoming/`
*   **Description**: Specialized endpoint for future events.

#### Create Conference
*   **Endpoint**: `POST /api/v1/conferences/`
*   **Body**:
    ```json
    {
        "conference_name": "Tech Summit 2026",
        "start_date": "2026-09-01",
        "end_date": "2026-09-03",
        "location": "San Francisco",
        "description": "Global tech/AI summit."
    }
    ```

#### Get Conference Details
*   **Endpoint**: `GET /api/v1/conferences/{id}/`
*   **Description**: Get details of a specific conference.

#### Update Conference
*   **Endpoint**: `PUT /api/v1/conferences/{id}/`
*   **Body**: JSON object with updated fields.

#### Delete Conference
*   **Endpoint**: `DELETE /api/v1/conferences/{id}/`
*   **Description**: Soft deletes the conference.

---

### 5.2 Sessions

#### List All Sessions
*   **Endpoint**: `GET /api/v1/sessions/`
*   **Response**: List of all sessions.

#### Create Session
*   **Endpoint**: `POST /api/v1/sessions/`
*   **Body**:
    ```json
    {
        "session_name": "Keynote: Future of AI",
        "conference": 1,
        "speaker": "Jane Doe",
        "start_time": "2026-09-01T09:00:00Z",
        "end_time": "2026-09-01T10:30:00Z",
        "max_attendees": 500,
        "price": 0.00
    }
    ```
*   **Validation**: Start time must be before End time. Sessions cannot overlap within the same conference.

#### Get Session Details
*   **Endpoint**: `GET /api/v1/sessions/{id}/`

#### Update Session
*   **Endpoint**: `PUT /api/v1/sessions/{id}/`

#### Delete Session
*   **Endpoint**: `DELETE /api/v1/sessions/{id}/`

---

### 5.3 Attendees & Recommendations

#### List All Attendees
*   **Endpoint**: `GET /api/v1/attendees/`

#### Create Attendee
*   **Endpoint**: `POST /api/v1/attendees/`
*   **Body**:
    ```json
    {
        "attendee_name": "John Smith",
        "email": "john@example.com",
        "phone_number": "123-456-7890",
        "organization": "Innovate Corp"
    }
    ```

#### Get Attendee Details
*   **Endpoint**: `GET /api/v1/attendees/{id}/`

#### Update Attendee
*   **Endpoint**: `PUT /api/v1/attendees/{id}/`

#### Delete Attendee
*   **Endpoint**: `DELETE /api/v1/attendees/{id}/`

#### Get Recommendations
*   **Endpoint**: `GET /api/v1/attendees/{id}/recommendations/?email=true`
*   **Description**: Get suggested sessions based on the attendee's interest (speaker overlap or topic match). Optionally sends an email.

---

### 5.4 Registrations & Payments

#### List All Registrations
*   **Endpoint**: `GET /api/v1/registrations/`

#### Create Registration
*   **Endpoint**: `POST /api/v1/registrations/`
*   **Body**:
    ```json
    {
        "conference": 1,
        "session": 5,
        "attendee": 10
    }
    ```
*   **Rules**: Checks for session capacity and attendee schedule conflicts.

#### Get Registration Details
*   **Endpoint**: `GET /api/v1/registrations/{id}/`

#### Update Registration
*   **Endpoint**: `PUT /api/v1/registrations/{id}/`

#### Delete Registration
*   **Endpoint**: `DELETE /api/v1/registrations/{id}/`

#### Process Payment
*   **Endpoint**: `POST /api/v1/payments/process/`
*   **Body**:
    ```json
    {
        "registration_id": 15
    }
    ```
*   **Description**: Simulates payment gateway. Returns `"Paid"` or `"Failed"` (80% success rate).

---

### 5.5 Reports, Search & Logs

#### Search
*   **Endpoint**: `GET /api/v1/search/?q=Keyword`
*   **Scope**: Searches Conference Names, Descriptions, Session Names, and Speakers.

#### Conference Report
*   **Endpoint**: `GET /api/v1/reports/conferences/`
*   **Data**: Conference Name, Total Sessions, Unique Attendees.

#### Session Report
*   **Endpoint**: `GET /api/v1/reports/sessions/`
*   **Data**: Session Name, Total Registrations, Remaining Capacity, Revenue.

#### Request Logs
*   **Endpoint**: `GET /api/v1/core/logs/`
*   **Description**: View API request logs (method, path, user, timestamp).

## 6. Testing

### Using Postman
1.  Import the provided `cms_api_collection.json`.
2.  Open the **"Auth"** folder and run **"Login (Get Token)"**.
3.  The `access_token` will be automatically saved to your environment.
4.  Run any other request; authentication is handled automatically.

---

