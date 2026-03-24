"""
Database Models for Accounts Application
Follows clean architecture with focused responsibility.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Profile(models.Model):
    """
    Extended user profile model.
    Stores additional user information beyond Django's default User model.
    """
    
    # Link Profile to User model (One-to-One relationship)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        help_text='Associated Django User account'
    )
    
    # Profile fields
    address = models.TextField(blank=True, null=True, help_text='User address')
    phone = models.CharField(max_length=20, blank=True, null=True, help_text='User phone number')
    bio = models.CharField(max_length=255, blank=True, null=True, help_text='User biography')
    age = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text='User age (must be >= 0)'
    )
    
    # Password reset system
    reset_otp = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        help_text='One-time password for account recovery'
    )
    otp_created_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when OTP was generated'
    )
    otp_attempts = models.IntegerField(
        default=0,
        help_text='Number of failed OTP attempts'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text='Profile creation timestamp')
    updated_at = models.DateTimeField(auto_now=True, help_text='Profile last update timestamp')
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of Profile."""
        return f'Profile of {self.user.username}'


class Note(models.Model):
    """
    User Notes Model.
    Allows users to create and manage personal notes.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        help_text='User who owns this note'
    )
    title = models.CharField(max_length=100, help_text='Note title')
    content = models.TextField(help_text='Note content')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Note creation timestamp')
    updated_at = models.DateTimeField(auto_now=True, help_text='Note last update timestamp')
    
    class Meta:
        verbose_name = 'User Note'
        verbose_name_plural = 'User Notes'
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of Note."""
        return self.title


class Task(models.Model):
    """
    User Tasks Model.
    Allows users to create and manage tasks with status tracking.
    """
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text='User who owns this task'
    )
    title = models.CharField(max_length=255, help_text='Task title')
    description = models.TextField(blank=True, null=True, help_text='Task description')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Current task status'
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text='Task creation timestamp')
    updated_at = models.DateTimeField(auto_now=True, help_text='Task last update timestamp')
    
    class Meta:
        verbose_name = 'User Task'
        verbose_name_plural = 'User Tasks'
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of Task."""
        return self.title
