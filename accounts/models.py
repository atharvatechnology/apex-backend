from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import datetime, make_aware, timedelta
from django.utils.translation import gettext_lazy as _

from accounts.api.otp import OTP
from accounts.validators import PhoneNumberValidator


class UserManager(BaseUserManager):
    """Custom User Manager."""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a user with the given username, email, and password."""
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        _ = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractUser):
    """Custom User model."""

    username_validator = PhoneNumberValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that phone already exists."),
        },
    )
    otp_counter = models.PositiveIntegerField(default=0)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_generate_time = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f"{self.username}"

    def validate_otp(self, otp):
        """To validate received OTP."""
        five_minutes_ago = make_aware(
            datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        )
        if not self.otp:
            return (False, "OTP is already used")
        if self.otp_generate_time < five_minutes_ago:
            return (False, "The OTP is out of date")
        if self.otp != otp:
            return (False, "OTP is not valid")
        return (True, otp)

    def generate_otp(self):
        """To generate OTP and call send otp method."""
        self.otp_counter += 1
        otp = OTP.generateOTP(self.username, self.otp_counter)
        self.otp_generate_time = make_aware(datetime.now())
        self.otp = otp
        OTP.sendOTP(self.username, otp)
        return otp


class Profile(models.Model):
    """Custom Profile model."""

    def profile_image_upload(self, filename):
        """To upload profile image."""
        return f"profile/{self.user.username}/{filename}"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    college_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to=profile_image_upload, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    faculty = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return f"{self.user.username}"
