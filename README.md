# Inkwell API 🛠️
The backend for the Inkwell blogging and note-taking starter app, built with Django and Django REST Framework.

This repo handles user accounts, blog post publishing, note creation, permissions, and JWT-based authentication, ready to pair with the Inkwell UI frontend.

## 🧰 Tech Stack
* Django 4+

* Django REST Framework

* djangorestframework-simplejwt for token auth

* bleach for HTML sanitization

* SQLite for local development (can swap for Postgres)

* CORS headers for frontend API access

## 📦 Features
📝 Blog Posts – Create, edit, publish, and filter posts

🔐 User Auth – Register, login, JWT token handling

✏️ Notes – Private note-taking per user

👥 Groups & Roles – Admin, Editor, Writer permission system

🧽 Clean HTML – User-submitted content is sanitized

## 🧑‍💻 Getting Started
1. Clone the Repo
    ```sh 
    git clone https://github.com/your-org/inkwell_api.git
   cd inkwell_api
    ```

2. Create & Activate a Virtual Environment
    ```sh
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    ```
3. Install Dependencies
    ```sh
    pip install -r requirements.txt
    ```

4. Environment Setup
Create a .env file in the root directory:

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

You can also set CORS_ALLOWED_ORIGINS in settings.py to match your frontend dev server.

## 🛠️ Migrations & Superuser
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

🚀 Start the Dev Server
```sh
python manage.py runserver
```

API should now be live at http://localhost:8000/api/

## 🔑 Authentication
JWT tokens are obtained via /api/auth/token/

Refresh via /api/auth/token/refresh/

Current user endpoint: /api/auth/current_user/

Tokens are stored client-side in localStorage by the frontend.

## ✍️ Blog & Notes Endpoints
/api/posts/ – Create, edit, view posts

/api/posts/published/ – Public posts only

/api/notes/ – Private note-taking (auth required)

## 🛡️ Role System (Groups)
Three default roles:

Admin – Can do everything

Editor – Can edit and publish all posts

Writer – Can manage only their own posts

Roles are managed via Django’s built-in Groups and enforced in code.

## ✅ Deployment
You can deploy this backend via:

Render (free Django app)

Heroku (with gunicorn)

DigitalOcean App Platform

Or self-hosted on a VPS

For production, set:

DEBUG=False

Proper ALLOWED_HOSTS

Production-ready database (e.g. PostgreSQL)

### 🔐 Setting a Secret Key

Django uses a `SECRET_KEY` for signing JWTs, sessions, and more.

For local development, a default key is provided. **For production, you must generate your own.**

Run this command to generate a secure key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'


## 🧪 Running Tests
```sh
python manage.py test
```

## 🧹 Admin Panel
Visit http://localhost:8000/admin/
Log in with your superuser credentials.

Use the panel to manage:

Users

Blog posts

Notes

Groups and permissions

Happy building! 🧱
See also: Inkwell UI frontend

