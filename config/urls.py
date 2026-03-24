"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# ═════════════════════════════════════════════════════════════════════════════
# API DOCUMENTATION PATHS
# ═════════════════════════════════════════════════════════════════════════════

api_docs_patterns = [
    # OpenAPI Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# ═════════════════════════════════════════════════════════════════════════════
# JWT AUTHENTICATION PATHS
# ═════════════════════════════════════════════════════════════════════════════

jwt_patterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# ═════════════════════════════════════════════════════════════════════════════
# APPLICATION PATHS
# ═════════════════════════════════════════════════════════════════════════════

app_patterns = [
    path('accounts/', include('apps.accounts.urls')),
]

# ═════════════════════════════════════════════════════════════════════════════
# MAIN URL PATTERNS
# ═════════════════════════════════════════════════════════════════════════════

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/v1/docs/', include(api_docs_patterns)),
    
    # JWT Authentication
    path('api/v1/auth/', include(jwt_patterns)),
    
    # Application APIs
    path('api/v1/', include(app_patterns)),
]

# ═════════════════════════════════════════════════════════════════════════════
# STATIC & MEDIA FILES (Development only)
# ═════════════════════════════════════════════════════════════════════════════

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Django Debug Toolbar (if installed)
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass

