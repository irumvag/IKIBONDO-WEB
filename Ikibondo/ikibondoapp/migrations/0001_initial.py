# Generated by Django 5.1.3 on 2024-12-02 09:43

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('UserGuide', models.TextField()),
                ('Description', models.CharField(max_length=100)),
                ('SerialNumber', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('LocationId', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('Country', models.CharField(blank=True, default='Rwanda', max_length=100)),
                ('Provence', models.CharField(max_length=100)),
                ('District', models.CharField(max_length=100)),
                ('Village', models.CharField(max_length=100)),
                ('Streetcode', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Medical_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HID', models.PositiveBigIntegerField()),
                ('BID', models.PositiveBigIntegerField()),
                ('DOB', models.DateField()),
                ('Born_height', models.PositiveBigIntegerField()),
                ('Born_weight', models.PositiveBigIntegerField()),
                ('Method_Used_in_Birth', models.CharField(max_length=100)),
                ('Midwife_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Medical Infos',
            },
        ),
        migrations.CreateModel(
            name='Vacinne_and_measure',
            fields=[
                ('VID', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('Vacinne_name', models.CharField(max_length=100)),
                ('Details', models.TextField()),
                ('Age_Limit', models.PositiveIntegerField()),
                ('Time_to_inject', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Myuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number must be 10 digits long.', regex='^\\d{10}$')])),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('HID', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('Names', models.CharField(max_length=100)),
                ('Hospitaltype', models.TextField()),
                ('LocationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Hospital', to='ikibondoapp.location')),
            ],
        ),
        migrations.CreateModel(
            name='CHW',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chw_profile', to=settings.AUTH_USER_MODEL)),
                ('HID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chw_profile', to='ikibondoapp.hospital')),
                ('LocationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chw_profile', to='ikibondoapp.location')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('NID', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('Age', models.PositiveIntegerField()),
                ('Phone', models.CharField(max_length=10)),
                ('Role', models.CharField(choices=[('Admin', 'Admin'), ('Parent', 'Parent'), ('CHW', 'CHW')], max_length=50)),
                ('Location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ikibondoapp.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parent_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Parents',
            },
        ),
    ]
