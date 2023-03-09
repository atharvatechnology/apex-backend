from django.contrib.auth import get_user_model
from django.db import models

from common.utils import get_human_readable_date_time

User = get_user_model()


class StaffTracking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stafftracking",
    )
    latitude = models.DecimalField(max_digits=15, decimal_places=13)
    longitude = models.DecimalField(max_digits=15, decimal_places=13)
    address = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id", "-user"]

    def __str__(self):
        return f"{self.user} at {get_human_readable_date_time(self.created_at)}"


class StaffConnectionStatus(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staffconnectionstatus",
    )
    is_connected = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id", "-user"]

    def __str__(self):
        return f"{self.user} is {self.is_connected}"
