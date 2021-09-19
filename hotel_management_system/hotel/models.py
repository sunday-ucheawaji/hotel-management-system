from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


class CustomAccountManger(BaseUserManager):

    def customer(self, email, username, firstname, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide a valid email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, firstname=firstname, **other_fields)

        user.set_password(password)
        user.save()
        return user

    def receptionist(self, email, username, firstname, password, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", False)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_admin", False)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Receptionist must be assigned to is_staff=True'
            )
        return self.customer(email, username, firstname, password, **other_fields)

    def admin(self, email, username, firstname, password, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", False)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_admin", True)

        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Admin must be assigned to is_admin=True'
            )
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Admin must be assigned to is_staff=True'
            )
        return self.customer(email, username, firstname, password, **other_fields)

    def create_superuser(self, email, username, firstname, password, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_admin", True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True'
            )
        if other_fields.get('is_admin') is not True:
            raise ValueError(
                'Admin must be assigned to is_admin=True'
            )
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Admin must be assigned to is_staff=True'
            )
        return self.customer(email, username, firstname, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique= True)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomAccountManger()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'email']

    def __str__(self):
        return self.username


class RoomType(models.Model):
    ROOM_TYPE = [
        ('MS', 'ministerial suite'),
        ('AM', 'ambassadorial'),
        ('DIP', 'diplomatic'),
        ('EX', 'executive'),
        ('SUP', 'superior'),
        ('STD', 'standard')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=30, unique=True, choices=ROOM_TYPE)
    price = models.CharField(max_length=10)
    about = models.CharField(max_length=250, null=False)
    image = models.ImageField(upload_to='images/', null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Room {self.type} price: {self.price}'


class RoomStatus(models.Model):
    ROOM_STATUS = [
        ('O', 'occupied'),
        ('V', 'vacant'),
        ('R', 'ready'),
        ('D', 'dirty'),
        ('C', 'clean'),
        ('OO', 'out of order')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, unique=True, choices=ROOM_STATUS)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.status}'


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_type_id = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_status_id = models.ForeignKey(RoomStatus, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=5, unique=True)
    price = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Room {self.room_no}'


class PaymentType(models.Model):
    PAYMENT_TYPE = [
        ('CA', 'cash'),
        ('CC', 'credit card'),
        ('CH', 'cheques')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True, choices=PAYMENT_TYPE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_type_id = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    new_user_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'User {self.new_user_id}'


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Booking by user {self.customer_id}'
