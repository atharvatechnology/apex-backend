from rest_framework import serializers

from ..models import Exam


class ExamMiniSerializer(serializers.ModelSerializer):
    """Exam Mini Serializer."""

    is_practice = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ("id", "name", "is_practice")
        read_only_fields = fields

    def get_is_practice(self, obj):
        return obj.is_practice
