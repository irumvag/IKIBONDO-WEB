# Generated by Django 5.1.3 on 2024-12-06 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ikibondoapp', '0002_alter_myuser_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='Age',
            field=models.PositiveIntegerField(null=True),
        ),
    ]