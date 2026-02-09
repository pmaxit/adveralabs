# Django Website Setup

This is the Django version of the Advera Labs website.

## Project Structure

```
adveralabs/
├── manage.py
├── adveralabs/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── website/
    ├── __init__.py
    ├── apps.py
    ├── urls.py
    ├── views.py
    ├── templates/
    │   └── website/
    │       └── home.html
    └── static/
        └── website/
            ├── css/
            │   └── styles.css
            └── js/
                └── script.js
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Collect Static Files

```bash
python manage.py collectstatic
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The website will be available at `http://127.0.0.1:8000/`

## Features

- **Django Template System**: Uses Django's template engine with static file handling
- **CSRF Protection**: Built-in CSRF protection for forms
- **AJAX ROI Calculator**: Backend API endpoint for ROI calculations
- **Static Files**: CSS and JavaScript served through Django's static files system
- **Responsive Design**: Mobile-first responsive design

## URLs

- `/` - Home page
- `/calculate-roi/` - ROI calculator API endpoint (POST)
- `/admin/` - Django admin interface

## Static Files

Static files are located in `website/static/website/`:
- CSS: `website/static/website/css/styles.css`
- JavaScript: `website/static/website/js/script.js`

## Templates

Templates are located in `website/templates/website/`:
- Home page: `website/templates/website/home.html`

## Environment Variables

Set these in your `.env` file or environment:

```bash
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Production Deployment

For production:

1. Set `DEBUG=False` in settings
2. Set a secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use a production WSGI server (gunicorn, uwsgi)
5. Set up static file serving (WhiteNoise or CDN)
6. Configure database (PostgreSQL recommended)

## Notes

- The website uses Django's static files system
- CSRF tokens are automatically included in forms
- The ROI calculator uses AJAX to call the Django backend
- All static assets are versioned and cached appropriately

