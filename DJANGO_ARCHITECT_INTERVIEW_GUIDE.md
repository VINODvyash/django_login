# 🎯 Django Architect - Interview Preparation Guide

## 30-Second Elevator Pitch

"I'm a Django architect with expertise in designing scalable web applications using clean architecture principles. I specialize in building high-performance REST APIs with Django REST Framework, implementing secure authentication systems with JWT, and deploying microservices using Docker. I've led teams through architectural decisions including database sharding, caching strategies, and DevOps implementation. I'm passionate about writing testable, maintainable code following SOLID principles."

---

## Technical Depth Questions & Answers

### 1. What is Clean Architecture and why is it important?

**Answer Template:**
Clean Architecture separates your application into distinct layers:
- **Presentation Layer** (Views, Serializers) - HTTP handling
- **Business Logic Layer** (Services) - Core application logic
- **Data Access Layer** (Repositories, ORM) - Database interaction
- **Domain Layer** (Models) - Business entities

**Why it matters:**
- ✅ Testable - Business logic independent of framework
- ✅ Maintainable - Clear separation of concerns
- ✅ Scalable - Easy to add features
- ✅ Flexible - Can swap implementations

**Example from your project:**
```python
# Bad: Fat view with mixed concerns
def create_order(request):
    # Validation
    if not request.data.get('items'):
        return Response({'error': 'Items required'})
    
    # Database
    order = Order.objects.create(user=request.user)
    for item in request.data['items']:
        OrderItem.objects.create(order=order, ...)
    
    # Side effects
    send_email(request.user.email, 'Order created')
    
    return Response(OrderSerializer(order).data)

# Good: Clean architecture
class OrderService:
    @staticmethod
    def create_order(user, items):
        if not items: raise ValueError("Items required")
        order = Order.objects.create(user=user)
        for item in items:
            OrderItem.objects.create(order=order, ...)
        return order

def create_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order = OrderService.create_order(request.user, serializer.validated_data['items'])
    return Response(OrderSerializer(order).data, status=201)
```

---

### 2. How would you design a scalable Django API for 1 million users?

**Answer Framework:**

**Database Layer:**
- Use PostgreSQL with replication (primary + replicas)
- Implement read replicas for SELECT queries
- Shard data by user_id for horizontal scaling
- Create strategic indexes on frequently queried columns
- Use connection pooling (PgBouncer)

**Caching Layer:**
- Redis for session storage and caching
- Cache expensive queries: user profiles, settings, listings
- Implement cache-aside pattern
- TTL-based expiration + event-driven invalidation

**API Layer:**
- API versioning (/api/v1/, /api/v2/)
- Pagination with cursor-based pagination (for large datasets)
- Rate limiting: 100 req/min for anonymous, 1000 for authenticated
- Response compression with gzip
- CDN for static files

**Async Processing:**
- Celery for long-running tasks (email, reports, notifications)
- Background workers for data processing
- Message queue (RabbitMQ) for reliability

**Infrastructure:**
- Load balancing (Nginx, HAProxy)
- Multiple application instances (Gunicorn workers)
- Container orchestration (Kubernetes)
- Auto-scaling based on CPU/memory

**Example:**
```
Users → Load Balancer → [App Instance 1, 2, N]
                              ↓
                        Read Replicas (Postgres)
                        Write Primary (Postgres)
                        
        ↓
    Redis Cache
    (Session, Cache, Rate Limit)
    
        ↓
    Message Queue
    (Celery Tasks)
    
        ↓
    Workers (Process Tasks)
```

---

### 3. Design an authentication system that's secure and scalable.

**Answer:**

```python
# 1. JWT with Refresh Tokens (Stateless)
from rest_framework_simplejwt.tokens import RefreshToken

# 2. Token Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,  # Issue new refresh token
    'BLACKLIST_AFTER_ROTATION': True,  # Invalidate old token
}

# 3. Login Flow
class AuthenticationService:
    @staticmethod
    def authenticate(email, password):
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationError("Invalid credentials")
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserSerializer(user).data
        }

# 4. Request with token
headers = {'Authorization': 'Bearer <access_token>'}

# 5. Logout (Blacklist token)
token.blacklist()

# 6. Security measures
- HTTPS only (SECURE_SSL_REDIRECT = True)
- HttpOnly cookies (if using cookies)
- CORS restrictions
- Rate limiting on login endpoint
- Monitor suspicious patterns
- Log all authentication events
```

