"""
Custom Permissions for Accounts Application
Defines permission classes for access control.
"""

from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group


class IsAdminUserCustom(BasePermission):
    """
    Custom permission to check if user is an admin.
    """
    
    message = 'Admin access required.'
    
    def has_permission(self, request, view):
        """Check if user is a superuser or member of admin group."""
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.is_superuser or request.user.is_staff


class IsProfileOwner(BasePermission):
    """
    Permission to check if user owns the profile.
    """
    
    message = 'You can only access your own profile.'
    
    def has_object_permission(self, request, view, obj):
        """Check if the user owns the profile."""
        return obj.user == request.user


class IsTaskOwner(BasePermission):
    """
    Permission to check if user owns the task.
    """
    
    message = 'You can only access your own tasks.'
    
    def has_object_permission(self, request, view, obj):
        """Check if the user owns the task."""
        return obj.user == request.user


class IsNoteOwner(BasePermission):
    """
    Permission to check if user owns the note.
    """
    
    message = 'You can only access your own notes.'
    
    def has_object_permission(self, request, view, obj):
        """Check if the user owns the note."""
        return obj.user == request.user
