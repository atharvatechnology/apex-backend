from rest_framework import serializers

from counseling.models import Counseling


class CounselingSerializer(serializers.ModelSerializer):
    """Serializer for Counseling."""

    class Meta:
        model = Counseling
        fields = (
            "id",
            "student_name",
            "counsellor",
            "note",
            "phone_number",
            "date",
        )
