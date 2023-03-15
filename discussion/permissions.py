# from common.permissions import IsAdmin,IsStudent
from rest_framework import permissions
class DiscussionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        if (
            user.is_admin or user.is_student
        ) and user.groups.all().first() in user.groups.all():
            return True
        else:
            return False
    def has_object_permission(self, request, view, obj):
        created_by =obj.created_by
        user = request.user
        if (user==created_by) or user.is_admin:
            return True
        else:
            return False
