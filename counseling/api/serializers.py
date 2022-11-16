from rest_framework import serializers

from counseling.models import Counseling


class CounselingListSerializer(serializers.ModelSerializer):
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


class CounselingRetrieveSerializer(serializers.ModelSerializer):
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


class CounselingUpdateSerializer(serializers.ModelSerializer):
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


class CounselingDeleteSerializer(serializers.ModelSerializer):
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
