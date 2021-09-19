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