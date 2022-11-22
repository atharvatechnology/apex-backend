from rest_framework import serializers

from counseling.models import Counseling


class CounselingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating counseling."""

    class Meta:
        model = Counseling
        fields = (
            "id",
            "student_name",
            "counsellor",
            "note",
            "phone_number",
            "created_at",
        )


class CounselingListSerializer(serializers.ModelSerializer):
    """Serializer for Listing Counseling."""

    class Meta:
        model = Counseling
        fields = (
            "id",
            "student_name",
            "counsellor",
            "note",
            "phone_number",
            "created_at",
        )


class CounselingRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for Retrieving  Counseling."""

    class Meta:
        model = Counseling
        fields = (
            "id",
            "student_name",
            "counsellor",
            "note",
            "phone_number",
            "created_at",
        )


class CounselingUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Updating Counseling."""

    class Meta:
        model = Counseling
        fields = (
            "id",
            "student_name",
            "counsellor",
            "note",
            "phone_number",
            "created_at",
        )
