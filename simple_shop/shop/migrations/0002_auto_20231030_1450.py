from django.contrib.auth.models import Group, Permission
from django.db import migrations
from django.contrib.contenttypes.models import ContentType

from ..permissions import BuyerGroupPermissions, SellerGroupPermissions


ROLE_PERMISSIONS = [
    BuyerGroupPermissions,
    SellerGroupPermissions
]


def add_groups_with_permissions(apps, schema_editor):
    """
    Creating instances of Group classes with given list of GroupPermissions
    :param apps:
    :param schema_editor:
    :return:
    """
    for role in ROLE_PERMISSIONS:
        group, group_created = Group.objects.get_or_create(name=role.GROUP_NAME)
        role_instance = role()
        role_instance.set_permission_list()
        for permission in role_instance.PERMISSION_LIST:
            model = apps.get_model(f"{permission['app_name']}", f"{permission['model_name']}")
            content_type = ContentType.objects.get_for_model(model)
            permission, created = Permission.objects.get_or_create(
                name=permission["name"],
                codename=permission["codename"],
                content_type=content_type
            )
            group.permissions.add(permission)
        group.save()


def revert_add_groups_migration(apps, schema_editor):
    Group.objects.get(name__in=[r.GROUP_NAME for r in ROLE_PERMISSIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_groups_with_permissions, revert_add_groups_migration)
    ]
