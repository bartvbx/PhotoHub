from django.urls import path
from . import views

urlpatterns = [
    path('', views.PhotoListView.as_view(), name='photo_list'),
    path('photo/<int:pk>/', views.PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/add/', views.PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/update/', views.PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),
    path('photo/<int:pk>/like/', views.like_photo, name='photo_like'),
    path('liked-photos/', views.liked_photo_list, name='photo_liked_list')
]