**Why JWT over sessions:**
- ✅ Stateless (no server-side session storage)
- ✅ Scales with multiple servers
- ✅ Works well with mobile/SPA
- ✅ Efficient for microservices (self-contained)
- ❌ Larger token size
- ❌ Can't revoke immediately (use blacklist)

---

### 4. Database Design: How would you design a social media schema?

**Answer:**

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE,
    username VARCHAR UNIQUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    INDEX idx_email,
    INDEX idx_created_at
);

-- Privacy: Store in separate table (data isolation)
CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY,
    bio TEXT,
    avatar_url VARCHAR,
    created_at TIMESTAMP
);

-- Posts (Denormalize counts for performance)
CREATE TABLE posts (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users,
    content TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    view_count INT DEFAULT 0,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    INDEX idx_user_id,
    INDEX idx_created_at
);

-- Comments (Nested structure)
CREATE TABLE comments (
    id UUID PRIMARY KEY,
    post_id UUID REFERENCES posts,
    user_id UUID REFERENCES users,
    parent_comment_id UUID (for replies),
    content TEXT,
    created_at TIMESTAMP,
    like_count INT DEFAULT 0
);

-- Likes
CREATE TABLE post_likes (
    post_id UUID,
    user_id UUID,
    created_at TIMESTAMP,
    PRIMARY KEY (post_id, user_id),
    INDEX idx_user_id  -- For: "User X liked Y posts"
);

-- Followers
CREATE TABLE follows (
    follower_id UUID,
    following_id UUID,
    created_at TIMESTAMP,
    PRIMARY KEY (follower_id, following_id),
    INDEX idx_follower_id,
    INDEX idx_following_id
);

-- Feed (Materialized view for performance)
CREATE TABLE feed_cache (
    user_id UUID,
    post_id UUID,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, post_id),
    INDEX idx_user_created  -- For pagination
);
```

**Optimization strategies:**
- ✅ Denormalize like/comment counts (update via triggers)
- ✅ Partition posts by date (daily tables)
- ✅ Shard by user_id for horizontal scaling
- ✅ Cache feed in Redis
- ✅ Archive old data (2+ years)
- ✅ Async update counts (Celery)

---

### 5. API Design: How do you handle pagination, filtering, and search?

**Answer:**

```python
# Pagination: Cursor-based (best for large datasets)
from rest_framework.pagination import CursorPagination

class PostPagination(CursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = '-created_at'  # Always order by sortable field

# Usage: /api/v1/posts/?cursor=cxczc...

# Filtering: Use FilterSet
from django_filters import FilterSet, CharFilter

class PostFilterSet(FilterSet):
    status = CharFilter(field_name='status', lookup_expr='exact')
    created_after = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    
    class Meta:
        model = Post
        fields = ['status', 'created_after']

# Usage: /api/v1/posts/?status=published&created_after=2024-01-01

# Search: Full-text search
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'user__username']
    ordering_fields = ['created_at', 'like_count']

# Usage: /api/v1/posts/?search=django&ordering=-like_count

# Best practices
class OptimizedPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('user').prefetch_related('comments')
    
    def get_queryset(self):
        # Filter by current user if needed
        if not self.request.user.is_authenticated:
            return Post.objects.none()
        
        # Apply filters from request
        queryset = super().get_queryset()
        
        # Performance: Only fetch needed fields
        if self.action == 'list':
            queryset = queryset.only('id', 'title', 'created_at')
        
        return queryset
```

**Q: Why cursor pagination over offset/limit?**

```
Offset/Limit: /posts?offset=100&limit=20
- Problem: If rows inserted, user might see duplicates
- Good for: Small datasets (<10k records)

Cursor: /posts?cursor=eJy...
- Advantage: Consistent even with data changes
- Good for: Large datasets, real-time feeds
- Implementation: Encode last row ID in cursor
```

---

### 6. Security: How would you prevent common attacks?

**Answer:**

```python
# 1. SQL Injection
# ❌ Bad: Direct string interpolation
users = User.objects.raw(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ Good: Django ORM (parameterized queries)
user = User.objects.get(id=user_id)

# 2. CSRF (Cross-Site Request Forgery)
# Django handles automatically with CSRF tokens
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# 3. XSS (Cross-Site Scripting)
# Serializers escape output
content = serializer.validated_data['content']  # Already escaped

# 4. Authentication attacks
# Rate limit login
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m')
def login(request):
    ...

# 5. Authorization: Check permissions
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsPostOwner]

