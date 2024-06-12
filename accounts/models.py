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
from common.utils import generate_qrcode


class Role(models.Model):
    SUPER_ADMIN = 1
    ADMIN = 2
    DIRECTOR = 3
    TEACHER = 4
    ACCOUNTANT = 5
    CASHIER = 6
    COUNSELLOR = 7
    STAFF = 8
    STUDENT = 9
    CONTENT_CREATOR = 10
    role_choices = (
        (SUPER_ADMIN, "Super Admin"),
        (ADMIN, "Admin"),
        (DIRECTOR, "Director"),
        (TEACHER, "Teacher"),
        (ACCOUNTANT, "Accountant"),
        (CASHIER, "Cashier"),
        (COUNSELLOR, "Counsellor"),
        (STAFF, "Staff"),
        (STUDENT, "Student"),
        (CONTENT_CREATOR, "Content Creator"),
    )
    super_admin_choices = (
        (ADMIN, "Admin"),
        (DIRECTOR, "Director"),
        (TEACHER, "Teacher"),
        (ACCOUNTANT, "Accountant"),
        (CASHIER, "Cashier"),
        (COUNSELLOR, "Counsellor"),
        (STAFF, "Staff"),
        (STUDENT, "Student"),
        (CONTENT_CREATOR, "Content Creator"),
    )
    admin_choices = (
        (DIRECTOR, "Director"),
        (TEACHER, "Teacher"),
        (ACCOUNTANT, "Accountant"),
        (CASHIER, "Cashier"),
        (COUNSELLOR, "Counsellor"),
        (STAFF, "Staff"),
        (STUDENT, "Student"),
        (CONTENT_CREATOR, "Content Creator"),
    )
    staff_choices = (
        (SUPER_ADMIN, "Super Admin"),
        (ADMIN, "Admin"),
        (DIRECTOR, "Director"),
        (ACCOUNTANT, "Accountant"),
        (CASHIER, "Cashier"),
        (COUNSELLOR, "Counsellor"),
        (STAFF, "Staff"),
        (CONTENT_CREATOR, "Content Creator"),
    )
    trackable_staff_choices = (
        (ACCOUNTANT, "Accountant"),
        (CASHIER, "Cashier"),
        (COUNSELLOR, "Counsellor"),
        (STAFF, "Staff"),
    )
    id = models.PositiveSmallIntegerField(choices=role_choices, primary_key=True)

    def __str__(self):
        return self.get_id_display()

    def role_dict(self):
        return {role[0]: role[1] for role in self.role_choices}


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

    def get_queryset(self):
        return super().get_queryset().select_related("profile")


class User(AbstractUser):
    """Custom User model."""

    roles = models.ManyToManyField(Role)

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
        db_index=True,
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
        return (False, "OTP is not valid") if self.otp != otp else (True, otp)

    def generate_otp(self, action):
        """To generate OTP and call send otp method."""
        self.otp_counter += 1
        otp = OTP.generateOTP(self.username, self.otp_counter)
        self.otp_generate_time = make_aware(datetime.now())
        self.otp = otp
        OTP.sendOTP(self.username, otp, action)
        return otp

    def get_roles(self):
        all_roles = self.roles.all()
        if not all_roles:
            return None
        user_roles = []
        for roles in all_roles:
            user_roles.extend(
                role_value
                for role_id, role_value in Role.role_choices
                if roles.id == role_id
            )
        return user_roles

    def check_role(self, roles):
        return roles in self.roles.all().values_list("id", flat=True)

    @property
    def is_student(self):
        return self.check_role(Role.STUDENT)

    @property
    def is_teacher(self):
        return self.check_role(Role.TEACHER)

    @property
    def is_director(self):
        return self.check_role(Role.DIRECTOR)

    @property
    def is_super_admin(self):
        return self.is_superuser or self.check_role(Role.SUPER_ADMIN)

    @property
    def is_accountant(self):
        return self.check_role(Role.ACCOUNTANT)

    @property
    def is_admin(self):
        return self.check_role(Role.ADMIN)

    @property
    def is_cashier(self):
        return self.check_role(Role.CASHIER)

    @property
    def is_counsellor(self):
        return self.check_role(Role.COUNSELLOR)

    @property
    def is_office_staff(self):
        return self.check_role(Role.STAFF)

    @property
    def is_content_creator(self):
        return self.check_role(Role.CONTENT_CREATOR)


class Profile(models.Model):
    """Custom Profile model.

    This model extends the default User model by adding additional fields to store
    profile information about users.

    Attributes
        user: A one-to-one relationship to the default User model.
        college_name: The name of the user's college or university.
        image: An optional image file for the user's profile picture.
        qr_code: An optional image file for the user's QR code.
        date_of_birth: The user's date of birth.
        faculty: The user's faculty or department.
        address: The user's address.
        interests: A many-to-many relationship to the CourseCategory model.

    """

    def profile_image_upload(self, filename):
        """Generate a filepath for a profile image file.

        This function takes a filename and generates a filepath to store the file
        in the format "profile/{username}/{filename}". The {username} variable is
        replaced with the username of the user associated with this instance.

        Args:
            filename: The name of the file being uploaded.

        Returns
            A string representing the filepath where the file should be stored.

        """
        return f"profile/{self.user.username}/{filename}"

    def qr_code_image_upload(self, filename):
        """Generate a filepath for a QR code image file.

        This function takes a filename and generates a filepath to store the file
        in the format "qr_code/{username}/{filename}". The {username} variable is
        replaced with the username of the user associated with this instance.

        Args:
            filename: The name of the file being uploaded.

        Returns
            A string representing the filepath where the file should be stored.

        """
        return f"qr_code/{self.user.username}/{filename}"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    college_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to=profile_image_upload, null=True, blank=True)
    qr_code = models.FileField(upload_to=qr_code_image_upload, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    faculty = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    interests = models.ManyToManyField("courses.CourseCategory", blank=True)

    class Meta:
        ordering = ["user"]

    def save(self, *args, **kwargs):
        """Override the default save method to generate a QR code for the user.

        If the instance does not already have a QR code, this function
        generates one using the user's username and saves the path to
        the instance. It then calls the superclass save method to save
        the instance to the database.

        Args:
            *args: Positional arguments passed to the save method.
            **kwargs: Keyword arguments passed to the save method.

        Returns
            None

        """
        usr_name = self.user.username
        # Generate a QR code for the user if one does not already exist.
        if not self.qr_code:
            qr_path = generate_qrcode(usr_name)
            self.qr_code = qr_path
        super().save(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the Profile instance.

        This function returns a string representation of the instance by returning
        the username of the associated user.

        Args:
            None

        Returns
            A string representing the instance.

        """
        return f"{self.user.username}"

    def generate_qr_code(self):
        """Generate a QR code for the user and saves the path to the instance.

        This function generates a QR code for the user's username using the
        `generate_qrcode` function and saves the resulting path to the `qr_code`
        field of the instance. It then calls the instance's `save` method to
        persist the changes to the database.

        Args:
            None

        Returns
            None

        """
        qr_path = generate_qrcode(self.user.username)
        self.qr_code = qr_path
        self.save()


class AccountDeleteion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
