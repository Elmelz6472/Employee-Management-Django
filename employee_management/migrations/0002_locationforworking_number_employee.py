# Generated by Django 4.0.6 on 2022-07-15 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="locationforworking",
            name="number_employee",
            field=models.IntegerField(null=True),
        ),
    ]
