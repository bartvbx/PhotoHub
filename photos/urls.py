from django.urls import path
from . import views

urlpatterns = [
    path('', views.PhotoListView.as_view(), name='photo_list'),
    path('photos/<int:pk>/', views.PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/add/', views.PhotoCreateView.as_view(), name='photo_create'),
    path('photos/<int:pk>/update/', views.PhotoUpdateView.as_view(), name='photo_update'),
    path('photos/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),
    path('photos/<int:pk>/like/', views.like_photo, name='photo_like'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('liked-photos/', views.liked_photo_list, name='photo_liked_list')
]