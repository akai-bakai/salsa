from rest_framework.permissions import BasePermission

class IsProductOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.owner

