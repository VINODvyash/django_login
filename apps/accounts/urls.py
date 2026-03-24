"""
URL Configuration for Accounts Application
Defines API endpoints for the accounts app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    health_check,
    register_view,
    login_view,
    profile_view,
    admin_dashboard,
    TaskViewSet,
    NoteViewSet,
)

# Initialize router for viewsets
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'notes', NoteViewSet, basename='note')

# URL patterns
urlpatterns = [
    # Health Check
    path('health/', health_check, name='health'),
    
    # Authentication
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    
    # Profile
    path('profile/', profile_view, name='profile'),
    
    # Admin
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    
    # Include router URLs (tasks and notes)
    path('', include(router.urls)),
]
