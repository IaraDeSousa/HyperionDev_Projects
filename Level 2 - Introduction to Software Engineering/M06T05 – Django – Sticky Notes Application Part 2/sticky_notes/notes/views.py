from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm


# List all notes in the database and display them on the note list page
def note_list(request):
    """
    View to display a list of all notes.

    :param request: HTTP request object.
    :return: Rendered template with a list of notes.
    """
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})


# Create a new note and save it to the database
def note_create(request):
    """
    View to display details of a specific post.

    :param request: HTTP request object.
    :return: Rendered template with form to create a new note.
    """
    form = NoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('note_list')
    return render(request, 'notes/note_form.html', {'form': form})


# Update an a note in the database using its id, if the note doesn't exist,
# then we return a 404 not found error
def note_update(request, pk):
    """
    View to display details of a specific note.

    :param request: HTTP request object.
    :param pk: Primary key of the note.
    :return: Rendered template with form to update the specified note.
    """
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('note_list')
    return render(request, 'notes/note_form.html', {'form': form})


# Delete a note from the database using its id, if the note doesn't exist, 
# then we return a 404 not found error
def note_delete(request, pk):
    """
    View to delete a specific note.

    :param request: HTTP request object.
    :param pk: Primary key of the note.
    :return: Redirects to the note list page after deletion.
    """
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
    return redirect('note_list')
