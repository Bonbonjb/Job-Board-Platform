# Job Platform API

A comprehensive job board platform built with Django and Django REST Framework that enables users to:

- Browse and search for jobs by category, type, location, and more
- Employers can post and manage job listings
- Authenticated users can apply to jobs with cover letters and resumes
- Track application status with real-time updates
- Admins manage users, jobs, and applications via Django Admin panel

## 🚀 Features
 
- CRUD for jobs, categories, and applications
- JWT-based authentication and token refresh      
- PostgreSQL database integration  
- Dockerized development and production environments
- User registration and login using email as username  
- JWT authentication with **djangorestframework-simplejwt**  
- Custom user model with role distinction (employer vs. job seeker)  
- Job postings with categories, job types, salary, and status  
- Job applications with status tracking (pending, reviewed, accepted, rejected)  
- File upload support for resumes  
- Pagination, filtering, and search for API endpoints  
- Secure permissions to protect data and actions
- Asynchronous task queue using Celery and Redis
- Comprehensive API documentation with Swagger and ReDoc  
- Deployment ready with PostgreSQL support and environment configurations  

## 🛠️ Tech Stack

- Backend Framework: Django & Django REST Framework  
- Authentication: Custom User Model + JWT Authentication  
- Database: PostgreSQL  
- API Documentation: drf-spectacular (Swagger UI and ReDoc)  
- File Storage: Local media files (resume uploads)  
- Deployment: Render.com  

## 📁 Project Structure
```
job_platform/
├── manage.py
├── job_platform/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── jobs/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── applications/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── templates/
│   └── index.html (API docs landing page)
└── media/ (uploaded resumes)
```
## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/bonbonjb/job-platform-api.git
cd job-platform-api
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

---

## 🔑 Authentication

This API uses **JWT tokens** for authentication, powered by `djangorestframework-simplejwt`.

### Obtain Token

```http
POST /api/token/
```

**Payload:**

```json
{
  "email": "your@email.com",
  "password": "yourpassword"
}
```

### Refresh Token

```http
POST /api/token/refresh/
```

**Payload:**

```json
{
  "refresh": "<your_refresh_token>"
}
```

### 📌 Use the Token

Include the access token in the `Authorization` header of authenticated requests:

```http
Authorization: Bearer <access_token>
```

---

### Use the Token

Include the access token in the Authorization header:

Authorization: Bearer <access_token>

## 📌 API Endpoints Overview

### Users

| Method | Endpoint             | Description             | Auth Required |
|--------|----------------------|-------------------------|---------------|
| GET    | /api/users/          | List users (admin only) | ✅            |
| POST   | /api/users/register/ | Register new user       | ❌            |
| POST   | /api/token/          | Obtain JWT token        | ❌            |

---

### Jobs

| Method | Endpoint          | Description                 | Auth Required |
|--------|-------------------|-----------------------------|---------------|
| GET    | /api/jobs/        | List all active jobs        | ❌            |
| POST   | /api/jobs/        | Create a new job (employer) | ✅            |
| GET    | /api/jobs/<id>/   | Get job details             | ❌            |
| PUT    | /api/jobs/<id>/   | Update job (owner only)     | ✅            |
| DELETE | /api/jobs/<id>/   | Delete job (owner only)     | ✅            |

---

### Applications

| Method | Endpoint                | Description                              | Auth Required |
|--------|-------------------------|------------------------------------------|---------------|
| GET    | /api/applications/      | List user’s applications                 | ✅            |
| POST   | /api/applications/      | Apply for a job                          | ✅            |
| PUT    | /api/applications/<id>/ | Update application status (admin/employer) | ✅            |

---

See full documentation at /api/docs/swagger/ or /api/docs/redoc/.

---

🙋🏽‍♂ Author

Brenda Jematia Bonareri  
📫 Contact: brendabjematia@gmail.com  
🌐 Hosted app: https://job-board-platform-a4ll.onrender.com/

---
