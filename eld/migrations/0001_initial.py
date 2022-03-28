# Generated by Django 3.2.9 on 2022-03-06 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('image', models.ImageField(default='/default.jpg', upload_to='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('company_name', models.CharField(max_length=100, unique=True)),
                ('usdot', models.IntegerField()),
                ('time_zone', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=100)),
                ('org_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.IntegerField(blank=True, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='DRIVERS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activated', models.TimeField(auto_created=True, blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=30)),
                ('driver_license_number', models.CharField(max_length=250)),
                ('dr_li_issue_state', models.CharField(max_length=100)),
                ('co_driver', models.CharField(blank=True, max_length=100, null=True)),
                ('home_terminal_address', models.CharField(blank=True, max_length=200, null=True)),
                ('home_terminal_time_zone', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=True)),
                ('trail_number', models.IntegerField()),
                ('enable_dr_eld', models.BooleanField(default=False)),
                ('enable_dr_elog', models.BooleanField(default=False)),
                ('allow_yard', models.BooleanField(default=False)),
                ('allow_personal_c', models.BooleanField(default=False)),
                ('terminated', models.TimeField(blank=True, default=None, null=True)),
                ('app_version', models.CharField(blank=True, max_length=200, null=True)),
                ('device_version', models.CharField(blank=True, max_length=500, null=True)),
                ('main_office', models.CharField(max_length=700, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld.company')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Drivers',
            },
        ),
        migrations.CreateModel(
            name='ELD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=30)),
                ('notes_eld', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('status', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld.company')),
            ],
        ),
        migrations.CreateModel(
            name='RegisterCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('time', models.TimeField(blank=True, default=None, null=True)),
                ('code', models.IntegerField()),
                ('password', models.CharField(max_length=150)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_id', models.CharField(max_length=200, unique=True)),
                ('make', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('license_plate_num', models.IntegerField(unique=True)),
                ('license_plate_issue_state', models.CharField(max_length=100)),
                ('vin', models.CharField(blank=True, max_length=30, null=True)),
                ('notes_vehicle', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('status', models.BooleanField(default=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld.company')),
                ('eld_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='eld.eld')),
            ],
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trailer_number', models.CharField(max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld.company')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld.drivers')),
            ],
        ),
        migrations.CreateModel(
            name='EventDriver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engine_state', models.CharField(blank=True, max_length=45, null=True)),
                ('vin', models.CharField(blank=True, max_length=50, null=True)),
                ('speed_kmh', models.CharField(blank=True, max_length=50, null=True)),
                ('odometer_km', models.CharField(blank=True, max_length=50, null=True)),
                ('trip_distance_km', models.CharField(blank=True, max_length=50, null=True)),
                ('hours', models.CharField(blank=True, max_length=50, null=True)),
                ('trip_hours', models.CharField(max_length=50)),
                ('voltage', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('time', models.DateTimeField()),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('gps_speed_kmh', models.CharField(max_length=50)),
                ('course_deg', models.CharField(max_length=50)),
                ('namsats', models.CharField(max_length=50)),
                ('altitude', models.CharField(max_length=50)),
                ('drop', models.CharField(max_length=50)),
                ('sequence', models.CharField(max_length=50)),
                ('firmware', models.CharField(max_length=50)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld.drivers')),
            ],
        ),
        migrations.AddField(
            model_name='drivers',
            name='vehicle_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld.vehicle'),
        ),
    ]
