from django.contrib.auth.models import Group
from rest_framework import permissions


def get_permit(user, group_name, user_perm):
    group = Group.objects.get(name=group_name)
    if user.is_anonymous:
        return False
    if user_perm and group in user.groups.all():
        return True
    return False


class IsAdminOrSuperAdminOrDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        if (
            user.is_super_admin or user.is_admin or user.is_director
        ) and user.groups.all().first() in user.groups.all():
            return True
        return False


class IsSuperAdminOrDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        if (
            user.is_super_admin or user.is_director
        ) and user.groups.all().first() in user.groups.all():
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
        return get_permit(request.user, "Super Admin", request.user.is_super_admin)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Admin", request.user.is_admin)


class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Director", request.user.is_director)


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Teacher", request.user.is_teacher)


class IsAccountant(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Accountant", request.user.is_accountant)


class IsCashier(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Cashier", request.user.is_cashier)


class IsCounsellor(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Counsellor", request.user.is_counsellor)


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Staff", request.user.is_office_staff)


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Student", request.user.is_student)
