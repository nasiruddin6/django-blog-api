# Django Blog API

A REST API for creating and listing blog posts, built with Django REST Framework and SQLite.

## Features

- List and create blog posts at `/posts/`.
- Validate post data with a model serializer.
- Record creation timestamps automatically.
- Explore endpoints through the browsable API.
- Redirect `/` to `/posts/`.

## Project structure

```text
django_projects/myproject/
├── manage.py
├── blog/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
└── myproject/
    ├── settings.py
    └── urls.py
```

## Local setup

Run from the repository root on Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install Django djangorestframework
cd django_projects/myproject
python manage.py migrate
python manage.py runserver
```

On Windows PowerShell, create and activate the environment with `py -m venv .venv` and `.venv\Scripts\Activate.ps1`, then follow the installation steps above.

Open [localhost:8000](http://127.0.0.1:8000/) to access the API.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Redirect to `/posts/` |
| GET | `/posts/` | List posts |
| POST | `/posts/` | Create a post |
| GET | `/admin/` | Django admin login |

### Create a post

```bash
curl -X POST http://127.0.0.1:8000/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting started with Django",
    "content": "Building a simple blog API.",
    "published_date": "2026-11-17"
  }'
```

Required fields: `title` (maximum 200 characters), `content`, and `published_date` (`YYYY-MM-DD`). The `created_at` timestamp is generated automatically and is read-only.

Successful creation returns `201 Created`. Invalid input returns `400 Bad Request` with field validation errors.

## Check configuration

```bash
python manage.py check
```

Run this command from the directory containing `manage.py`.
