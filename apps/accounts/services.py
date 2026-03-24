"""
Service Layer for Accounts Application
Houses all business logic independent of views, serializers, or HTTP.
Promotes clean architecture and easy testing.
"""

import random
from datetime import timedelta
from typing import Optional, Dict, Tuple

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .models import Profile, Note, Task


class AuthenticationService:
    """
    Service class for authentication-related operations.
    Handles user login, token generation, and validation.
    """
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Authenticate user with username and password.
        
        Args:
            username (str): User's username
            password (str): User's password
            
        Returns:
            Tuple[Optional[User], Optional[str]]: User object and error message (if any)
        """
        from django.contrib.auth import authenticate
        
        # Validate input
        if not username or not password:
            return None, "Username and password are required"
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is None:
            return None, "Invalid username or password"
        
        return user, None
    
    @staticmethod
    def get_tokens_for_user(user: User) -> Dict[str, str]:
        """
        Generate JWT tokens for authenticated user.
        
        Args:
            user (User): User object
            
        Returns:
            Dict[str, str]: Dictionary with access and refresh tokens
        """
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Create a new user account.
        
        Args:
            username (str): User's username
            email (str): User's email address
            password (str): User's password
            
        Returns:
            Tuple[Optional[User], Optional[str]]: Created user object and error message (if any)
        """
        # Validate input
        if not all([username, email, password]):
            return None, "Username, email, and password are required"
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return None, "Username already exists"
        
        if User.objects.filter(email=email).exists():
            return None, "Email already registered"
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Create associated profile
            Profile.objects.create(user=user)
            return user, None
        except Exception as e:
            return None, str(e)


