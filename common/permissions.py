from django.contrib.auth.models import Group
from rest_framework import permissions


def get_permit(user, group_id):
    group = Group.objects.get(id=group_id)
    if user.is_anonymous:
        return False
    if user.is_authenticated and group in user.groups.all():
        return True
    return False


class IsAllUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        if user.is_authenticated:
            return True
        return False


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 1)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 2)


class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 3)


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 4)


class IsAccountant(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 5)


class IsCashier(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 6)


class IsCounsellor(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 7)


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 8)


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, 9)
