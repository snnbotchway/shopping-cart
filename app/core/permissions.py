from rest_framework.permissions import SAFE_METHODS, IsAdminUser


class IsAdminUserOrReadOnly(IsAdminUser):
    """
    Allow all users to read data, but only admins to create, update or delete.
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
