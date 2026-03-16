from django.db import models


# Note model with title, content and when it was created
class Note(models.Model):
    """
    Model representing a note with a title and content.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
