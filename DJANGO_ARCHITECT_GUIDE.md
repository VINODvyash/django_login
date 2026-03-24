# 🏗️ Django Architect - Complete Knowledge Base

A comprehensive guide for Django architects in 2026, covering architecture patterns, best practices, and career development.

---

## 📑 Table of Contents

1. [Role Overview](#role-overview)
2. [Project Architecture](#project-architecture)
3. [Database Design](#database-design)
4. [API Design & REST](#api-design--rest)
5. [Security & Authentication](#security--authentication)
6. [Performance & Optimization](#performance--optimization)
7. [Scalability Patterns](#scalability-patterns)
8. [Testing Strategy](#testing-strategy)
9. [Deployment & DevOps](#deployment--devops)
10. [Monitoring & Observability](#monitoring--observability)
11. [Code Quality & Standards](#code-quality--standards)
12. [Team Leadership](#team-leadership)
13. [Tools & Technologies Stack](#tools--technologies-stack)

---

## 1️⃣ Role Overview

### Responsibilities
- **Design** scalable, maintainable Django applications
- **Lead** technical decisions and architecture reviews
- **Mentor** junior developers on best practices
- **Optimize** for performance, security, and maintainability
- **Plan** infrastructure and deployment strategies
- **Document** architectural decisions (ADRs)

### Key Skills
- ✅ 5+ years Django experience
- ✅ System design & scalability
- ✅ Database optimization
- ✅ DevOps & deployment
- ✅ Team leadership
- ✅ Technical communication

---

## 2️⃣ Project Architecture

### Clean Architecture Layers

```
┌─────────────────────────────────────────────────┐
│         Presentation Layer (Views)              │
│  - API Endpoints                                │
│  - Serializers                                  │
│  - Permission Classes                          │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│      Application/Business Logic Layer           │
│  - Services (Business Logic) ⭐                  │
│  - Use Cases                                    │
│  - Validators                                   │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│       Domain/Data Access Layer                  │
│  - Models (ORM)                                 │
│  - Repositories                                 │
│  - Querysets                                    │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│       Infrastructure Layer                      │
│  - Database                                     │
│  - Cache (Redis)                                │
│  - External APIs                                │
│  - File Storage                                 │
└─────────────────────────────────────────────────┘
```

### Recommended Project Structure

```
project/
├── apps/
│   ├── users/
│   │   ├── models.py                    # Domain models
│   │   ├── views.py                     # Thin HTTP layer
│   │   ├── serializers.py               # Validation & serialization
│   │   ├── services.py                  # Business logic ⭐
│   │   ├── repositories.py              # Data access abstraction
│   │   ├── permissions.py               # Access control
│   │   ├── signals.py                   # Event handlers
│   │   ├── tasks.py                     # Celery tasks
│   │   ├── urls.py                      # API routes
│   │   ├── tests/
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   ├── test_services.py
│   │   │   └── test_integration.py
│   │   └── migrations/
│   │
│   ├── orders/
│   ├── payments/
│   └── ...
│
├── config/                              # Project configuration
│   ├── settings/
│   │   ├── base.py                      # Shared settings
│   │   ├── local.py                     # Development
│   │   ├── production.py                # Production
│   │   ├── testing.py                   # Testing
│   │   └── staging.py                   # Staging
│   ├── urls.py                          # Main URL routing
│   ├── asgi.py                          # Async server app
│   ├── wsgi.py                          # WSGI server app
│   └── celery.py                        # Celery config
│
├── core/
│   ├── utils/                           # Shared utilities
│   ├── exceptions.py                    # Custom exceptions
│   ├── constants.py                     # Application constants
│   ├── decorators.py                    # Custom decorators
│   ├── managers.py                      # Custom QuerySet managers
│   └── middleware.py                    # Custom middleware
│
├── templates/
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   └── apps/                            # App-specific templates
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── vendor/
│
├── media/                               # User uploads
│
├── tests/
│   ├── conftest.py                      # Pytest configuration
│   ├── factories.py                     # Test data factories
│   ├── fixtures.py                      # Shared fixtures
│   └── mocks.py                         # Mock objects
│
├── scripts/
│   ├── manage_db.py                     # DB management
│   ├── seed_data.py                     # Data seeding
│   └── cleanup.py                       # Cleanup tasks
│
├── docs/
│   ├── architecture.md                  # Architecture decisions
│   ├── api.md                           # API documentation
│   ├── database.md                      # Database design
│   └── deployment.md                    # Deployment guide
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   ├── prod.txt
│   └── test.txt
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── .env.example
├── .gitignore
├── .dockerignore
├── pytest.ini
├── manage.py
├── README.md
└── LICENSE
```

### Key Architecture Principles

#### 1. **Separation of Concerns**
```python
# ❌ BAD - View is doing too much
@api_view(['POST'])
def create_order(request):
    # Validation
    if not request.data.get('items'):
        return Response({'error': 'Items required'})
    
    # Business logic
    total = sum(item['price'] * item['qty'] for item in request.data['items'])
    tax = total * 0.1
    
    # Database interaction
    order = Order.objects.create(user=request.user, total=total + tax)
    order.items.set(request.data['items'])
    
    # Email sending
    send_email(request.user.email, f"Order {order.id} created")
    
    return Response(OrderSerializer(order).data)

# ✅ GOOD - Separated concerns
class OrderService:
    @staticmethod
    def create_order(user, items):
        # Business logic
        total = sum(item['price'] * item['qty'] for item in items)
        tax = total * 0.1
        
        # Database interaction
        order = Order.objects.create(user=user, total=total + tax)
        order.items.set(items)
        
        # Event emission
        OrderCreatedEvent.emit(order)
        
        return order

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    order = OrderService.create_order(request.user, serializer.validated_data['items'])
    return Response(OrderSerializer(order).data, status=201)
```

#### 2. **DRY (Don't Repeat Yourself)**
```python
# ❌ BAD - Repeated validation
@api_view(['POST'])
def create_user(request):
    if not request.data.get('email'):
        return Response({'error': 'Email required'})
    if User.objects.filter(email=request.data['email']).exists():
        return Response({'error': 'Email exists'})
    # ... more code

@api_view(['POST'])
def create_admin(request):
    if not request.data.get('email'):
        return Response({'error': 'Email required'})
    if User.objects.filter(email=request.data['email']).exists():
        return Response({'error': 'Email exists'})
    # ... more code

# ✅ GOOD - Centralized validation
class BaseUserSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class UserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ['email', 'name']

class AdminSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'permissions']
```

#### 3. **SOLID Principles**
- **S** - Single Responsibility: Each class has one reason to change
- **O** - Open/Closed: Open for extension, closed for modification
- **L** - Liskov Substitution: Derived classes can replace base classes
- **I** - Interface Segregation: Depend on specific interfaces
- **D** - Dependency Inversion: Depend on abstractions, not concrete implementations

---

## 3️⃣ Database Design

### Normalization Levels

#### 1NF - First Normal Form
- Eliminate repeating groups
- Each column contains atomic values

```python
# ❌ BAD - Violates 1NF
class Order(models.Model):
    items = models.TextField()  # Stores "item1,item2,item3"

# ✅ GOOD - Proper 1NF
class Order(models.Model):
    pass

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
```

#### 2NF - Second Normal Form
- Meet 1NF + Remove partial dependencies
- All non-key attributes depend on entire primary key

#### 3NF - Third Normal Form
- Meet 2NF + Remove transitive dependencies
- No non-key attribute depends on another non-key attribute

### Indexing Strategy

```python
class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Composite index for common queries
        indexes = [
            models.Index(fields=['category', 'created_at']),
            models.Index(fields=['category', '-created_at']),
        ]
        # Avoid indexing low-cardinality columns (boolean, status with few values)
```

### Query Optimization

```python
# ❌ BAD - N+1 query problem
def get_orders():
    orders = Order.objects.all()
    for order in orders:
        print(order.customer.name)  # Query for each order!
    # Result: 1 + N queries

# ✅ GOOD - Use select_related for ForeignKey
def get_orders():
    orders = Order.objects.select_related('customer').all()
    for order in orders:
        print(order.customer.name)  # No additional query
    # Result: 1 query

# ✅ GOOD - Use prefetch_related for reverse ForeignKey/M2M
def get_customers_with_orders():
    customers = Customer.objects.prefetch_related('orders').all()
    for customer in customers:
        for order in customer.orders.all():  # No additional query
            print(order.id)
    # Result: 2 queries (1 customers + 1 orders)

# ✅ GOOD - Use only() and defer() for large models
def get_orders_summary():
    orders = Order.objects.only('id', 'total', 'customer_id')
    # Excludes large fields like 'notes', 'description'
    
def get_orders_details():
    orders = Order.objects.defer('large_text_field')
    # Loads everything except specified fields
```

### Denormalization Strategy

```python
# Consider denormalization for heavy read operations
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # Denormalized field (updated via signal)
    item_count = models.IntegerField(default=0)
    customer_name = models.CharField(max_length=255)  # Cache for reporting
    
    class Meta:
        indexes = [
            models.Index(fields=['customer_name']),  # Fast customer search
        ]
```

---

## 4️⃣ API Design & REST

### RESTful Principles

```
HTTP Methods      CRUD      Example
─────────────────────────────────────────────
GET               Read      GET /api/v1/orders/123/
POST              Create    POST /api/v1/orders/
PUT/PATCH         Update    PATCH /api/v1/orders/123/
DELETE            Delete    DELETE /api/v1/orders/123/
```

### Versioning Strategy

```python
# URL-based versioning (Recommended)
urlpatterns = [
    path('api/v1/', include('apps.users.urls')),
    path('api/v2/', include('apps.users.urls_v2')),
]

# Header-based versioning
# Accept: application/json; version=1.0

# Accept versioning
# Accept: application/vnd.company.v1+json
```

### Response Format

```python
# ✅ Standardized response format
{
    "success": true,
    "status_code": 200,
    "message": "Order retrieved successfully",
    "data": {
        "id": 123,
        "total": 99.99,
        "items": []
    },
    "meta": {
        "timestamp": "2026-03-10T22:00:00Z",
        "request_id": "req-abc123",
        "version": "1.0"
    }
}

# ✅ Error response format
{
    "success": false,
    "status_code": 400,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid email format",
        "details": {
            "email": ["Enter a valid email address"]
        }
    },
    "meta": {
        "timestamp": "2026-03-10T22:00:00Z",
        "request_id": "req-abc123"
    }
}
```

### Pagination

```python
# Cursor-based pagination (recommended for large datasets)
class OrderPagination(CursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = '-created_at'  # Must be specified

# Offset/limit pagination (for smaller datasets)
class OrderPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

### Filtering & Searching

```python
from django_filters import FilterSet, CharFilter, DateTimeFromToRangeFilter
from rest_framework import filters

class OrderFilterSet(FilterSet):
    date_range = DateTimeFromToRangeFilter(field_name='created_at')
    
    class Meta:
        model = Order
        fields = ['customer', 'status', 'payment_method']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilterSet
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['customer__name', 'order_number']
    ordering_fields = ['created_at', 'total']
    ordering = ['-created_at']
```

### Rate Limiting

```python
from rest_framework.throttling import SimpleRateThrottle

class OrderThrottle(SimpleRateThrottle):
    scope = 'order'
    
class OrderViewSet(viewsets.ModelViewSet):
    throttle_classes = [OrderThrottle]

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'order': '50/hour',
    }
}
```

---

## 5️⃣ Security & Authentication

### Authentication Methods

#### JWT (JSON Web Tokens)
```python
# settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
```

#### OAuth 2.0
```python
# Third-party authentication
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_social_oauth2',  # Social auth
]

AUTHENTICATION_BACKENDS = [
    'rest_framework_social_oauth2.backends.DjangoOAuth2Backend',
]
```

### Authorization & Permissions

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in ['GET', 'HEAD', 'OPTIONS'] or 
                   request.user and request.user.is_staff)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
```

### Security Best Practices

```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "cdn.example.com"),
}

# CORS configuration
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
]
CORS_ALLOW_CREDENTIALS = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Input Validation & Sanitization

```python
from django.core.validators import validate_email, MinLengthValidator
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    customer_email = serializers.EmailField(
        validators=[validate_email]
    )
    
    def validate_customer_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, data):
        # Cross-field validation
        if data['total'] < 0:
            raise serializers.ValidationError("Total cannot be negative")
        return data
```

---

## 6️⃣ Performance & Optimization

### Caching Strategy

```python
from django.core.cache import cache

# Cache levels:
# 1. Browser cache (HTTP headers)
# 2. CDN cache
# 3. Application cache (Redis, Memcached)
# 4. Database query cache

# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Implementation
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def get_popular_orders(request):
    return Response(OrderSerializer(Order.objects.all()[:10], many=True).data)

# Manual caching
class ProductService:
    CACHE_KEY = 'products:list'
    CACHE_TIMEOUT = 60 * 10  # 10 minutes
    
    @classmethod
    def get_all_products(cls):
        products = cache.get(cls.CACHE_KEY)
        if products is None:
            products = list(Product.objects.all())
            cache.set(cls.CACHE_KEY, products, cls.CACHE_TIMEOUT)
        return products
    
    @classmethod
    def invalidate_cache(cls):
        cache.delete(cls.CACHE_KEY)
```

### Database Connection Pooling

```python
# Using django-db-pool
DATABASES = {
    'default': {
        'ENGINE': 'dj_database_url.config',
        'CONN_MAX_AGE': 600,  # Connection pooling
        'OPTIONS': {
            'pool': {
                'min': 5,
                'max': 20,
            }
        }
    }
}
```

### Async Tasks with Celery

```python
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_order_confirmation(self, order_id):
    try:
        order = Order.objects.get(id=order_id)
        # Send email
        order.customer.send_email(f"Order {order_id} confirmed")
        return f"Confirmation sent for order {order_id}"
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found")
        return None
    except Exception as exc:
        logger.error(f"Error sending confirmation: {exc}")
        raise self.retry(exc=exc, countdown=60)

# View integration
@api_view(['POST'])
def create_order(request):
    order = OrderService.create_order(request.user, request.data)
    # Async task
    send_order_confirmation.delay(order.id)
    return Response(OrderSerializer(order).data, status=201)
```

### Query Profiling

```python
from django.db import connection
from django.test.utils import override_settings
import logging

logger = logging.getLogger(__name__)

@override_settings(DEBUG=True)
def profile_queries():
    from django.db import reset_queries
    reset_queries()
    
    # Your code here
    products = Product.objects.prefetch_related('categories').all()
    
    # Log queries
    for query in connection.queries:
        logger.info(f"Query: {query['sql']}")
        logger.info(f"Time: {query['time']}")
```

---

## 7️⃣ Scalability Patterns

### Horizontal Scaling

```
┌─────────────────────────────────────────────┐
│           Load Balancer (Nginx)             │
│         (Round-robin, Least conn)           │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼────┐    ┌──────▼────┐
│ Django    │    │ Django    │
│ Instance1 │    │ Instance2 │
└──────┬────┘    └──────┬────┘
       │                │
       └────────┬───────┘
              ┌─▼──────────┐
              │  Shared    │
              │  Cache     │
              │  (Redis)   │
              └────────────┘
              
              ┌────────────┐
              │  Database  │
              │ (Primary + │
              │  Replicas) │
              └────────────┘
```

### Database Replication

```python
# settings.py
DATABASES = {
    'default': {  # Write database
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb_primary',
        'HOST': 'primary.db.aws.com',
    },
    'replica': {  # Read-only replica
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb_replica',
        'HOST': 'replica.db.aws.com',
    }
}

class OrderRouter:
    def db_for_read(self, model, **hints):
        if model.__name__ == 'Order':
            return 'replica'
        return 'default'
    
    def db_for_write(self, model, **hints):
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'

DATABASE_ROUTERS = ['apps.orders.routers.OrderRouter']
```

### Sharding Strategy

```python
# For very large datasets, implement sharding
class ShardedOrderService:
    SHARD_COUNT = 10
    
    @staticmethod
    def get_shard(order_id):
        return order_id % ShardedOrderService.SHARD_COUNT
    
    @staticmethod
    def get_database(order_id):
        shard = ShardedOrderService.get_shard(order_id)
        return f'shard_{shard}'
    
    @classmethod
    def get_order(cls, order_id):
        db = cls.get_database(order_id)
        return Order.objects.using(db).get(id=order_id)
```

---

## 8️⃣ Testing Strategy

### Test Pyramid

```
        ▲
       /│\
      / │ \
     /  │  \           E2E Tests (10%)
    /   │   \          - Full workflow
   /    │    \         - Slow, expensive
  ╱─────┼─────╲
 /      │      \       Integration Tests (20%)
/       │       \      - Multiple components
────────┼────────      - Medium speed
│       │       │
│       │       │      Unit Tests (70%)
│       │       │      - Single function
│       │       │      - Fast, isolated
└───────┼───────┘
```

### Unit Testing

```python
import pytest
from django.test import TestCase
from apps.orders.services import OrderService
from apps.orders.models import Order

class TestOrderService(TestCase):
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='test')
    
    def test_create_order_success(self, user):
        items = [{'id': 1, 'qty': 2, 'price': 10.00}]
        order = OrderService.create_order(user, items)
        
        assert order.user == user
        assert order.total == 20.00
    
    def test_create_order_invalid_items(self, user):
        with pytest.raises(ValueError):
            OrderService.create_order(user, [])
    
    @pytest.mark.parametrize('qty,price,expected', [
        (1, 10.00, 10.00),
        (2, 10.00, 20.00),
        (0, 10.00, 0.00),
    ])
    def test_order_calculation(self, user, qty, price, expected):
        items = [{'id': 1, 'qty': qty, 'price': price}]
        order = OrderService.create_order(user, items)
        assert order.total == expected
```

### Integration Testing

```python
class TestOrderAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.token = get_token(self.user)
    
    def test_create_order_integration(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        response = self.client.post('/api/v1/orders/', {
            'items': [{'product_id': 1, 'qty': 2}]
        })
        
        assert response.status_code == 201
        assert Order.objects.filter(user=self.user).exists()
    
    def test_order_workflow(self):
        # Create
        create_response = self.client.post('/api/v1/orders/', {...})
        order_id = create_response.data['id']
        
        # Retrieve
        get_response = self.client.get(f'/api/v1/orders/{order_id}/')
        assert get_response.status_code == 200
        
        # Update
        patch_response = self.client.patch(f'/api/v1/orders/{order_id}/', {
            'status': 'SHIPPED'
        })
        assert patch_response.status_code == 200
        
        # Delete
        delete_response = self.client.delete(f'/api/v1/orders/{order_id}/')
        assert delete_response.status_code == 204
```

### Test Factories

```python
import factory
from factory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Faker('email')
    is_active = True

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order
    
    user = factory.SubFactory(UserFactory)
    total = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    status = 'PENDING'

# Usage
user = UserFactory()
order = OrderFactory(user=user)
```

### Fixtures & Mocks

```python
from unittest.mock import patch, MagicMock
import pytest

@pytest.fixture
def mock_email_service(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('apps.orders.services.send_email', mock)
    return mock

def test_order_sends_email(mock_email_service):
    order = OrderService.create_order(user, items)
    mock_email_service.assert_called_once()
```

---

## 9️⃣ Deployment & DevOps

### Docker Setup

```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements/prod.txt .
RUN pip install --no-cache-dir -r prod.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

RUN python manage.py collectstatic --noinput
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

### Docker Compose Orchestration

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    
  celery:
    build: .
    command: celery -A config worker -l info
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Django CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          pip install -r requirements/test.txt
      
      - name: Run tests
        run: |
          pytest --cov=apps tests/
      
      - name: Lint
        run: |
          flake8 apps/
          black --check apps/
      
      - name: Type checking
        run: |
          mypy apps/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Deploy commands here
          echo "Deploying to production..."
```

### Environment Management

```bash
# .env.example
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com

DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0

AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

---

## 🔟 Monitoring & Observability

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024 * 1024 * 15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Usage
logger.info(f"Order {order_id} created")
logger.error(f"Payment failed: {error}")
logger.warning("Low stock for product {product_id}")
```

### Error Tracking (Sentry)

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/12345",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

### Metrics & Monitoring

```python
from prometheus_client import Counter, Histogram, generate_latest
import time

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@api_view(['GET'])
def orders_list(request):
    request_count.labels(method='GET', endpoint='/orders').inc()
    
    start_time = time.time()
    orders = Order.objects.all()
    duration = time.time() - start_time
    
    request_duration.labels(endpoint='/orders').observe(duration)
    
    return Response(OrderSerializer(orders, many=True).data)
```

### Health Checks

```python
from django.core.management.base import BaseCommand
from django.db import connection
from django.core.cache import cache

@api_view(['GET'])
def health_check(request):
    status = {
        'status': 'healthy',
        'database': check_database(),
        'cache': check_cache(),
        'disk_space': check_disk_space(),
    }
    
    if all(status.values()):
        return Response(status, status=200)
    else:
        return Response(status, status=503)

def check_database():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except:
        return False

def check_cache():
    try:
        cache.set('health_check', 'ok', 10)
        return cache.get('health_check') == 'ok'
    except:
        return False
```

---

## 1️⃣1️⃣ Code Quality & Standards

### Code Style (PEP 8)

```python
# Use Black for code formatting
def create_order(user: User, items: List[OrderItem]) -> Order:
    """
    Create a new order.
    
    Args:
        user: The user creating the order
        items: List of items to include
        
    Returns:
        The created Order instance
        
    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Order must contain at least one item")
    
    # Implementation...
```

### Type Hints

```python
from typing import Optional, List, Dict, Tuple, Union

def get_user_orders(
    user: User,
    status: Optional[str] = None,
    limit: int = 10
) -> List[Order]:
    """Get orders for a user."""
    orders = Order.objects.filter(user=user)
    if status:
        orders = orders.filter(status=status)
    return list(orders[:limit])

def process_payment(
    order: Order,
    amount: float
) -> Tuple[bool, Optional[str]]:
    """Process payment and return success status and optional error message."""
    try:
        # Process payment
        return True, None
    except PaymentError as e:
        return False, str(e)
```

### Documentation Standards

```python
class Order(models.Model):
    """
    Order model representing a customer order.
    
    Attributes:
        user: Foreign key to User
        total: Total order amount
        status: Current order status (PENDING, SHIPPED, DELIVERED)
        created_at: Order creation timestamp
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Code Review Checklist

- [ ] Follows PEP 8 and project standards
- [ ] Has proper type hints
- [ ] Includes unit tests (>80% coverage)
- [ ] Handles errors gracefully
- [ ] No hardcoded values
- [ ] Uses Django best practices
- [ ] Optimized database queries
- [ ] Security considerations addressed
- [ ] Documentation updated
- [ ] No deprecated dependencies

---

## 1️⃣2️⃣ Team Leadership

### Architecture Decision Records (ADR)

```markdown
# ADR-001: Use JWT for API Authentication

## Context
We need to secure our REST API endpoints and support mobile applications.

## Decision
We will use JWT (JSON Web Tokens) for authentication.

## Rationale
- Stateless authentication (scalable)
- Works well with mobile apps
- Industry standard
- Good library support in Django

## Consequences
- Need to implement token refresh mechanism
- Tokens can't be revoked immediately (use blacklist)
- Need secure token storage on client side
```

### Code Review Best Practices

```
1. Review for correctness
   - Does it solve the problem?
   - Are there any bugs?
   - Are edge cases handled?

2. Review for design
   - Does it follow architecture patterns?
   - Is it maintainable?
   - Could it be simpler?

3. Review for performance
   - Are there N+1 queries?
   - Is caching used appropriately?
   - Are database indexes optimized?

4. Review for security
   - Is user input validated?
   - Are permissions checked?
   - Are secrets stored properly?

5. Review for testing
   - Is there adequate test coverage?
   - Are edge cases tested?
```

### Technical Debt Management

```
1. Track technical debt
   - Create issues/tickets
   - Label as "technical-debt"
   - Estimate effort

2. Balance new features with debt
   - 20% of sprint for technical debt
   - Regular refactoring cycles

3. Prevent accumulation
   - Code review standards
   - Automated testing
   - Architecture guidelines
```

---

## 1️⃣3️⃣ Tools & Technologies Stack

### Essential Tools

```
Frontend              Backend              DevOps
─────────────────────────────────────────────────
React/Vue.js         Django 4.2+         Docker
TypeScript           Django REST         Kubernetes
Axios                PostgreSQL          Terraform
                     Redis               GitHub Actions
                     Celery              Datadog
                     
Testing              Code Quality        Documentation
─────────────────────────────────────────────────
Pytest               Black               Swagger/OpenAPI
pytest-django        Flake8              Sphinx
Cypress              Pylint              MkDocs
                     MyType              
```

### Development Environment

```bash
# Tools setup
pip install -r requirements/dev.txt

# Pre-commit hooks
pip install pre-commit
pre-commit install

# Run linters before commit
black apps/
isort apps/
flake8 apps/
mypy apps/

# Run tests
pytest --cov=apps/
```

### Recommended Extensions (VS Code)

```json
{
  "extensions": [
    "ms-python.python",              // Python support
    "ms-python.vscode-pylance",      // Type checking
    "batisteo.vscode-django",        // Django support
    "eamodio.gitlens",               // Git integration
    "ms-azuretools.vscode-docker",   // Docker support
    "ms-vscode-remote.remote-containers",  // Dev containers
    "GitHub.copilot",                // AI assistance
    "ms-python.black-formatter",     // Code formatting
    "ms-python.pylint",              // Linting
    "sonarsource.sonarlint-vscode"   // Code quality
  ]
}
```

---

## 📊 Django Architect Competencies Matrix

```
Competency                Level 1        Level 2           Level 3           Level 4
──────────────────────────────────────────────────────────────────────────────────
Django Core               Understanding  Implementation    Optimization      Innovation
Database Design           Basic SQL      Normalization     Sharding/Scale    Data warehousing
API Design                REST basics    Versioning        Rate limiting     GraphQL
Security                  HTTPS basic    JWT/OAuth2        Key mgmt          Zero trust
Performance               Caching basic  Query opt         Profiling         Tuning
Testing                   Unit tests     Integration       E2E               Mutation testing
DevOps/Deployment         Docker basic   CI/CD            IaC/K8s           Multi-region
Scalability               Single server  Replication       Sharding          Microservices
Team Leadership           Code review    Architecture      Mentoring         Strategic planning
```

---

## 🎯 Career Path: Django Architect

### Year 1-2: Foundation
- ✅ Master Django ORM and models
- ✅ Write RESTful APIs
- ✅ Understand authentication/authorization
- ✅ Learn database basics
- ✅ Setup basic testing

### Year 3-4: Mid-Level
- ✅ Optimize database queries
- ✅ Implement caching strategies
- ✅ Design scalable APIs
- ✅ Master testing frameworks
- ✅ Learn DevOps basics (Docker)

### Year 5-6: Senior
- ✅ System design & architecture
- ✅ Database sharding & replication
- ✅ Microservices patterns
- ✅ Team leadership
- ✅ Production deployment

### Year 7+: Architect
- ✅ Enterprise architecture
- ✅ Strategic technology decisions
- ✅ Cross-team collaboration
- ✅ Innovation & R&D
- ✅ Mentoring & knowledge sharing

---

## 📚 Recommended Learning Resources

### Books
- "Two Scoops of Django" by Daniel and Audrey Roy Greenfeld
- "High Performance Django" by Peter Baumgartner
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "The Pragmatic Programmer"

### Online Courses
- Django for Beginners (WilliamVincent)
- Advanced Django (Real Python)
- System Design (ExamPro)

### Communities
- Django Communities (forums)
- DjangoCon talks
- GitHub open-source projects
- Stack Overflow

---

## 🏆 Conclusion

A successful Django Architect combines:
- 🧠 **Technical Excellence** - Deep Django knowledge
- 🏗️ **Architectural Thinking** - System design at scale
- 👥 **Leadership** - Team mentorship & communication
- 📈 **Business Acumen** - Align tech with business goals
- 🔐 **Security Mindset** - Build secure systems
- ⚡ **Performance Focus** - Optimize for speed & efficiency

**Remember**: "The right architecture is the one that enables teams to deliver value continuously while maintaining quality." - Unknown

---

**Last Updated**: March 10, 2026
**Version**: 1.0
**Audience**: Django Architects & Senior Developers
