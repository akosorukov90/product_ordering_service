from rest_framework.permissions import BasePermission


class IsAdminUserOrOwnUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user == obj.user or request.user.is_staff)


class IsShop(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'shop'
