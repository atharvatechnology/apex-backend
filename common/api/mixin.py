from django.db.models import BooleanField, Case, When
from rest_framework import serializers

from enrollments.api.utils import is_enrolled, is_enrolled_active


class EnrolledSerializerMixin(serializers.ModelSerializer):
    is_enrolled = serializers.SerializerMethodField()
    is_enrolled_active = serializers.SerializerMethodField()

    # (
    #     "is_enrolled",
    #     "is_enrolled_active",
    # )

    def get_is_enrolled(self, obj):
        return is_enrolled(obj, self.context["request"].user)

    def get_is_enrolled_active(self, obj):
        """Return True if the user is enrolled and active.

        Args:
            obj (db object): Objects which can be enrolled into.

        Returns
            bool: True if the user is enrolled and active.

        """
        return is_enrolled_active(obj, self.context["request"].user)


class PublishableModelMixin:
    """Filter the queryset to only include published instances."""

    def get_queryset(self):
        return super().get_queryset().published()


class InterestWiseOrderMixin:
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, "profile"):
            return (
                super()
                .get_queryset()
                .annotate(
                    cat=Case(
                        When(category__in=user.profile.interests.all(), then=True),
                        default=False,
                        output_field=BooleanField(),
                    )
                )
                .order_by("-cat", "-id")
            )
        return super().get_queryset()
