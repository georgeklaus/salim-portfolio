# Portfolio Backend

Django backend for a portfolio site. It exposes JSON endpoints for profile, projects, skills, experience, education, and contact messages.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The portfolio frontend runs at `http://127.0.0.1:8000/`.
The API runs at `http://127.0.0.1:8000/api/`.

## Endpoints

- `GET /api/health/`
- `GET /api/profile/`
- `GET /api/projects/`
- `GET /api/skills/`
- `GET /api/experience/`
- `GET /api/education/`
- `POST /api/contact/`

Manage portfolio content through Django admin at `http://127.0.0.1:8000/admin/`.

## Render Deployment

This repo includes `render.yaml`, so the fastest path is Render Blueprints:

1. Push this project to GitHub.
2. In Render, create a new Blueprint from the repository.
3. Apply the blueprint and wait for the build to finish.
4. Open the Render Shell for the web service and run:

```bash
python manage.py createsuperuser
```

If Render Shell is not available on your plan, add these environment variables
to the web service and redeploy:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

The deploy will create or update that admin account automatically.

## Contact Email

The contact form stores each message in Django admin and can also email you.
Configure SMTP with environment variables:

- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`
- `CONTACT_RECIPIENT_EMAIL`

For the easiest setup without a custom domain, use Gmail SMTP with a Google App
Password:

- `EMAIL_HOST`: `smtp.gmail.com`
- `EMAIL_PORT`: `587`
- `EMAIL_USE_TLS`: `True`
- `EMAIL_HOST_USER`: your Gmail address
- `EMAIL_HOST_PASSWORD`: your Google App Password
- `DEFAULT_FROM_EMAIL`: your Gmail address
- `CONTACT_RECIPIENT_EMAIL`: where you want messages delivered

If you later verify a domain, Resend or Brevo SMTP can use the same variables.

For a manual Render web service, use:

- Build command: `./build.sh`
- Start command: `python -m gunicorn backend.wsgi:application`
- Environment variables:
  - `DATABASE_URL`: your Render PostgreSQL internal database URL
  - `DJANGO_SECRET_KEY`: generated secret
  - `DJANGO_DEBUG`: `False`
  - `PYTHON_VERSION`: `3.13.5`
  - `DJANGO_SUPERUSER_USERNAME`: your admin username
  - `DJANGO_SUPERUSER_EMAIL`: your admin email
  - `DJANGO_SUPERUSER_PASSWORD`: your admin password
