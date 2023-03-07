from django.db import models
from django.utils import timezone

from common.models import CreatorBaseModel

# Create your models here.


class Question(CreatorBaseModel):
    content = models.TextField()
    question = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.content

    def reply_count(self):
        return self.replies.count()

    @property
    def is_question(self):
        if self.question is None:
            return True
        return False

    def save(self, *args, **kwargs):
        if (self.question) and self.created_by.is_student:
            question = self.question
            question.updated_at = timezone.now()
            question.updated_by = self.created_by
            question.save()
        super().save(*args, **kwargs)
