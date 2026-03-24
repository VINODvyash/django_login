# 🚀 Django Architect - Quick Reference Cheat Sheet

## Project Setup Checklist

```bash
# ✅ Initialize project
django-admin startproject config
python manage.py startapp apps

# ✅ Configure settings
# - Split base.py, local.py, production.py
# - Setup environment variables (.env)
# - Configure logging

# ✅ Setup database
# - Define models with proper relationships
# - Create migrations
# - Add indexes strategically
# - Setup replication/sharding if needed

# ✅ API endpoints
# - Use DRF ViewSets
# - Implement serializers
# - Add pagination, filtering, search
# - Version APIs (/api/v1/)

# ✅ Authentication
# - JWT for stateless auth
# - Refresh token mechanism
# - Token blacklist for logout

# ✅ Caching
# - Redis for session/cache
# - Cache frequently accessed data
# - Implement cache invalidation

# ✅ Testing
# - Unit tests (70%)
# - Integration tests (20%)
# - E2E tests (10%)
# - >80% code coverage

# ✅ Deployment
# - Docker containerization
# - CI/CD pipeline (GitHub Actions)
# - Environment management
# - Monitoring & logging
```

---

## Architecture Pattern Quick Ref

```python
# ✅ Recommended: Service Layer Architecture
views.py       →  Serializers    →  Services      →  Models  →  Database
(HTTP)            (Validation)      (Business)       (ORM)
                                    (Reusable)

# ❌ Avoid: Fat Views
views.py (business logic + validation + database queries)
```

---

## Common Django Patterns

### Models Best Practices

```python
class BaseModel(models.Model):
    """Abstract base for all models"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class User(BaseModel):
    email = models.EmailField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email', 'created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email'
            ),
        ]
```

### QuerySet Optimization

```python
# ✅ Good: select_related (ForeignKey, OneToOne)
User.objects.select_related('profile').all()

# ✅ Good: prefetch_related (Reverse FK, M2M)
User.objects.prefetch_related('orders').all()

# ✅ Good: only() for large models
User.objects.only('id', 'email', 'name').all()

# ✅ Good: values() for specific columns
User.objects.values('id', 'email').all()

# ❌ Bad: N+1 queries
for user in User.objects.all():
    print(user.profile.bio)  # Extra query for each user!
```

### Service Layer Pattern

```python
# services.py - Business logic here
class OrderService:
    @staticmethod
    def create_order(user, items):
        # Validation
        if not items:
            raise ValueError("Items required")
        
        # Calculation
        total = sum(item['price'] * item['qty'] for item in items)
        
        # Database
        order = Order.objects.create(user=user, total=total)
        
        # Side effects (use signals or events)
        OrderCreatedEvent.emit(order)
        
        return order

# views.py - Just HTTP handling
@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    order = OrderService.create_order(
        request.user,
        serializer.validated_data['items']
    )
    return Response(OrderSerializer(order).data, status=201)
```

---

## API Design Patterns

### Versioning

```python
# URL-based (best for mobile)
path('api/v1/', include('apps.urls')),
path('api/v2/', include('apps.urls_v2')),

# Header-based
# Accept: application/json; version=1
```

### Response Format

```python
# Success (200, 201)
{
    "success": true,
    "status_code": 200,
    "message": "Success",
    "data": {...}
}

# Error (400, 401, 500)
{
    "success": false,
    "status_code": 400,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input",
        "details": {...}
    }
}
```

### Pagination

```python
# Cursor-based (for large datasets)
class CursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'

# Offset/limit (for smaller datasets)
class PageNumberPagination(PageNumberPagination):
    page_size = 20
```

### Filtering & Search

```python
class OrderViewSet(viewsets.ModelViewSet):
    filterset_class = OrderFilterSet
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['number', 'customer__name']
    ordering_fields = ['created_at', 'total']
```

---

## Security Checklist

