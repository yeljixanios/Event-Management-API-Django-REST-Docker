# Event Management API

A comprehensive RESTful API service for managing events and user registrations, built with **Django REST Framework**.

The project is fully containerized using **Docker** and includes advanced features like filtering, search, and email notifications.

## Features

* **Events Management:** Full CRUD operations (Create, Read, Update, Delete) for events.
* **User Registration:** Secure user sign-up and authentication system(Token-based).
* **Event Registration:** Users can register for specific events.
* **Prevent Double Booking:** Validation to ensure a user cannot register for the same event twice.
* **Documentation:** Auto-generated Swagger/OpenAPI documentation.
* **Dockerized:** Easy setup with Docker and Docker Compose.

### Bonus Features Implemented
* ✅ **Advanced Filtering:** Filter events by date (`?date=2025-10-10`) or location (`?location=Kyiv`).
* ✅ **Search:** Search events by title or description (`?search=Python`).
* ✅ **Email Notifications:** Automatic email confirmation sent to the user upon successful registration (Console Backend).

---

## Tech Stack

* **Language:** Python 3.11
* **Framework:** Django 5.0, Django REST Framework
* **Database:** PostgreSQL 15
* **Infrastructure:** Docker, Docker Compose
* **Docs:** drf-spectacular (Swagger UI)

---

## API Endpoints

### Auth
* `POST /api/register/` — Register a new user
* `POST /api/login/` — Login (obtain auth token)

### Events
* `GET /api/events/` — List all events (supports filters)
* `POST /api/events/` — Create a new event
* `GET /api/events/{id}/` — Retrieve specific event details
* `PUT|PATCH /api/events/{id}/` — Update an event
* `DELETE /api/events/{id}/` — Delete an event

### Registrations
* `POST /api/registrations/` — Register for an event
* `GET /api/registrations/` — View registrations
* `GET /api/registrations/{id}/` — View specific registration details
* `DELETE /api/registrations/{id}/` — Cancel registration

---

## Getting Started

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yeljixanios/Event-Management-API-Django-REST-Docker/
    cd event_manager
    ```

2.  **Create `.env` file:**
    Create a file named `.env` in the root directory and add the following config:
    ```ini
    SECRET_KEY=<YOUR_TEST_KEY>
    DEBUG=1
    ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

    POSTGRES_DB=events_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    ```

3.  **Build and Run with Docker:**
    ```bash
    docker-compose up --build
    ```

4.  **Apply Migrations:**
    Open a new terminal tab and run:
    ```bash
    docker-compose run --rm web python manage.py migrate
    ```

5.  **Create Superuser (Admin):**
    ```bash
    docker-compose run --rm web python manage.py createsuperuser
    ```

---

## API Documentation

Once the server is running, you can access the interactive API documentation:

* **Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
* **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Testing

### 1. Filtering & Search
You can test filtering via URL parameters:
* `GET /api/events/?location=Kyiv`
* `GET /api/events/?search=Conference`

### 2. Email Notifications (Bonus)
Since this is a test environment, the email backend is set to `console` to avoid SMTP configuration.

**How to verify:**
1.  Register a user for an event via the API.
    **Important:** Ensure the user has a valid **email address** set.
2.  Check the **Terminal/Logs** where `docker-compose` is running.
3.  You will see the raw email text printed in the console.

---

