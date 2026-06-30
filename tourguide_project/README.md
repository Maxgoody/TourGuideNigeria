# TourGuide Nigeria

A web-based platform for booking and rating local tour guides and experiences, built with Django and PostgreSQL.

---

## Tech Stack

- **Backend:** Django 4.2 (Python 3.11)
- **Database:** PostgreSQL 15
- **Frontend:** HTML5, Bootstrap 5, Vanilla JavaScript
- **Media Storage:** Cloudinary
- **Static Files:** WhiteNoise
- **Production Server:** Gunicorn + Nginx

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/tourguide-nigeria.git
cd tourguide-nigeria
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env and fill in your PostgreSQL and Cloudinary credentials
```

### 5. Create the PostgreSQL database
```sql
CREATE DATABASE tourguide_db;
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 8. Collect static files
```bash
python manage.py collectstatic
```

### 9. Start the development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Project Structure

```
tourguide_project/
├── tourguide_project/   # Project config (settings, urls, wsgi)
├── accounts/            # User auth, registration, dashboards
├── guides/              # Guide profiles, experience listings, search
├── bookings/            # Booking request and management
├── reviews/             # Ratings and reviews
├── templates/           # All HTML templates
├── static/              # CSS, JS, images
├── requirements.txt
├── .env.example
└── manage.py
```

---

## User Roles

| Role    | Capabilities                                                  |
|---------|---------------------------------------------------------------|
| Tourist | Register, search guides, book experiences, submit reviews     |
| Guide   | Register, manage profile, list experiences, handle bookings   |
| Admin   | Manage users, verify guides, moderate reviews via /admin/     |

---

## Key URLs

| URL                        | Description                  |
|----------------------------|------------------------------|
| `/`                        | Landing page                 |
| `/register/tourist/`       | Tourist registration         |
| `/register/guide/`         | Guide registration           |
| `/login/`                  | Login                        |
| `/dashboard/`              | Role-based dashboard         |
| `/guides/`                 | Guide search and listing     |
| `/guides/<id>/`            | Guide public profile         |
| `/guides/profile/edit/`    | Guide profile editor         |
| `/bookings/`               | Booking management           |
| `/reviews/create/<id>/`    | Review submission            |
| `/admin/`                  | Admin panel                  |

---

## Deployment Notes

- Set `DEBUG=False` in production `.env`
- Set `ALLOWED_HOSTS` to your domain
- Run `collectstatic` before deploying
- Use Gunicorn as WSGI server behind Nginx
- Ensure Cloudinary credentials are configured for media uploads
