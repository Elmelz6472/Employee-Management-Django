# Generated by Django 4.0.6 on 2022-08-02 02:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee_management", "0013_employeebaseinformation_bonus"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weeklyhoursforeachemployeeandlocation",
            name="friday_num_hours",
            field=models.PositiveIntegerField(
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="weeklyhoursforeachemployeeandlocation",
            name="monday_num_hours",
            field=models.PositiveIntegerField(
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="weeklyhoursforeachemployeeandlocation",
            name="saturday_num_hours",
            field=models.PositiveIntegerField(
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="weeklyhoursforeachemployeeandlocation",
            name="sunday_num_hours",
            field=models.PositiveIntegerField(
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="weeklyhoursforeachemployeeandlocation",
            name="thursday_num_hours",
            field=models.PositiveIntegerField(
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="weeklyhoursforeachemployeeandlocation",
            name="tuesday_num_hours",
            field=models.PositiveIntegerField(
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="weeklyhoursforeachemployeeandlocation",
            name="wednesday_num_hours",
            field=models.PositiveIntegerField(
                default=0,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(15),
                ],
            ),
        ),
    ]