```python
# ✅ settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True

# ✅ Authentication
- Use JWT with refresh tokens
- Implement token blacklist for logout
- Hash passwords (Django handles this)
- Rate limit login attempts

# ✅ Authorization
- Check permissions in every view
- Use object-level permissions
- Don't trust user input

# ✅ Data Protection
- Encrypt sensitive data at rest
- Use HTTPS for all traffic
- Validate all inputs
- Sanitize output
```

---

## Performance Checklist

```python
# ✅ Database
- Use select_related() and prefetch_related()
- Add indexes to frequently queried columns
- Use database-level pagination
- Monitor slow queries

# ✅ Caching
- Cache expensive queries (Redis)
- Cache API responses
- Implement cache invalidation
- Monitor cache hit rate

# ✅ Async Tasks
- Use Celery for long-running tasks
- Don't block request/response
- Implement retry logic
- Monitor task queue

# ✅ Frontend
- Use CDN for static files
- Enable gzip compression
- Minify CSS/JS
- Optimize images

# ✅ Monitoring
- Log errors to Sentry
- Monitor metrics (Prometheus)
- Set up alerting
- Track performance metrics
```

---

## Testing Quick Reference

```python
# Unit Test Template
class TestOrderService(TestCase):
    def setUp(self):
        self.user = UserFactory()
    
    def test_create_order_success(self):
        order = OrderService.create_order(self.user, items)
        self.assertEqual(order.user, self.user)
    
    def test_create_order_invalid(self):
        with self.assertRaises(ValueError):
            OrderService.create_order(self.user, [])

# Integration Test Template
class TestOrderAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.token = TokenFactory(user=self.user)
    
    def test_create_order_via_api(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post('/api/v1/orders/', {...})
        self.assertEqual(response.status_code, 201)

# Run tests
pytest                          # Run all tests
pytest tests/test_models.py    # Run specific file
pytest --cov=apps              # With coverage
pytest -k "test_order"         # By name
```

---

## Deployment Checklist

```bash
# ✅ Pre-deployment
- [ ] Run all tests (pytest)
- [ ] Check code quality (flake8, black, mypy)
- [ ] Security scan (bandit)
- [ ] Dependency audit (safety)
- [ ] Database migrations ready

# ✅ Deployment Steps
- [ ] Build Docker image
- [ ] Push to registry
- [ ] Run migrations (python manage.py migrate)
- [ ] Collect static files (python manage.py collectstatic)
- [ ] Start workers (celery, gunicorn)
- [ ] Health checks pass
- [ ] Smoke tests pass

# ✅ Post-deployment
- [ ] Monitor error tracking (Sentry)
- [ ] Check server logs
- [ ] Verify metrics
- [ ] Test critical flows
- [ ] Have rollback plan ready
```

---

## Common Django Commands

```bash
# Project & App
django-admin startproject config
python manage.py startapp users

# Database
python manage.py makemigrations           # Create migrations
python manage.py migrate                  # Apply migrations
python manage.py showmigrations          # Show migration status
python manage.py migrate users 0003      # Rollback to migration

# Development
python manage.py runserver 0.0.0.0:8000  # Run dev server
python manage.py shell                    # Python shell
python manage.py shell_plus               # IPython shell
python manage.py dbshell                 # Database shell

# Testing
pytest                                    # Run tests
pytest --cov=apps                        # With coverage

# Utilities
python manage.py createsuperuser          # Create admin user
python manage.py collectstatic            # Collect static files
python manage.py dumpdata > backup.json   # Backup data
python manage.py loaddata backup.json     # Restore data

# Admin
python manage.py changepassword username  # Change password
```

---

## Django ORM Queries

```python
# Create
user = User.objects.create(name='John', email='john@example.com')

# Read
user = User.objects.get(id=1)              # Single object
users = User.objects.all()                 # All objects
users = User.objects.filter(status='active')  # Filter

# Update
user.name = 'Jane'
user.save()

# Or bulk update
User.objects.filter(status='inactive').update(active=False)

# Delete
user.delete()
User.objects.filter(status='inactive').delete()

# Aggregation
from django.db.models import Count, Sum, Avg
User.objects.aggregate(total=Count('id'), avg_age=Avg('age'))

# Annotation
users = User.objects.annotate(order_count=Count('orders'))
```

