from rest_framework.permissions import BasePermission

class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                    request.user.is_staff or request.user.is_superuser)
    
class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)