# Generated by Django 4.0.6 on 2022-07-28 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee_management", "0012_generalnotes_modified_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeebaseinformation",
            name="bonus",
            field=models.IntegerField(null=True),
        ),
    ]
