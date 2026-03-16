from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """Form for creating and updating Note instances."""
    class Meta:
        """Class to specify the model and fields for the form."""
        model = Note
        fields = ['title', 'content']
