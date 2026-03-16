from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = "news"

    def ready(self):
        """
        When the app is ready, groups and permissions are set up for the
        project.
        """
        from .setup_groups import create_project_groups
        from django.db.models.signals import post_migrate
        from .tweet import Tweet

        Tweet()
        post_migrate.connect(create_project_groups, sender=self)
