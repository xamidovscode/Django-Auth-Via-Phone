from rest_framework.permissions import BasePermission

class IsCodeVerified(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.status == "code_verified"
        return False