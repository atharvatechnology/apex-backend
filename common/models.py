from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.timezone import localtime, now

User = get_user_model()


class CreatorBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator_%(class)ss"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="updater_%(class)ss"
    )

    class Meta:
        abstract = True


class PublishedQueryset(models.QuerySet):
    def published(self):
        today = localtime(now())
        return (
            super()
            .get_queryset()
            .filter(is_published=True or Q(publish_date__lte=today))
        )


class PublishedModel(models.Model):
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True, null=True)

    objects = models.Manager.from_queryset(PublishedQueryset)()

    class Meta:
        abstract = True

    @property
    def is_visible(self):
        today = localtime(now())
        return self.is_published or self.publish_date <= today
