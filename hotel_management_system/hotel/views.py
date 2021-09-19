# Authentication modules
from django.contrib.auth import authenticate, login, logout


from django.http import HttpResponse
from .models import Room, RoomType, RoomStatus, NewUser, PaymentType

# class views
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


