from rest_framework import serializers

from notes.models import Content, Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["title", "created_at", "updated_at"]


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["name", "description", "type", "file", "note"]