# 6. Sensitive data exposure
# ✅ HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True

# ✅ Don't expose sensitive fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        # Exclude: password_hash, api_key, etc.

# 7. Injection in templates
# ✅ Always escape in templates (Django does this by default)
{{ user.bio }}  {# Automatically escaped #}

# 8. Dependency vulnerabilities
# Check monthly
pip-audit
safety check

# 9. Secrets management
# ❌ Never commit secrets
# ✅ Use environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

# 10. Logging sensitive data
# ❌ Bad: Log password
logger.info(f"User {user.email} logged in with password {password}")

# ✅ Good: Don't log passwords
logger.info(f"User {user.email} logged in successfully")
```

---

### 7. Performance: How would you optimize a slow query?

**Answer:**

```python
# Problem: Slow endpoint listing user's posts with comments
# GET /api/v1/users/123/posts/ - takes 10 seconds

# 1. Profile the queries
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    posts = Post.objects.filter(user_id=123)
    for post in posts:
        print(post.comments.count())  # N+1 query!

print(f"Total queries: {len(ctx)}")  # Likely 100+

# Solution:
# ✅ Add select_related/prefetch_related
posts = Post.objects.filter(user_id=123).prefetch_related('comments').select_related('user')

# ✅ Add indexes
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'created_at']),  # Composite index
        ]

# ✅ Pagination (not fetching all)
paginator = Paginator(posts, 20)  # Fetch only 20
page = paginator.page(1)

# ✅ Caching
@cache_page(60 * 5)  # Cache 5 minutes
def user_posts(request, user_id):
    posts = Post.objects.filter(user_id=user_id).values('id', 'title', 'created_at')
    return Response(posts)

# ✅ Denormalize (store comment_count on Post)
class Post(models.Model):
    comment_count = models.IntegerField(default=0)  # Update via Celery

# Performance improved: 10 seconds → 100ms (100x faster!)
```

---

### 8. Scalability: How would you scale a Django app to 10M users?

**Answer:**

**Phase 1: Single Server (0-100K users)**
```
1 Server:
- Django app
- PostgreSQL
- Redis
```

**Phase 2: Separate Layers (100K-1M users)**
```
Load Balancer
    ↓
[App1, App2, App3] (Horizontal scaling)
    ↓
PostgreSQL Primary + Replicas
    ↓
Redis Cluster
    ↓
Celery Workers
```

**Phase 3: Microservices (1M-10M users)**
```
API Gateway → Load Balancer → [Service 1, Service 2, ...]
                                ↓
                    [DB Shard 1, DB Shard 2, ...]
                    [Cache Cluster 1, 2, ...]
                    [Worker Pool 1, 2, ...]
```

**Specific strategies:**

1. **Database Sharding**
```python
# Shard by user_id
shard_number = user_id % NUM_SHARDS  # 0-9
connection = get_connection(f"db_shard_{shard_number}")
```

2. **Read Replicas**
```python
# Write to primary, read from replicas
Post.objects.using('primary').create(...)
Post.objects.using('replica').filter(...)
```

3. **Caching Strategy**
```python
# Cache by user
cache_key = f"user:{user_id}:profile"
cached = cache.get(cache_key)
if not cached:
    profile = User.objects.get(id=user_id)
    cache.set(cache_key, profile, 3600)
```

4. **Async Processing**
```python
# Don't block requests
send_email.delay(user.email)
generate_report.delay(user.id)
```

5. **CDN for static files**
```python
# Serve from cloudflare, AWS CloudFront
STATIC_URL = 'https://cdn.example.com/static/'
```

---

## System Design Questions

### Q: Design Instagram

**Architecture:**
```
Users → API Gateway → Auth Service → Post Service → Comment Service
                 ↓
        Feed Service (Caching heavy)
                 ↓
        Image Service (Upload, Resize, CDN)
                 ↓
        Notification Service (WebSockets)
                 ↓
        Analytics Service
```

**Database:**
```
Users (PostgreSQL)
Posts (PostgreSQL + Sharded by user_id)
Comments (PostgreSQL + Secondary index by post_id)
Likes (NoSQL - Redis for fast access)
Following (Cache in Redis)
Feed (Cache in Redis, regenerate every hour)
```

### Q: Design a real-time chat system

**Requirements:**
- Low latency (< 100ms)
- Scalable to millions of users
- Message persistence
- Offline message delivery

**Solution:**
```
WebSocket Server (Socket.io, Django Channels)
    ↓
