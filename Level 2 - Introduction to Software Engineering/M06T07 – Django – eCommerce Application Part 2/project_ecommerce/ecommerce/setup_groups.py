from django.contrib.auth.models import Group, Permission


def create_project_groups(sender, **kwargs):
    """
    :param sender: The model class that sent the signal.
    :param kwargs: Additional keyword arguments.

    Create 'vendor' and 'buyer' groups if they don't exist, and assign
    permissions to the 'vendor' group.
    """
    vendor_group = Group.objects.get_or_create(name="vendor")
    Group.objects.get_or_create(name="buyer")

    try:
        product_permissions = Permission.objects.filter(
            codename__in=[
                "add_product",
                "change_product",
                "delete_product",
                "add_store",
                "change_store",
                "delete_store",
            ]
        )

        vendor_group.permissions.set(product_permissions)

    except Exception as e:
        print(f"Error setting up groups: {e}")
