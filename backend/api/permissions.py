from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class AllowAnyGetPost(IsAuthenticated):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.method == 'POST'


class CurrentUserOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_admin() or obj.id == user.id


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return request.user.is_admin


class IsAdminAuthorOrReadPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        if request.user.is_anonymous:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        if request.user.is_anonymous:
            return False
        return request.user.is_admin or obj.author == request.user
