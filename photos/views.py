from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Photo


class PhotoListView(ListView):
    model = Photo
    paginate_by = 5


class PhotoDetailView(DetailView):
    model = Photo


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['image', 'title', 'category', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    fields = ['title', 'category', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        photo = self.get_object()
        if self.request.user == photo.author:
            return True
        return False


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    success_url = '/'

    def test_func(self):
        photo = self.get_object()
        if self.request.user == photo.author:
            return True
        return False
