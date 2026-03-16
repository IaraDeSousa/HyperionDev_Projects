""" This module defines the data models for the news application, including publishers, articles, newsletters, subscriptions, and password reset tokens. """
from django.conf import settings
from django.db import models


class Publisher(models.Model):
    """
    Model representing a publisher, which can have multiple editors and
    journalists.
    """

    name = models.CharField(max_length=200)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="edited_publishers"
    )
    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="employed_publishers"
    )


class Article(models.Model):
    """
    Model representing an article, indicating if it has been approved by an 
    editor.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Newsletter(models.Model):
    """
    Model representing a newsletter created by journalists or publishers.
    """

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    """
    Model to handle reader subscriptions to publishers and journalists.
    """

    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    subscribed_publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, null=True, blank=True
    )
    subscribed_journalist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="journalist_subscribers",
    )


class ResetToken(models.Model):
    """
    Model representing a password reset token, which is associated with
    a user and has a token value, expiry date, and determines if it has
    been used.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
