# Generated by Django 5.1.3 on 2024-12-15 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ikibondoapp', '0004_baby_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baby',
            name='DOB',
            field=models.DateTimeField(),
        ),
    ]