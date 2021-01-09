from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to Admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)


class IsSuperAdminUser(BasePermission):
    """
    Allows access only to Super Admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_super_admin)
