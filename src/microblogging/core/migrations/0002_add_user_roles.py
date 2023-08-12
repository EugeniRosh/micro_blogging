from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.models import Group, Permission
from django.db import migrations

if TYPE_CHECKING:
    from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
    from django.db.migrations.state import StateApps

USER_ROLES = {
    "user": [
        "add_twits",
        "delete_twits",
    ]
}


def populate_user_roles(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    for role, permission_list in USER_ROLES.items():
        group = Group.objects.create(name=role)
        permission = Permission.objects.filter(codename__in=permission_list)
        group.permissions.set(permission)


def delete_user_roles(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    for role, permission_list in USER_ROLES.items():
        Group.objects.get(name=role).delete()


class Migration(migrations.Migration):
    dependencies: list[tuple[str, str]] = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=populate_user_roles, reverse_code=delete_user_roles),
    ]
