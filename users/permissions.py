from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_owner


class IsOwnerAccount(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object()


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser
