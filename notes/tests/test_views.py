from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from notes.models import Note

User = get_user_model()


class NoteTest(APITestCase):
    def setUp(self):
        self.created_by = User.objects.create(username="9842021425")
        self.updated_by = User.objects.create(username="9810468134")
        self.client = APIClient()
        self.client.force_authenticate(user=self.created_by)
        self.data = {
            "created_by": "9800991847",
            "updated_by": "9800991847",
            "title": "title 1",
        }
        self.note = Note.objects.create(
            created_by=self.created_by, updated_by=self.updated_by, title="title 1"
        )

    def test_note_create_api_view(self):
        url = reverse("notes:note-create")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)

    def test_note_list_api_view(self):
        url = reverse("notes:note-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_note_filter_without_api_value(self):
        response = self.client.get(reverse("notes:note-list") + "?search=abc")
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, [])

    def test_note_filter_with_api_value(self):
        response = self.client.get(reverse("notes:note-list") + "?search=title 1")
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result[0]["title"], "title 1")

    def test_update_note_value(self):
        data = {
            "created_by": "9815333275",
            "updated_by": "9807096968",
            "title": "title 2",
        }
        url = reverse("notes:note-update", args=[1])
        response = self.client.put(url, data=data)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["title"], "title 2")

    def test_delete_note_value(self):
        url = reverse("notes:note-delete", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
