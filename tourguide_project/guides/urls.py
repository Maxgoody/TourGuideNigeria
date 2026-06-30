from django.urls import path
from . import views

app_name = 'guides'

urlpatterns = [
    path('', views.guide_list, name='guide_list'),
    path('<int:pk>/', views.guide_detail, name='guide_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('experience/create/', views.experience_create, name='experience_create'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
]
