"""
Database Admin Configuration for Accounts Application
Customizes Django admin interface for better usability.
"""

from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Note, Task


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for Profile model."""
    
    list_display = ('user', 'phone', 'age', 'created_at', 'updated_at')
    list_filter = ('age', 'created_at', 'otp_attempts')
    search_fields = ('user__username', 'user__email', 'phone', 'bio')
    readonly_fields = ('created_at', 'updated_at', 'otp_created_at')
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('address', 'phone', 'bio', 'age')
        }),
        ('OTP & Security', {
            'fields': ('reset_otp', 'otp_created_at', 'otp_attempts')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin interface for Note model."""
    
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Note Information', {
            'fields': ('user', 'title', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for Task model."""
    
    list_display = ('title', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Task Information', {
            'fields': ('user', 'title', 'description', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
