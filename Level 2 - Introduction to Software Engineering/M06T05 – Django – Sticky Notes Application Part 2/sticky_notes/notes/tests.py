# notes/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    """
    Test case for the Note model to make sure it stores data correctly.
    """
    def setUp(self):
        """
        Create a note to use in the tests
        """
        self.note = Note.objects.create(
            title='Study Django',
            content='Learn how to write unit tests.'
        )

    def test_note_content(self):
        """Test that the note stores the title and content correctly."""
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, 'Study Django')
        self.assertEqual(note.content, 'Learn how to write unit tests.')

    def test_string_representation(self):
        """Test the __str__ method returns the title."""
        self.assertEqual(str(self.note), 'Study Django')


class NoteViewTest(TestCase):
    """
    Test case for the views of the notes program to ensure they work as
    expected.
    """
    def setUp(self):
        """
        Create a note to use in the view tests
        """
        self.note = Note.objects.create(
            title='Initial Note',
            content='This is for testing views.'
        )

    def test_note_list_view(self):
        """Test the note list view contains the note."""
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Initial Note')

    def test_note_create_view_post(self):
        """Test creating a note and confirming it appears on the list page."""
        response = self.client.post(reverse('note_create'), {
            'title': 'New Note',
            'content': 'Content of the new note.'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Note')

    def test_note_update_view_post(self):
        """Test updating a note and confirming the new title appears."""
        url = reverse("note_update", args=[self.note.pk])

        response = self.client.post(
            url,
            {
                "title": "Updated Title",
                "content": "Updated content.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated Title')
        # Confirm the old title is no longer there
        self.assertNotContains(response, 'Initial Note')

    def test_note_delete_view_post(self):
        """Test deleting a note and confirming it is gone from the list."""
        url = reverse("note_delete", args=[self.note.pk])

        response = self.client.post(
            url,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Initial Note")

    def test_404_on_invalid_note(self):
        """Verify 404 for notes that do not exist."""
        response = self.client.get(reverse('note_update', args=[999]))
        self.assertEqual(response.status_code, 404)