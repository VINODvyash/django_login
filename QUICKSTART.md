# 🚀 QUICK START GUIDE

## 1️⃣ Initial Setup (5 minutes)

```bash
# Navigate to project
cd c:\Users\Lenovo\django_login

# Create virtual environment
python -m venv env

# Activate virtual environment (Windows)
.\env\Scripts\activate

# Install dependencies
pip install -r requirements/dev.txt

# Copy environment file
copy .env.example .env

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

## 2️⃣ Start Development Server (1 minute)

```bash
python manage.py runserver 0.0.0.0:8000
```

## 3️⃣ Access the Application

### Main Links:
| Purpose | URL |
|---------|-----|
| API Health Check | http://localhost:8000/api/v1/accounts/health/ |
| **Swagger Docs** | **http://localhost:8000/api/v1/docs/swagger/** |
| ReDoc Documentation | http://localhost:8000/api/v1/docs/redoc/ |
| Admin Panel | http://localhost:8000/admin/ |

## 4️⃣ Test API Endpoints

### Using Thunder Client (VS Code Extension)

1. Open VS Code
2. Click Thunder Client icon (sidebar)
3. New Request
4. Create POST request to: `http://localhost:8000/api/v1/accounts/register/`

**Request Body:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "TestPass123!",
  "password_confirm": "TestPass123!"
}
```

5. Send and see response!

### Using cURL (Terminal)

```bash
# Register
curl -X POST http://localhost:8000/api/v1/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

## 5️⃣ Key Features

✅ **Authentication**: JWT token-based authentication  
✅ **Profile Management**: Update user profiles  
✅ **Task Management**: Create, read, update tasks  
✅ **Notes**: Create and manage personal notes  
✅ **Admin Dashboard**: View system statistics  
✅ **Clean Architecture**: Services layer for business logic  

## 6️⃣ Useful Commands

```bash
# Run with custom port
python manage.py runserver 0.0.0.0:3000

# Run tests
pytest

# Format code
black . && isort .

# Django shell
python manage.py shell_plus

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic
```

## 7️⃣ Docker Setup (Alternative)

```bash
# Start all services
docker-compose up -d

# Run migrations in Docker
docker-compose exec web python manage.py migrate

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## 8️⃣ VS Code Recommended Extensions

Click Extensions (Ctrl+Shift+X) and search for:

- Python (Microsoft)
- Pylance (Microsoft)
- Django (batisteo)
- REST Client (humao)
- Docker (Microsoft)
- Thunder Client (rangav)
- Django Snippets (nicolas)
- SQLTools (mtxr)

## 9️⃣ Project Structure

```
django_login/
├── apps/accounts/          # Main application
│   ├── models.py           # Database models
│   ├── views.py            # API endpoints
│   ├── serializers.py      # Data validation
│   ├── services.py         # Business logic ⭐
│   └── urls.py             # Routes
├── config/
│   ├── settings/           # Split settings (dev/prod)
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py             # Main routes
│   └── wsgi.py
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # User uploads
├── requirements/           # Dependencies
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
└── manage.py               # CLI tool
```

## 🔟 API Endpoint Examples

### Register New User
```
POST /api/v1/accounts/register/
```

### Get JWT Token
```
POST /api/v1/auth/token/
```

### Access Protected Endpoint
```
GET /api/v1/accounts/profile/
Header: Authorization: Bearer <token>
```

### Create Task
```
POST /api/v1/accounts/tasks/
Header: Authorization: Bearer <token>
```

### List Tasks
```
GET /api/v1/accounts/tasks/
Header: Authorization: Bearer <token>
```

---

## ❓ Troubleshooting

### Port 8000 Already in Use
```bash
python manage.py runserver 0.0.0.0:3000
```

### Module Not Found
```bash
pip install -r requirements/dev.txt
```

### Database Errors
```bash
python manage.py migrate
```

### Permission Denied (Linux/Mac)
```bash
chmod +x manage.py
```

---

## 📚 Documentation Links

- [Full README](README.md) - Complete documentation
- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [JWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)

---

**You're all set!** Start building amazing APIs! 🎉
