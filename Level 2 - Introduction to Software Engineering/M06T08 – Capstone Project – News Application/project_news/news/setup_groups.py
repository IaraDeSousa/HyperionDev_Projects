from django.contrib.auth.models import Group, Permission


def create_project_groups(sender, **kwargs):
    """
    :param sender: The model class that sent the signal.
    :param kwargs: Additional keyword arguments.

    Create 'editor' and 'journalist' groups if they don't exist, and assign
    permissions to the 'editor' and 'journalist' groups.
    """
    editor_group = Group.objects.get_or_create(name="editor")
    journalist_group = Group.objects.get_or_create(name="journalist")

    try:
        editor_permissions = Permission.objects.filter(
            codename__in=[
                "change_article",
                "delete_article",
                "add_newsletter",
                "change_newsletter",
                "delete_newsletter",
            ]
        )

        journalist_permissions = Permission.objects.filter(
            codename__in=[
                "add_article",
                "change_article",
                "delete_article",
                "add_newsletter",
                "change_newsletter",
                "delete_newsletter",
            ]
        )

        editor_group = Group.objects.get(name="editor")
        editor_group.permissions.set(editor_permissions)

        journalist_group = Group.objects.get(name="journalist")
        journalist_group.permissions.set(journalist_permissions)

    except Exception as e:
        print(f"Error setting up groups: {e}")
