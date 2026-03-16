from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Publisher, Article, Subscription


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, id, username and email fields.
    """
    class Meta:
        """
        Meta class to specify the model and fields for the UserSerializer.
        """
        model = User
        fields = ["id", "username", "email"]


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Publisher model, id and name fields.
    """
    class Meta:
        """
        Meta class to specify the model and fields for the
        PublisherSerializer."""
        model = Publisher
        fields = ["id", "name"]


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model, including nested serializers for author and publisher.
    """
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        """"
        Meta class to specify the model and fields for the ArticleSerializer"""
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "created_at",
            "is_approved",
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subscription model, including  serializers for reader,
    subscribed publisher and journalist.
    """
    class Meta:
        """
        Meta class to specify the model and fields for the
        SubscriptionSerializer.
        """
        model = Subscription
        fields = [
            "id",
            "reader",
            "subscribed_publisher",
            "subscribed_journalist",
        ]
