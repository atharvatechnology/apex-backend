from rest_framework import serializers


class GenerateSignatureSerializer(serializers.Serializer):
    """Serializer for generating signature."""

    meeting_id = serializers.IntegerField()
    role = serializers.IntegerField()

    class Meta:
        fields = ("meeting_id", "role")
