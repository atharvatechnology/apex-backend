from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group  # , Permission
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile, User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users.

    Includes all the required fields, plus a repeated password.
    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users.

    Includes all the fields on the user,
    but replaces the password field with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    def view_profile(self, obj):
        return mark_safe(
            "<a href="
            f'"{reverse("admin:accounts_profile_change", args=(obj.profile.pk,))}">'
            f"{obj.profile}</a>"
        )

    actions = ["make_active"]

    list_display = [
        "id",
        "name",
        "username",
        "email",
        "is_active",
        "role",
        "last_login",
        "date_joined",
        "view_profile",
    ]
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "role",
    )
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = ("groups",)
    readonly_fields = [
        "last_login",
        "date_joined",
        "otp_generate_time",
    ]
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "role",
                    "otp",
                    "otp_counter",
                    "otp_generate_time",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    date_hierarchy = "date_joined"

    def name(self, object):
        return object.get_full_name()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user
        if not user.is_superuser:
            queryset = queryset.filter(is_superuser=False, is_staff=False)
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        user = request.user
        if not user.is_superuser:
            self.readonly_fields.extend(["is_staff", "is_superuser"])
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        user = request.user
        if not user.is_superuser and db_field.name == "groups":
            kwargs["queryset"] = Group.objects.exclude(name__in=["Admin", "Manager"])
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    @admin.action(description="Mark selected students active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "college_name",
        "faculty",
        "date_of_birth",
    ]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
    ]
    autocomplete_fields = [
        "user",
    ]


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# admin.site.register(Permission)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
