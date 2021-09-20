# Sunday Ucheawaji
# How to build an Hotel Management System

This project attempts to build an hotel management system with Django. Multiple users will be making use of our website. These users include customers, receptionist, managers and Superadmin. The distinguishing factors are the permissions and authorization assigned to the users.
An understanding of Python and basics of Django is a prerequisite to understanding this project. open this https://drive.google.com/drive/folders/1JwKQkefincizwCpZhXnsr3eCF0ZaX45z?usp=sharing for details about the task and schema.

![pexels-jonathan-borba-5563472](https://user-images.githubusercontent.com/61336165/133947900-640a960a-dddc-4405-8cb1-1bd0e17674c7.jpg)


Let's get started
1. Set up the project using your terminal
``` 
>>cd Desktop 
>> mkdir hotel_management_system
>> cd hotel_management_system
 ```

2. Create your virtual environment in which you install your third party packages and activate it
```
>> python3 -m venv hotel_venv
>> source hotel_venv/bin/activate #activated
>> pip3 install django
>> pip3 install django-environ
```

3. We move to creating our django prohect as well as our app. After which we get the hotel app registered in our installed apps in settings.py
```
>> django-admin startapp hotel_management_system
>> python manage.py startapp hotel
```
4. Then we move to configuring the CI/CD continous integration using git-hub actions and then deploy using Heroku

```
name: Hotel Management Test Django
on: [push, pull_request]
jobs:
 build:
 runs-on: ubuntu-latest
steps:
 — uses: actions/checkout@v1
 — name: setup python 3.9
 uses: actions/setup-python@v1
 with:
 python_version: 3.9
 — name: install dependencies
 run: |
 python -m pip install — upgrade pip
 pip install -r requirements.txt
 
 — name: Run migrations
 run: hotel_management_system/hotel_management_system/manage.py migrate
 run: python hms/manage.py migrate 
 — name: Run tests
 run: python3 hms/manage.py test
```

5. The models.py is populated with the following classses

```
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


class CustomAccountManager(BaseUserManager):

    def customer(self, email, username, firstname, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          firstname=firstname, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def receptionist(self, email, username, firstname, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_admin', False)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                "Receptionist must be assigned to is_staff=True"
            )

        return self.customer(email, username, firstname, password, **other_fields)

    def admin(self, email, username, firstname, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                "Superuser must be assigned to is_staff=True"
            )
        if other_fields.get('is_admin') is not True:
            raise ValueError(
                "Admin must be assigned to is_admin=True"
            )

        return self.customer(email, username, firstname, password, **other_fields)

    def create_superuser(self, email, username, firstname, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                "Superuser must be assigned to is_staff=True"
            )

        if other_fields.get('is_admin') is not True:
            raise ValueError(
                "Superuser must be assigned to is_admin=True"
            )

        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True"
            )
        return self.customer(email, username, firstname, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150)
    start_date = models.DateTimeField(default= timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomAccountManager()

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
```

6. The views.py is also populated with the following functions views and class-based views

```
# Authentication modules
from django.contrib.auth import authenticate, login, logout


from django.http import HttpResponse
from .models import Room, RoomType, RoomStatus, NewUser, PaymentType

## class views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView

# modules for rendering the page and also redirecting
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

# module forms for creating user and logging
from .forms import LoginForm, UserRegisterForm
from django.contrib import messages


def homepage(request):
    context = {}
    return render(request, 'hotel/homepage.html', context)


def about(request):
    context = {}
    return render(request, 'hotel/about.html', context)


def admin_login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')

        else:
            msg = 'error validating form'
    return render(request, 'hotel/admin_login.html', {"form": form})


def admin_logout(request):
    logout(request)
    return render(request, 'hotel/admin_logout.html')


def admin_create(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration Successful')
            return redirect('homepage')
        messages.error(request, "Unsuccessful Registration. Invalid Credentials")
    form = UserRegisterForm()
    return render(request, template_name='hotel/admin_create.html', context={'form':form})


class RoomList(ListView):
    model = RoomType
    template_name = 'hotel/room_list.html'


class SingleRoom(DetailView):
    model = RoomType
    template_name = 'hotel/single_room.html'


class AdminList(ListView):
    model = NewUser
    template_name = 'hotel/admin_list.html'


class ShowAdmin(DetailView):
    model = NewUser
    template_name = 'hotel/show_admin.html'


class EditAdmin(UpdateView):
    model = NewUser
    template_name = 'hotel/edit_admin.html'
    fields = '__all__'
    success_url = reverse_lazy('homepage')


class DeleteAdmin(DeleteView):
    model = NewUser
    template_name = 'hotel/delete_admin.html'
    success_url = reverse_lazy('homepage')


room_types = RoomType.objects.all()
room = Room.objects.all()
room_status = RoomStatus.objects.all()


def room_booking(request, room_id):
    room_detail = get_object_or_404(RoomType, pk=room_id)
    return render(request, 'hotel/room_booking.html', {'room': room_detail,'rooms': room_types,'room_no':room})


def room_payment(request,room_id):
    room_detail = get_object_or_404(RoomType, pk=room_id)
    return render(request, 'hotel/room_payment.html', {'room': room_detail,'rooms': room_types,'room_no':room})

```

7. The root urls.py is configured with the following paths

```
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel/', include('hotel.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
8. The hotel app urls.py is configured in this manner
```
from django.urls import path
from .import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about', views.about, name='about'),
    path('rooms/<uuid:room_id>/booking', views.room_booking, name='room-booking'),
    path('rooms/<uuid:room_id>/booking/payment', views.room_payment, name='room-payment'),


    path('rooms', views.RoomList.as_view(), name='room-list'),
    path('rooms/<uuid:pk>', views.SingleRoom.as_view(), name='room-single'),

    path('login/', views.admin_login, name='admin-login'),
    path('logout/', views.admin_logout, name='admin-logout'),


    path('admin', views.AdminList.as_view(), name='admin-list'),
    path('admin/<int:pk>', views.ShowAdmin.as_view(), name='show-admin'),
    path('admin/create', views.admin_create, name='admin-create'),
    path('admin/<int:pk>/edit', views.EditAdmin.as_view(), name='admin-edit'),
    path('admin/<int:pk>/delete', views.DeleteAdmin.as_view(), name='admin-delete'),
]

