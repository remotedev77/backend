from rest_framework import permissions

class CheckFinalTestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
            return request.user.main_test_count > 1

