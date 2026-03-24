"""
Utility Functions for Accounts Application
Common utilities and helpers used across the app.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for REST API.
    Provides consistent error response format.
    
    Args:
        exc: Exception instance
        context: Dictionary with context information
        
    Returns:
        Response: Formatted error response
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, let Django handle the exception
    if response is None:
        return None
    
    # Customize the response format
    if response.status_code in [400, 401, 403, 404, 500]:
        custom_response_data = {
            'error': True,
            'status_code': response.status_code,
            'message': 'An error occurred',
            'details': response.data,
        }
        response.data = custom_response_data
    
    return response


def get_error_response(message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: dict = None) -> Response:
    """
    Create a standardized error response.
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code
        details (dict): Additional error details
        
    Returns:
        Response: Formatted error response
    """
    data = {
        'error': True,
        'message': message,
        'status_code': status_code,
    }
    
    if details:
        data['details'] = details
    
    return Response(data, status=status_code)


def get_success_response(message: str, data: dict = None, status_code: int = status.HTTP_200_OK) -> Response:
    """
    Create a standardized success response.
    
    Args:
        message (str): Success message
        data (dict): Response data
        status_code (int): HTTP status code
        
    Returns:
        Response: Formatted success response
    """
    response_data = {
        'error': False,
        'message': message,
        'status_code': status_code,
    }
    
    if data:
        response_data['data'] = data
    
    return Response(response_data, status=status_code)
