from rest_framework.permissions import BasePermission

class IsAdminUserCustom(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    

    #(..\env\Scripts\activate) avtivate virtual environment command