class ProfileService:
    """
    Service class for user profile-related operations.
    Handles profile updates, OTP generation, and validation.
    """
    
    @staticmethod
    def get_or_create_profile(user: User) -> Profile:
        """
        Get or create a profile for a user.
        
        Args:
            user (User): User object
            
        Returns:
            Profile: User's profile
        """
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile
    
    @staticmethod
    def update_profile(user: User, **kwargs) -> Tuple[Profile, Optional[str]]:
        """
        Update user profile information.
        
        Args:
            user (User): User object
            **kwargs: Fields to update (username, email, address, phone, bio, age)
            
        Returns:
            Tuple[Profile, Optional[str]]: Updated profile and error message (if any)
        """
        try:
            profile = ProfileService.get_or_create_profile(user)
            
            # Update User fields
            if 'username' in kwargs:
                if User.objects.filter(username=kwargs['username']).exclude(pk=user.pk).exists():
                    return None, "Username already taken"
                user.username = kwargs['username']
            
            if 'email' in kwargs:
                if User.objects.filter(email=kwargs['email']).exclude(pk=user.pk).exists():
                    return None, "Email already registered"
                user.email = kwargs['email']
            
            user.save()
            
            # Update Profile fields
            for field in ['address', 'phone', 'bio', 'age']:
                if field in kwargs:
                    setattr(profile, field, kwargs[field])
            
            profile.save()
            return profile, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def generate_otp() -> str:
        """
        Generate a 6-digit OTP for password reset.
        
        Returns:
            str: 6-digit OTP
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    @staticmethod
    def create_reset_otp(user: User) -> Tuple[str, Optional[str]]:
        """
        Create and store an OTP for password reset.
        
        Args:
            user (User): User object
            
        Returns:
            Tuple[str, Optional[str]]: Generated OTP and error message (if any)
        """
        try:
            profile = ProfileService.get_or_create_profile(user)
            otp = ProfileService.generate_otp()
            profile.reset_otp = otp
            profile.otp_created_at = timezone.now()
            profile.otp_attempts = 0
            profile.save()
            return otp, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def verify_otp(user: User, otp: str, max_attempts: int = 3, otp_validity_minutes: int = 10) -> Tuple[bool, Optional[str]]:
        """
        Verify OTP for password reset.
        
        Args:
            user (User): User object
            otp (str): OTP to verify
            max_attempts (int): Maximum number of attempts allowed
            otp_validity_minutes (int): OTP validity period in minutes
            
        Returns:
            Tuple[bool, Optional[str]]: Verification result and error message (if any)
        """
        try:
            profile = ProfileService.get_or_create_profile(user)
            
            # Check if OTP exists
            if not profile.reset_otp:
                return False, "No OTP generated for this user"
            
            # Check if OTP is expired
            if profile.otp_created_at:
                expiry_time = profile.otp_created_at + timedelta(minutes=otp_validity_minutes)
                if timezone.now() > expiry_time:
                    return False, "OTP has expired"
            
            # Check attempt limit
            if profile.otp_attempts >= max_attempts:
                return False, "Maximum OTP attempts exceeded"
            
            # Verify OTP
            if profile.reset_otp != otp:
                profile.otp_attempts += 1
                profile.save()
                return False, f"Invalid OTP. Attempts remaining: {max_attempts - profile.otp_attempts}"
            
            # Clear OTP on successful verification
            profile.reset_otp = None
            profile.otp_attempts = 0
            profile.save()
            return True, None
        except Exception as e:
            return False, str(e)


class TaskService:
    """
    Service class for task-related operations.
    Handles task creation, updates, and status management.
    """
    
    @staticmethod
    def create_task(user: User, title: str, description: str = '', status: str = 'pending') -> Tuple[Optional[Task], Optional[str]]:
        """
        Create a new task for a user.
        
        Args:
            user (User): User object
            title (str): Task title
            description (str): Task description
            status (str): Task status
            
        Returns:
            Tuple[Optional[Task], Optional[str]]: Created task and error message (if any)
        """
        try:
            task = Task.objects.create(
                user=user,
                title=title,
                description=description,
                status=status
            )
            return task, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def update_task(task: Task, **kwargs) -> Tuple[Optional[Task], Optional[str]]:
        """
        Update task information.
        
        Args:
            task (Task): Task object to update
            **kwargs: Fields to update (title, description, status)
            
        Returns:
            Tuple[Optional[Task], Optional[str]]: Updated task and error message (if any)
        """
        try:
            for field in ['title', 'description', 'status']:
                if field in kwargs:
                    setattr(task, field, kwargs[field])
            
            task.save()
            return task, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def delete_task(task: Task) -> Tuple[bool, Optional[str]]:
        """
        Delete a task.
        
        Args:
            task (Task): Task object to delete
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message (if any)
        """
        try:
            task.delete()
            return True, None
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_user_tasks(user: User, status: Optional[str] = None):
        """
        Get tasks for a user, optionally filtered by status.
        
        Args:
            user (User): User object
            status (Optional[str]): Filter by status if provided
            
        Returns:
            QuerySet: Filtered tasks
        """
        tasks = Task.objects.filter(user=user)
        if status:
            tasks = tasks.filter(status=status)
        return tasks


class NoteService:
    """
    Service class for note-related operations.
    Handles note creation, updates, and deletion.
    """
    
    @staticmethod
    def create_note(user: User, title: str, content: str) -> Tuple[Optional[Note], Optional[str]]:
        """
        Create a new note for a user.
        
        Args:
            user (User): User object
            title (str): Note title
            content (str): Note content
            
        Returns:
            Tuple[Optional[Note], Optional[str]]: Created note and error message (if any)
        """
        try:
            note = Note.objects.create(
                user=user,
                title=title,
                content=content
            )
            return note, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def update_note(note: Note, **kwargs) -> Tuple[Optional[Note], Optional[str]]:
        """
        Update note information.
        
        Args:
            note (Note): Note object to update
            **kwargs: Fields to update (title, content)
            
        Returns:
            Tuple[Optional[Note], Optional[str]]: Updated note and error message (if any)
        """
        try:
            for field in ['title', 'content']:
                if field in kwargs:
                    setattr(note, field, kwargs[field])
            
            note.save()
            return note, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def delete_note(note: Note) -> Tuple[bool, Optional[str]]:
        """
        Delete a note.
        
        Args:
            note (Note): Note object to delete
            
        Returns:
            Tuple[bool, Optional[str]]: Success status and error message (if any)
        """
        try:
            note.delete()
            return True, None
        except Exception as e:
            return False, str(e)
