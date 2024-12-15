# Generated by Django 5.1.3 on 2024-12-15 15:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ikibondoapp', '0007_remove_baby_pid_baby_pid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baby',
            name='Age',
        ),
        migrations.RemoveField(
            model_name='medical_info',
            name='DOB',
        ),
        migrations.AddField(
            model_name='baby',
            name='DOB',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medical_info',
            name='Age',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medical_info',
            name='BID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Baby', to='ikibondoapp.baby'),
        ),
        migrations.RemoveField(
            model_name='medical_info',
            name='HID',
        ),
        migrations.AddField(
            model_name='medical_info',
            name='HID',
            field=models.ManyToManyField(related_name='bornhospital', to='ikibondoapp.hospital'),
        ),
    ]
