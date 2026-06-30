from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:booking_pk>/', views.review_create, name='review_create'),
]