```

9. The following forms were created for the login forms, registration forms etc.

```
from django import forms
from .models import NewUser, Booking, Room
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
            attrs={
                'class':'form-control'
            }
        ))

    class Meta:
        model = NewUser
        fields = ('username', 'email', 'firstname', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class BookingForm(ModelForm):

    class Meta:
        model = Booking
        fields = "__all__"


class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = "__all__"


class PasswordChange(forms.Form):
    username = forms.CharField(max_length=150)
    new_password = forms.CharField(max_length=150)

```

10. The following models are registered  in the admin.py in order for the changes to be made from the Django Admin

```
from django.contrib import admin
from .models import NewUser, Room, RoomType, RoomStatus, Booking, PaymentType, Payment

admin.site.register(NewUser)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(RoomStatus)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(PaymentType)

```
11. The folllowing changes and additions are made to the settings.py 

```
"""
Django settings for hotel_management_system project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import dj_database_url
import django_heroku
from pathlib import Path

 Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


 Quick-start development settings - unsuitable for production
 See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

 SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7lb-xs9l@z6(#0o=-rmtm!*=(f0&p7z&2nzj+j@&&81iszjmsj'

 SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['sunday-hotel.herokuapp.com', 'localhost', '127.0.0.1']



INSTALLED_APPS = [
    'hotel',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'hotel_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hotel_management_system.wsgi.application'


 Database
 https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': 'hotel_db',
        'USER': 'postgres',
        'PASSWORD': 'holyboy191',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}


 Password validation
 https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


 Internationalization
 https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


 Static files (CSS, JavaScript, Images)
 https://docs.djangoproject.com/en/3.2/howto/static-files/

import os


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

 Default primary key field type
 https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL='hotel.NewUser'
django_heroku.settings(locals())
```
Here is the ERD Diagram
![MicrosoftTeams-image (4)](https://user-images.githubusercontent.com/61336165/133947788-7b7379e5-e101-465b-ae79-19bc04d85975.png)

# About the author
# Sunday Ucheawaji
I am a full stack software developer with indepth understanding of Django, React, Angular, Typescript, Python, Database and Data Analytics.

