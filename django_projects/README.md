# Django Blog API

**A small backend project with a complete request-to-database journey.**

Built as a homework project, this API explores how Django and Django REST Framework work together to turn a blog post into validated, stored, and readable JSON data.

`Python` · `Django` · `Django REST Framework` · `SQLite`

---

## What this project does

- Lists saved blog posts through a GET request.
- Creates blog posts through a POST request.
- Validates incoming data with a model serializer.
- Records the creation time automatically.
- Provides a browsable API for trying requests directly in a browser.
- Redirects the homepage to the posts endpoint.
- Includes Django's admin route.

The current scope is deliberately small: listing and creating posts. Post detail, editing, deletion, and custom authentication are possible future additions.

## How a request travels

```text
Browser / API client
        |
        v
URL route: /posts/
        |
        v
PostCreateView (ListCreateAPIView)
        |
        v
PostSerializer <--> Post model <--> SQLite
        |
        v
JSON response
```

## Project structure

```text
django_projects/
├── README.md
└── myproject/
    ├── manage.py
    ├── blog/
    │   ├── migrations/
    │   ├── models.py       # Blog post fields
    │   ├── serializers.py  # Validation and JSON representation
    │   ├── urls.py         # Posts endpoint
    │   └── views.py        # List and create behavior
    └── myproject/
        ├── settings.py     # Application and database settings
        └── urls.py         # Root redirect and URL routing
```

SQLite creates `myproject/db.sqlite3` when migrations are applied.

## Run locally

Open a terminal in the repository root, where this README is located.

### 1. Create a virtual environment

On Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install Django djangorestframework
```

### 3. Prepare the database and start the server

```bash
cd myproject
python manage.py migrate
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**. It redirects to **http://127.0.0.1:8000/posts/**, where you can browse posts and submit a new one.

Stop the server with **Ctrl+C**.

## API reference

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/` | Redirects to `/posts/` with HTTP 302 |
| GET | `/posts/` | Returns the list of posts with HTTP 200 |
| POST | `/posts/` | Creates a valid post with HTTP 201 |
| GET | `/admin/` | Opens Django's admin login |

### Post fields

| Field | Type | Rules |
| --- | --- | --- |
| `title` | String | Required; maximum 200 characters |
| `content` | String | Required; post body |
| `published_date` | Date | Required; `YYYY-MM-DD` format |
| `created_at` | Date and time | Generated automatically; read-only |

### Create a post

```bash
curl -X POST http://127.0.0.1:8000/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My first Django API",
    "content": "Today I connected a model, a serializer, and a view.",
    "published_date": "2026-11-17"
  }'
```

Example response; the creation timestamp will depend on when you send the request:

```json
{
  "title": "My first Django API",
  "content": "Today I connected a model, a serializer, and a view.",
  "published_date": "2026-11-17",
  "created_at": "2026-11-17T14:30:00Z"
}
```

### Read posts

```bash
curl http://127.0.0.1:8000/posts/
```

The response is a JSON array. Before any posts are created, it is `[]`. Invalid POST data returns HTTP 400 with field-specific validation errors.

## Lessons from this homework

| Concept | Where it appears |
| --- | --- |
| Models and migrations | Defining a post and creating its database table |
| Serializers | Validating input and representing model data as JSON |
| Generic API views | Supporting GET and POST with `ListCreateAPIView` |
| URL routing | Connecting `/posts/` to the view |
| Redirects | Sending homepage visitors to the API |
| HTTP status codes | Understanding 200, 201, 302, 400, 404, and 405 |

### A routing issue I learned to fix

The homepage originally returned **404** because the URL configuration only matched `admin/` and `posts/`. Including an app's URLs under an empty prefix does not automatically create a homepage; an empty route still needs a matching view.

The fix adds a root redirect to the named posts route. The posts view also uses `ListCreateAPIView`, allowing both browser GET requests and POST requests to create posts. A create-only view would reject GET with **405 Method Not Allowed**.

## Quick troubleshooting

| Symptom | What to check |
| --- | --- |
| `404 Page not found` | Compare the requested path with the patterns in `urls.py`. |
| `405 Method Not Allowed` | Check whether the view supports the request's HTTP method. |
| `No module named django` | Activate the virtual environment and install dependencies. |
| `no such table: blog_post` | Run `python manage.py migrate` from the folder containing `manage.py`. |
| Port already in use | Try `python manage.py runserver 8001` and open port 8001. |

## Optional admin access

From the folder containing `manage.py`, run:

```bash
python manage.py createsuperuser
```

Then sign in at **http://127.0.0.1:8000/admin/**. Models appear in the admin only after they are registered in `blog/admin.py`.

---

*Homework milestone: define the data, validate the input, save a post, and read it back through an API.*
