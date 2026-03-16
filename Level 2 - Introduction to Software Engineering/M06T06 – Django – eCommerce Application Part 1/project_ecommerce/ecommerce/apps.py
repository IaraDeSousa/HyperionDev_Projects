from django.apps import AppConfig
from django.db.models.signals import post_migrate


class EcommerceConfig(AppConfig):
    """Configuration for the ecommerce app."""

    name = "ecommerce"

    def ready(self):
        """
        When the app is ready, groups and permissions are set up for the
        project.
        """
        from .setup_groups import create_project_groups

        post_migrate.connect(create_project_groups, sender=self)
