from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('create/<int:experience_pk>/', views.booking_create, name='booking_create'),
    path('<int:pk>/accept/', views.booking_accept, name='booking_accept'),
    path('<int:pk>/decline/', views.booking_decline, name='booking_decline'),
    path('<int:pk>/complete/', views.booking_complete, name='booking_complete'),
    path('<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
]
