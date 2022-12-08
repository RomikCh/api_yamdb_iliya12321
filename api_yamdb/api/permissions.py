from rest_framework import permissions


class IsAuthorModerAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.is_authenticated

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return (
                obj.author == request.user
                or request.user.is_superuser
                or request.user.role in ('moderator', 'admin')
            )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin')
            )
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == 'admin')
        )