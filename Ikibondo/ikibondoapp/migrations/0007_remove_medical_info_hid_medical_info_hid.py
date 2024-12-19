# Generated by Django 5.1.3 on 2024-12-15 22:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ikibondoapp', '0006_alter_baby_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medical_info',
            name='HID',
        ),
        migrations.AddField(
            model_name='medical_info',
            name='HID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bornhospital', to='ikibondoapp.hospital'),
            preserve_default=False,
        ),
    ]