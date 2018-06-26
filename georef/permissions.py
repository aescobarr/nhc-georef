from rest_framework import permissions


class HasAdministrativePermission(permissions.BasePermission):
    message = 'Edició d\'usuaris no permesa.'

    def has_permission(self, request, view):
        current_user = request.user
        return current_user.profile and current_user.profile.permission_administrative