Message Queue (RabbitMQ, Kafka)
    ↓
Message Service (Store to PostgreSQL)
    ↓
Redis Cache (Recent messages, user presence)
    ↓
Notification Service (Push, Email for offline)
```

---

## Behavioral Interview Questions

### Q: Tell me about a time you optimized a system. What was the result?

**STAR Format:**
- **Situation:** "I was working on a Django API handling 10K requests/min. The database was at 80% CPU."
- **Task:** "I needed to reduce database load without changing the API contract."
- **Action:** 
  - "I profiled queries and found N+1 queries in user profile endpoints"
  - "Added select_related to fetch user + profile in single query"
  - "Implemented Redis caching for frequently accessed profiles"
  - "Added database indexes on user_id and email fields"
  - "Implemented pagination to limit result sets"
- **Result:** "Database CPU dropped to 20%, API response time improved by 70%, saved ~$5K/month in infrastructure costs"

### Q: Describe a time you made a difficult architectural decision.

**STAR Format:**
- **Situation:** "Team was split on using microservices vs monolith for a social platform."
- **Task:** "Make decision that balances team scalability and technical debt."
- **Action:**
  - "I created a decision matrix with criteria: team size, deployment frequency, complexity"
  - "Presented two options with trade-offs"
  - "Led discussion with pros/cons"
  - "Documented decision with rationale for future reference (ADR)"
- **Result:** "Team consensus on monolith with separated services (modular monolith), faster iteration, reduced DevOps complexity"

### Q: How do you stay updated with Django/Python ecosystem?

**Answer:** "I actively follow best practices through:
- Django official blog posts and release notes
- Reading 'Two Scoops of Django' and relevant books
- Contributing to open-source Django projects
- Attending Django conferences (DjangoCon)
- Reviewing architecture decisions quarterly with team
- Experimenting with new tools in side projects"

---

## Questions to Ask Interviewer

1. **Technical:** "How is your Django application currently structured? What are the scaling challenges you're facing?"
2. **Team:** "What size is the engineering team? How are architectural decisions made?"
3. **Growth:** "Where do you see the product/technical complexity in 2 years?"
4. **Impact:** "What would success look like in this role after first 6months/1 year?"
5. **Culture:** "How does the team handle disagreements on technical decisions?"

---

## Study Schedule (8 weeks to mastery)

**Week 1-2: Foundations**
- Django ORM deep dive
- QuerySet optimization
- Database indexing strategies

**Week 3-4: Architecture**
- Clean architecture patterns
- Design patterns in Django
- SOLID principles

**Week 5-6: Scalability**
- Caching strategies
- Database sharding
- Load balancing

**Week 7: Security & Performance**
- OWASP Top 10
- Performance profiling
- Common vulnerabilities

**Week 8: Projects & Practice**
- Build portfolio project
- Solve system design problems
- Practice behavioral questions

---

## Resources for Interview Prep

**Books:**
- "Two Scoops of Django" (Best Practices)
- "Designing Data-Intensive Apps" (Scalability)
- "System Design Interview" (Architecture)

**Websites:**
- Django Official Documentation
- Real Python (Advanced tutorials)
- Hacker Rank (System Design problems)

**Practice:**
- LeetCode (Database design problems)
- Interview.io (Mock interviews)
- Prep with peers

---

## Red Flags to Avoid in Interviews

❌ Saying "I don't know" without follow-up
✅ "I'm not familiar with that, but here's my approach to learning it..."

❌ Overcomplicating solutions
✅ Start simple, discuss trade-offs, optimize if needed

❌ Not asking clarifying questions
✅ Ask about scale, constraints, requirements before designing

❌ Speaking negatively about past experiences
✅ Focus on lessons learned and improvements made

---

## Final Checklist Before Interview

- [ ] Review Django ORM common patterns
- [ ] Practice 2-3 system design problems
- [ ] Prepare 3-4 STAR stories about past projects
- [ ] Understand their tech stack (read tech blog/GitHub)
- [ ] Have 5-6 smart questions ready
- [ ] Get good sleep night before!
- [ ] Practice talking about code out loud

---

**Remember:** You've built a production-grade Django project. You understand clean architecture, authentication, caching, and API design. You're well-prepared! 🚀
