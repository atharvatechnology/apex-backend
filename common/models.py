from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CreatorBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creater"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="updater"
    )

    class Meta:
        abstract = True
