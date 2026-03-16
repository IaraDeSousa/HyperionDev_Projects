import base64
from unittest.mock import patch
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Article, Publisher, Subscription


class SubscriptionAPITests(APITestCase):
    def setUp(self):
        """Set up the data for testing."""
        self.reader = User.objects.create_user(
            username="reader", password="password"
        )
        self.journalist = User.objects.create_user(
            username="journalist", password="password"
        )
        self.publisher = Publisher.objects.create(name="Daily Planet")

        self.article_a = Article.objects.create(
            title="Journalist Scoop",
            content="Content A",
            author=self.journalist,
            is_approved=True,
        )
        self.article_b = Article.objects.create(
            title="Publisher News",
            content="Content B",
            author=User.objects.create_user(
                username="journalist9", password="password"
            ),
            publisher=self.publisher,
            is_approved=True,
        )
        self.article_c = Article.objects.create(
            title="Secret News",
            content="Content C",
            author=User.objects.create_user(
                username="stranger", password="password123"
            ),
            is_approved=True,
        )

        Subscription.objects.create(
            reader=self.reader, subscribed_journalist=self.journalist
        )
        Subscription.objects.create(
            reader=self.reader, subscribed_publisher=self.publisher
        )

        self.url = reverse("api_subscribed_articles")

    @patch("news.views.Tweet")
    def test_get_subscribed_articles_authenticated(self, mock_tweet):
        """Verify the API returns only subscribed articles using Basic Auth."""

        credentials = "reader:password"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        auth_header = f"Basic {encoded_credentials}"

        response = self.client.get(self.url, HTTP_AUTHORIZATION=auth_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        titles = [article["title"] for article in response.data]
        self.assertIn("Journalist Scoop", titles)
        self.assertIn("Publisher News", titles)
        self.assertNotIn("Secret News", titles)

    def test_get_subscribed_articles_unauthenticated(self):
        """Verify that unauthenticated users are blocked."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
