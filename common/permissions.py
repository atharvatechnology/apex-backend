from django.contrib.auth.models import Group
from rest_framework import permissions


def get_permit(user, group_name):
    group = Group.objects.get(name=group_name)
    if user.is_anonymous:
        return False
    user_perm_dict = {
        "Super Admin": user.is_super_admin,
        "Admin": user.is_admin,
        "Director": user.is_director,
        "Teacher": user.is_teacher,
        "Accountant": user.is_accountant,
        "Cashier": user.is_cashier,
        "Counsellor": user.is_counsellor,
        "Staff": user.is_office_staff,
        "Student": user.is_student,
    }
    if user_perm_dict[group_name] and group in user.groups.all():
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
        return get_permit(request.user, "Super Admin")


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Admin")


class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Director")


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Teacher")


class IsAccountant(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Accountant")


class IsCashier(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Cashier")


class IsCounsellor(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Counsellor")


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Staff")


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_permit(request.user, "Student")
