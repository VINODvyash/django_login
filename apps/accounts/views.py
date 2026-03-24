"""
Views for Accounts Application
RESTful API endpoints for authentication, profile, tasks, and notes.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .models import Profile, Task, Note
from .serializers import (
    RegisterSerializer, UserSerializer, ProfileSerializer,
    UpdateProfileSerializer, TaskSerializer, NoteSerializer
)
from .services import (
    AuthenticationService, ProfileService, TaskService, NoteService
)
from .permissions import IsAdminUserCustom


# ═════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═════════════════════════════════════════════════════════════════════════════

@api_view(['GET'])
def health_check(request):
    """Health check endpoint to verify API status."""
    return Response({
        'status': 'OK',
        'message': 'API is running smoothly'
    }, status=status.HTTP_200_OK)


# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION VIEWS
# ═════════════════════════════════════════════════════════════════════════════

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user.
    
    Expected JSON:
    {
        "username": "string",
        "email": "email@example.com",
        "password": "string",
        "password_confirm": "string"
    }
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = AuthenticationService.get_tokens_for_user(user)
        
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data,
            **tokens
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authenticate user and return JWT tokens.
    
    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user, error = AuthenticationService.authenticate_user(username, password)
    
    if error:
        return Response(
            {'error': error},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    tokens = AuthenticationService.get_tokens_for_user(user)
    
    return Response({
        'message': 'Login successful',
        'user': UserSerializer(user).data,
        **tokens
    }, status=status.HTTP_200_OK)


# ═════════════════════════════════════════════════════════════════════════════
# PROFILE VIEWS
# ═════════════════════════════════════════════════════════════════════════════

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Get or update user profile.
    
    GET: Returns current user's profile
    PUT: Updates user's profile
    """
    profile = ProfileService.get_or_create_profile(request.user)
    
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'data': ProfileSerializer(profile).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ═════════════════════════════════════════════════════════════════════════════
# TASK VIEWS
# ═════════════════════════════════════════════════════════════════════════════

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user tasks.
    Provides full CRUD operations for tasks.
    """
    
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get tasks for current user only."""
        user = self.request.user
        if user and user.is_authenticated:
            return Task.objects.filter(user=user)
        return Task.objects.none()
    
    def perform_create(self, serializer):
        """Create a task for current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def by_status(self, request):
        """
        Get tasks filtered by status.
        
        Query params:
            status: pending, in_progress, or completed
        """
        status_filter = request.query_params.get('status')
        
        if not status_filter:
            return Response(
                {'error': 'status query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tasks = self.get_queryset().filter(status=status_filter)
        serializer = self.get_serializer(tasks, many=True)
        
        return Response({
            'status': status_filter,
            'count': tasks.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['POST'])
    def mark_completed(self, request):
        """
        Mark a task as completed.
        
        Expected JSON:
        {
            "task_id": integer
        }
        """
        task_id = request.data.get('task_id')
        
        try:
            task = self.get_queryset().get(id=task_id)
            task, error = TaskService.update_task(task, status='completed')
            
            if error:
                return Response(
                    {'error': error},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.get_serializer(task)
            return Response({
                'message': 'Task marked as completed',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ═════════════════════════════════════════════════════════════════════════════
# NOTE VIEWS
# ═════════════════════════════════════════════════════════════════════════════

class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user notes.
    Provides full CRUD operations for notes.
    """
    
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get notes for current user only."""
        user = self.request.user
        if user and user.is_authenticated:
            return Note.objects.filter(user=user)
        return Note.objects.none()
    
    def perform_create(self, serializer):
        """Create a note for current user."""
        serializer.save(user=self.request.user)


# ═════════════════════════════════════════════════════════════════════════════
# ADMIN VIEWS
# ═════════════════════════════════════════════════════════════════════════════

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def admin_dashboard(request):
    """Admin-only dashboard with system statistics."""
    return Response({
        'message': 'Welcome, Admin',
        'user': request.user.username,
        'role': 'Admin',
        'stats': {
            'total_users': User.objects.count(),
            'total_tasks': Task.objects.count(),
            'total_notes': Note.objects.count(),
        }
    }, status=status.HTTP_200_OK)
