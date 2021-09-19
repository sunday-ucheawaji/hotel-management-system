# Generated by Django 3.2.6 on 2021-09-19 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('firstname', models.CharField(max_length=150)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('about', models.TextField(blank=True, max_length=500, verbose_name='about')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('CA', 'cash'), ('CC', 'credit card'), ('CH', 'cheques')], max_length=30, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('O', 'occupied'), ('V', 'vacant'), ('R', 'ready'), ('D', 'dirty'), ('C', 'clean'), ('OO', 'out of order')], max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('MS', 'ministerial suite'), ('AM', 'ambassadorial'), ('DIP', 'diplomatic'), ('EX', 'executive'), ('SUP', 'superior'), ('STD', 'standard')], max_length=30, unique=True)),
                ('price', models.CharField(max_length=10)),
                ('about', models.CharField(max_length=250)),
                ('image', models.ImageField(upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('room_no', models.CharField(max_length=5, unique=True)),
                ('price', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('room_status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.roomstatus')),
                ('room_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.roomtype')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('new_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.paymenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.payment')),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room')),
            ],
        ),
    ]
