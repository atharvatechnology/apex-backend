from django.contrib.auth import get_user_model
from django.test import TestCase

from notes.models import Content, Note

User = get_user_model()


class NoteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.created_by = User.objects.create(
            username="9810468135",
        )
        cls.updated_by = User.objects.create(
            username="9810468134",
        )

        cls.note = Note.objects.create(
            created_by=cls.created_by, updated_by=cls.updated_by, title="This is title"
        )

        cls.content = Content.objects.create(
            name="content1",
            description="desc",
            type="Video",
            file="content/1/cite.pdf",
            note=cls.note,
            created_by=cls.created_by,
            updated_by=cls.updated_by,
        )

    def test_create_notes(self):
        self.assertEqual(self.note.title, str(self.note))
        self.assertIsInstance(self.note, Note)

    def test_content(self):
        self.assertEqual(self.content.name, str(self.content))
        self.assertEqual(self.content.content_location("cite.pdf"), self.content.file)
