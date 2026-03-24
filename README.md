# Django Login - Industry-Standard Architecture for 2026

A production-ready Django REST Framework authentication system with clean architecture, comprehensive API documentation, and industry-standard best practices.

---

## 📋 Table of Contents

1. [Project Structure](#project-structure)
2. [Architecture Overview](#architecture-overview)
3. [Installation & Setup](#installation--setup)
4. [Available Endpoints](#available-endpoints)
5. [Localhost Links](#localhost-links)
6. [VS Code Extensions & Plugins](#vs-code-extensions--plugins)
7. [Required Dependencies](#required-dependencies)
8. [Environment Configuration](#environment-configuration)
9. [Docker Deployment](#docker-deployment)
10. [Development Workflow](#development-workflow)
11. [API Documentation](#api-documentation)

---

## 🗂️ Project Structure

```
django_login/
├── apps/                               # Custom applications (clean structure)
│   ├── accounts/                       # User accounts application
│   │   ├── migrations/                 # Database migrations
│   │   ├── api_tests/                  # API test suite
│   │   ├── admin.py                    # Django admin customization
│   │   ├── apps.py                     # App configuration
│   │   ├── models.py                   # Database models (Profile, Note, Task)
│   │   ├── views.py                    # API views (thin, delegates to services)
│   │   ├── serializers.py              # DRF serializers (validation & conversion)
│   │   ├── services.py                 # Business logic layer (CLEAN ARCHITECTURE)
│   │   ├── permissions.py              # Custom permission classes
│   │   ├── signals.py                  # Django signals for auto-actions
│   │   ├── urls.py                     # URL routing
│   │   ├── utils.py                    # Utility functions
│   │   └── tests.py                    # Unit tests
│   └── __init__.py
│
├── config/                             # Project configuration
│   ├── settings/                       # Split settings for different environments
│   │   ├── base.py                     # Base settings (shared across all environments)
│   │   ├── local.py                    # Development settings (DEBUG=True, CORS relaxed)
│   │   ├── production.py               # Production settings (security hardened, SSL, etc.)
│   │   └── __init__.py
│   ├── urls.py                         # Main URL configuration with API docs & versioning
│   ├── asgi.py                         # ASGI configuration (for async apps)
│   ├── wsgi.py                         # WSGI configuration (production server)
│   └── __init__.py
│
├── templates/                          # Project-wide templates
│   └── accounts/                       # App-specific templates (namespace pattern)
│       └── (HTML templates here)
│
├── static/                             # Static files (CSS, JavaScript, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                              # User-uploaded media files
│
├── requirements/                       # Dependency management (split by environment)
│   ├── base.txt                        # Base dependencies for all environments
│   ├── dev.txt                         # Development-specific dependencies
│   └── prod.txt                        # Production-specific dependencies
│
├── logs/                               # Application logs
│
├── Dockerfile                          # Multi-stage Docker image (production-optimized)
├── docker-compose.yml                  # Docker Compose with PostgreSQL, Redis, Nginx
├── nginx.conf                          # Nginx reverse proxy configuration
│
├── .env                                # Local environment variables (git-ignored)
├── .env.example                        # Example environment variables (git-tracked)
├── .gitignore                          # Git ignore rules
│
├── manage.py                           # Django management CLI
├── pytest.ini                          # Pytest configuration
├── conftest.py                         # Pytest fixtures & configuration
│
└── db.sqlite3                          # SQLite database (development only)
```

---

## 🏗️ Architecture Overview

### Clean Architecture Pattern

This project follows **Clean Architecture** principles with a clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                      REST API Layer                              │
│                    (views.py, serializers.py)                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Business Logic Layer                            │
│                    (services.py)                                 │
│  - AuthenticationService                                         │
│  - ProfileService                                                │
│  - TaskService                                                   │
│  - NoteService                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Data Access Layer                             │
│                    (models.py)                                   │
│  - Profile, Note, Task models                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Database Layer                                │
│              (PostgreSQL/SQLite)                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Architectural Benefits

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Business logic in services can be tested independently
3. **Reusability**: Services can be used by multiple views or external systems
4. **Maintainability**: Changes to one layer don't affect others
5. **Scalability**: Easy to add new features or modify existing ones

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL (optional, SQLite used by default in development)
- Redis (optional, for caching)
- pip or Poetry

### Step 1: Clone the Repository

```bash
cd c:\Users\Lenovo\django_login
```

### Step 2: Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv env
env\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### Step 3: Install Dependencies

```bash
# Development environment
pip install -r requirements/dev.txt

# Production environment
pip install -r requirements/prod.txt
```

### Step 4: Configure Environment

```bash
# Copy example to actual .env file (Windows uses copy)
copy .env.example .env

# Edit .env with your settings
```

### Step 5: Run Migrations

```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### Step 7: Load Fixtures (Optional)

```bash
python manage.py loaddata accounts/fixtures/sample_data.json
```

---

## 🔌 Available Endpoints

### Health Check

```
GET /api/v1/accounts/health/
```

**Response:**
```json
{
  "status": "OK",
  "message": "API is running smoothly"
}
```

### Authentication

#### Register
```
POST /api/v1/accounts/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!"
}
```

**Response (201 Created):**
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login
```
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```
POST /api/v1/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Profile Management

#### Get Profile
```
GET /api/v1/accounts/profile/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "address": "123 Main St",
  "phone": "+1234567890",
  "bio": "Django developer",
  "age": 28,
  "created_at": "2026-03-10T10:00:00Z",
  "updated_at": "2026-03-10T10:00:00Z"
}
```

#### Update Profile
```
PUT /api/v1/accounts/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "phone": "+9876543210",
  "bio": "Senior Django Developer"
}
```

### Tasks Management

#### List Tasks
```
GET /api/v1/accounts/tasks/
Authorization: Bearer <access_token>
```

#### Create Task
```
POST /api/v1/accounts/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the Django project",
  "status": "in_progress"
}
```

#### Get Task by Status
```
GET /api/v1/accounts/tasks/by_status/?status=pending
Authorization: Bearer <access_token>
```

### Notes Management

#### List Notes
```
GET /api/v1/accounts/notes/
Authorization: Bearer <access_token>
```

#### Create Note
```
POST /api/v1/accounts/notes/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "My Note",
  "content": "Note content goes here"
}
```

### Admin Dashboard

```
GET /api/v1/accounts/admin-dashboard/
Authorization: Bearer <admin_access_token>
```

**Response:**
```json
{
  "message": "Welcome, Admin",
  "user": "admin_user",
  "role": "Admin",
  "stats": {
    "total_users": 5,
    "total_tasks": 12,
    "total_notes": 8
  }
}
```

---

## 🌐 Localhost Links

### Development Server

| Service | URL | Purpose |
|---------|-----|---------|
| **Django App** | http://localhost:8000 | Main API server |
| **API Swagger Docs** | http://localhost:8000/api/v1/docs/swagger/ | Interactive API documentation |
| **API ReDoc** | http://localhost:8000/api/v1/docs/redoc/ | API documentation (alternative UI) |
| **OpenAPI Schema** | http://localhost:8000/api/v1/docs/schema/ | Raw OpenAPI schema (JSON) |
| **Django Admin** | http://localhost:8000/admin/ | Admin panel |
| **Health Check** | http://localhost:8000/api/v1/accounts/health/ | API health status |

### Docker Services

| Service | URL | Purpose |
|---------|-----|---------|
| **Web App (Docker)** | http://localhost:8000 | Django app container |
| **Nginx Proxy** | http://localhost:80 | Reverse proxy (load balancing) |
| **PostgreSQL** | localhost:5432 | Database (if using Docker) |
| **Redis** | localhost:6379 | Cache/Session store (if using Docker) |

### Database Tools (Optional)

| Tool | Connection String |
|------|-------------------|
| **pgAdmin** | http://localhost:5050 (if added to docker-compose) |
| **Redis Commander** | http://localhost:8081 (if added to docker-compose) |

---

## 🔧 VS Code Extensions & Plugins

### Recommended Extensions

#### Core Development
1. **Python** (microsoft.python)
   - IntelliSense, linting, debugging
   - Install: `ext install ms-python.python`

2. **Pylance** (ms-python.vscode-pylance)
   - Advanced Python type checking
   - Install: `ext install ms-python.vscode-pylance`

3. **Django** (batisteo.vscode-django)
   - Django template support and commands
   - Install: `ext install batisteo.vscode-django`

4. **REST Client** (humao.rest-client)
   - Test REST APIs directly in VS Code
   - Install: `ext install humao.rest-client`

#### Code Quality
5. **Black Formatter** (ms-python.black-formatter)
   - Python code formatter
   - Install: `ext install ms-python.black-formatter`

6. **Pylint** (ms-python.pylint)
   - Python linter
   - Install: `ext install ms-python.pylint`

7. **isort** (ms-python.isort)
   - Import sorting
   - Install: `ext install ms-python.isort`

8. **Flake8** (ms-python.flake8)
   - Python linter
   - Install: `ext install ms-python.flake8`

#### Database & API
9. **Thunder Client** (rangav.vscode-thunder-client)
   - API testing tool (alternative to Postman)
   - Install: `ext install rangav.vscode-thunder-client`

10. **SQLTools** (mtxr.sqltools)
    - Database explorer and query runner
    - Install: `ext install mtxr.sqltools`

11. **PostgreSQL** (ckolkman.vscode-postgres)
    - PostgreSQL database management
    - Install: `ext install ckolkman.vscode-postgres`

#### Git & Collaboration
12. **GitLens** (eamodio.gitlens)
    - Advanced git features
    - Install: `ext install eamodio.gitlens`

13. **GitHub Copilot** (GitHub.copilot)
    - AI-powered code suggestions
    - Install: `ext install GitHub.copilot`

#### Docker
14. **Docker** (ms-azuretools.vscode-docker)
    - Docker and Docker Compose support
    - Install: `ext install ms-azuretools.vscode-docker`

15. **Dev Containers** (ms-vscode-remote.remote-containers)
    - Develop inside containers
    - Install: `ext install ms-vscode-remote.remote-containers`

#### Utilities
16. **Environment Manager** (irongeek.vscode-env)
    - .env file syntax highlighting
    - Install: `ext install irongeek.vscode-env`

17. **Thunder Client** (rangav.vscode-thunder-client)
    - API testing
    - Install: `ext install rangav.vscode-thunder-client`

18. **Better Comments** (aaron-bond.better-comments)
    - Color-coded comments
    - Install: `ext install aaron-bond.better-comments`

19. **Error Lens** (usernamehw.errorlens)
    - Show errors inline
    - Install: `ext install usernamehw.errorlens`

20. **Code Spell Checker** (streetsidesoftware.code-spell-checker)
    - Spell checking
    - Install: `ext install streetsidesoftware.code-spell-checker`

### Extension Installation Script

```powershell
# Run this in VS Code terminal to install all extensions
$extensions = @(
    "ms-python.python",
    "ms-python.vscode-pylance",
    "batisteo.vscode-django",
    "humao.rest-client",
    "ms-python.black-formatter",
    "ms-python.pylint",
    "ms-python.isort",
    "ms-python.flake8",
    "rangav.vscode-thunder-client",
    "mtxr.sqltools",
    "ckolkman.vscode-postgres",
    "eamodio.gitlens",
    "GitHub.copilot",
    "ms-azuretools.vscode-docker",
    "ms-vscode-remote.remote-containers",
    "irongeek.vscode-env",
    "aaron-bond.better-comments",
    "usernamehw.errorlens",
    "streetsidesoftware.code-spell-checker"
)

foreach ($ext in $extensions) {
    code --install-extension $ext
}
```

---

## 📦 Required Dependencies

### Base Dependencies (requirements/base.txt)
```
Django==6.0
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
psycopg2-binary==2.9.10
python-decouple==3.8
django-cors-headers==4.4.0
django-filter==24.1
pytz==2025.1
PyJWT==2.10.1
requests==2.32.5
celery==5.4.0
redis==5.0.4
```

### Development Dependencies (requirements/dev.txt)
```
# Testing
pytest==9.0.2
pytest-django==4.11.1
pytest-cov==4.1.0
factory-boy==3.3.0

# Code Quality
black==24.10.0
isort==5.13.2
flake8==7.0.0
pylint==3.0.3
mypy==1.7.0

# Development Tools
django-extensions==3.2.3
ipython==8.19.0
drf-spectacular==0.40.0
Werkzeug==3.0.1

# Debugging
django-debug-toolbar==4.2.0
django-silk==5.1.0
```

### Production Dependencies (requirements/prod.txt)
```
gunicorn==23.0.0
whitenoise==6.6.0
sentry-sdk==1.48.0
django-redis==5.4.0
django-cachalot==2.6.3
```

---

## 🌍 Environment Configuration

### Local Development (.env)
```env
DJANGO_SETTINGS_MODULE=config.settings.local
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DJANGO_LOG_LEVEL=INFO
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
REDIS_URL=redis://localhost:6379/0
```

### Production (.env)
```env
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_login_db
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/0
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SENTRY_DSN=your-sentry-dsn
```

---

## 🐳 Docker Deployment

### Build and Run

```bash
# Build Docker image
docker build -t django-login:latest .

# Run with Docker Compose
docker-compose up -d

# Run migrations in container
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web
```

### Docker Compose Services

- **Web**: Django application with Gunicorn
- **Postgres**: Database (PostgreSQL 15)
- **Redis**: Cache and session store
- **Nginx**: Reverse proxy and load balancer

---

## 💻 Development Workflow

### Run Development Server

```bash
python manage.py runserver
# or
python manage.py runserver 0.0.0.0:8000
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest apps/accounts/api_tests/test_login.py

# Run with verbose output
pytest -v
```

### Create Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Access Django Shell

```bash
python manage.py shell_plus
```

### Code Formatting

```bash
# Format code with Black
black apps/

# Sort imports
isort apps/

# Run linter
flake8 apps/

# Type checking
mypy apps/
```

---

## 📚 API Documentation

### Swagger UI (Interactive)
```
http://localhost:8000/api/v1/docs/swagger/
```

### ReDoc (Alternative UI)
```
http://localhost:8000/api/v1/docs/redoc/
```

### OpenAPI Schema (JSON)
```
http://localhost:8000/api/v1/docs/schema/
```

### Try in Thunder Client

1. Open Thunder Client extension in VS Code
2. Create new request
3. Set method to POST
4. Use endpoint URL (e.g., `http://localhost:8000/api/v1/accounts/register/`)
5. Add JSON body and send

---

## 📋 Project Highlights

✅ **Clean Architecture** - Separation of concerns with service layer  
✅ **JWT Authentication** - Secure token-based authentication  
✅ **API Versioning** - `/api/v1/` prefix for future-proofing  
✅ **Comprehensive Documentation** - Swagger & ReDoc  
✅ **Environment Management** - Separate settings for dev/prod  
✅ **Docker Support** - Production-ready containerization  
✅ **Security Hardened** - CORS, CSRF, SSL/TLS support  
✅ **Caching** - Redis integration for performance  
✅ **Testing** - pytest fixtures and test suite  
✅ **Logging** - Structured logging for all environments  

---

## 🚀 Quick Start Commands

```bash
# Development
python manage.py runserver 0.0.0.0:8000

# Production (Docker)
docker-compose up -d

# Migrations
python manage.py migrate

# Tests
pytest --cov=apps

# Format code
black . && isort .

# Shell
python manage.py shell_plus
```

---

## 📞 Support & Documentation

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- JWT Docs: https://django-rest-framework-simplejwt.readthedocs.io/
- drf-spectacular: https://drf-spectacular.readthedocs.io/

---

## 📝 License

This project is licensed under the MIT License.

---

## 🎉 You're All Set!

Your Django project is now structured following industry-standard best practices for 2026. Start building amazing APIs! 🚀
