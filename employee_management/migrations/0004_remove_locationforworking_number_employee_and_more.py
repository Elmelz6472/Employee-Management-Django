# Generated by Django 4.0.6 on 2022-07-16 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee_management", "0003_alter_locationforworking_number_employee"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="locationforworking",
            name="number_employee",
        ),
        migrations.AddField(
            model_name="locationforworking",
            name="notes",
            field=models.CharField(max_length=500, null=True),
        ),
    ]