---

## Signals Pattern

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Register in apps.py
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    
    def ready(self):
        import apps.users.signals  # noqa
```

---

## Middleware Pattern

```python
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Before view
        logger.info(f"Request: {request.method} {request.path}")
        
        response = self.get_response(request)
        
        # After view
        logger.info(f"Response: {response.status_code}")
        return response

# settings.py
MIDDLEWARE = [
    'apps.core.middleware.RequestLoggingMiddleware',
]
```

---

## Celery Task Pattern

```python
@shared_task(bind=True, max_retries=3)
def send_email_task(self, user_id, subject):
    try:
        user = User.objects.get(id=user_id)
        send_email(user.email, subject)
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
    except Exception as exc:
        # Retry after 60 seconds
        self.retry(exc=exc, countdown=60)

# Usage in view
send_email_task.delay(user.id, 'Welcome!')
```

---

## Environment Setup

```bash
# Create virtual environment
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements/dev.txt

# Setup environment
cp .env.example .env
# Edit .env with your values

# Initialize database
python manage.py migrate

# Create admin
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## Key Metrics to Track

```
Performance:
- API response time (p50, p95, p99)
- Error rate
- Cache hit rate
- Database query time

Business:
- Request count per endpoint
- User registration rate
- Feature usage
- Conversion rate

Infrastructure:
- CPU/Memory usage
- Disk space
- Database connections
- Queue size (Celery)
```

---

## Decision Matrix: When to Use What

| Problem | Solution | When |
|---------|----------|------|
| Long-running task | Celery | > 1 second |
| Expensive query | Redis cache | Frequently accessed |
| Large dataset | Pagination | > 1000 records |
| User isolation | select_related | FK relationship |
| Related data | prefetch_related | Reverse FK/M2M |
| Frequent login | Redis session | High traffic |
| Real-time updates | Websockets | Need < 1s latency |
| Large scale | Microservices | > 10 million users |
| Complex queries | Raw SQL | ORM too slow |
| API documentation | Swagger | Public API |

---

## Most Common Mistakes to Avoid

```python
# ❌ N+1 Queries
for order in Order.objects.all():
    print(order.customer.name)  # Query per order!

# ✅ Use select_related
for order in Order.objects.select_related('customer').all():
    print(order.customer.name)  # Single query

# ❌ Storing large files in database
file_content = models.TextField()

# ✅ Use FileField
file = models.FileField(upload_to='files/')

# ❌ No permission checks
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.save()

# ✅ Check permissions
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.user != request.user:
        raise PermissionDenied
    order.save()

# ❌ Synchronous email in view
send_email(user.email, 'Welcome!')  # Blocks request!

# ✅ Use Celery
send_email.delay(user.email, 'Welcome!')

# ❌ Storing secrets in code
SECRET_KEY = 'my-secret-key'

# ✅ Use environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
```

---

## Resources for Further Learning

📚 **Books**
- "Two Scoops of Django" - Best practices
- "High Performance Django" - Optimization
- "Designing Data-Intensive Apps" - Scalability

🎓 **Courses**
- Real Python (Advanced Django)
- Full Stack Python (Django tutorials)
- Architecture (System Design)

🔗 **Documentation**
- Django official docs
- Django REST Framework docs
- PostgreSQL docs

💬 **Communities**
- Django Forum
- Stack Overflow (django tag)
- r/django subreddit

---

## Quick Links

- Django Docs: https://docs.djangoproject.com
- DRF Docs: https://www.django-rest-framework.org
- PostgreSQL Docs: https://www.postgresql.org/docs
- Redis Docs: https://redis.io/documentation
- Celery Docs: https://docs.celeryproject.io

---

**Last Updated**: March 10, 2026
**Keep this handy for quick reference!** 🚀
