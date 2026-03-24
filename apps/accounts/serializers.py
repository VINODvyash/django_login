"""
Serializers for Accounts Application
Handles validation and conversion of model instances to JSON and vice versa.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Profile, Task, Note


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's User model.
    Provides read-only access to user information.
    """
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles validation and creation of new user accounts.
    """
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
    
    def validate_email(self, value):
        """Validate email address."""
        # Validate email format
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        # Check if email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        
        return value
    
    def validate_username(self, value):
        """Validate username."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        
        return value
    
    def validate(self, data):
        """Validate password confirmation."""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        
        return data
    
    def create(self, validated_data):
        """Create a new user and associated profile."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    Includes user information and profile-specific fields.
    """
    
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    
    class Meta:
        model = Profile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'address', 'phone', 'bio', 'age', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_email(self, value):
        """Validate email address."""
        # Validate email format
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        
        # Check if email already exists (excluding current user)
        if User.objects.filter(email=value).exclude(
            pk=self.instance.user.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError("Email already registered.")
        
        return value
    
    def update(self, instance, validated_data):
        """Update profile and associated user."""
        user_data = validated_data.pop('user', {})
        
        # Update User fields
        user = instance.user
        user.email = user_data.get('email', user.email)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()
        
        # Update Profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for profile updates.
    Focuses on commonly updated fields.
    """
    
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = Profile
        fields = ('username', 'email', 'address', 'phone', 'bio', 'age')
    
    def update(self, instance, validated_data):
        """Update profile with validated data."""
        user = instance.user
        
        # Update User fields
        if 'username' in validated_data:
            user.username = validated_data.pop('username')
        if 'email' in validated_data:
            user.email = validated_data.pop('email')
        user.save()
        
        # Update Profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for user tasks.
    Provides CRUD operations for task management.
    """
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_status(self, value):
        """Validate task status."""
        valid_statuses = ['pending', 'in_progress', 'completed']
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}"
            )
        return value


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for user notes.
    Provides CRUD operations for note management.
    """
    
    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_title(self, value):
        """Validate note title."""
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Title cannot be empty.")
        return value
    
    def validate_content(self, value):
        """Validate note content."""
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Content cannot be empty.")
        return value
