from django.db import migrations


def single_to_multiple_role(apps, schema_editor):
    SUPER_ADMIN = 1
    ADMIN = 2
    DIRECTOR = 3
    TEACHER = 4
    ACCOUNTANT = 5
    CASHIER = 6
    COUNSELLOR = 7
    STAFF = 8
    STUDENT = 9
    role_choices = (
        (SUPER_ADMIN, "Super Admin"),
        (ADMIN, "Admin"),
        (DIRECTOR, "Director"),
        (TEACHER, "Teacher"),
        (ACCOUNTANT, "Accountant"),
        (CASHIER, "Cashier"),
        (COUNSELLOR, "Counsellor"),
        (STAFF, "Staff"),
        (STUDENT, "Student"),
    )

    User = apps.get_model("accounts", "User")
    Role = apps.get_model("accounts", "Role")
    from django.contrib.auth.models import Group

    # Create all roles as per Business Logic
    for roles in range(1, 10):
        Role.objects.create(id=roles)
        Group.objects.create(name=role_choices[roles - 1][1])

    for data in User.objects.all():
        if data.role == 1:
            data.roles.add(1)
        elif data.role == 2:
            data.roles.add(4)
        elif data.role == 3:
            data.roles.add(3)
        elif data.role == 4:
            data.roles.add(9)
        data.save()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0015_auto_20221122_1443"),
    ]

    operations = [
        migrations.RunPython(single_to_multiple_role),
    ]


# Generated by Django 3.0.7 on 2021-09-29 08:38