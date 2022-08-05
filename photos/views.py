from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from django.views.generic.detail import SingleObjectMixin
from .models import Photo
from .forms import CommentForm


class PhotoListView(ListView):
    model = Photo
    paginate_by = 5


class PhotoDisplay(DetailView):
    model = Photo
    template_name = 'photos/photo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PhotoComment(SingleObjectMixin, FormView):
    template_name = 'photos/photo_detail.html'
    form_class = CommentForm
    model = Photo

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.photo = self.object
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('photo-detail', kwargs={'pk': self.object.pk})


class PhotoDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PhotoDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PhotoComment.as_view()
        return view(request, *args, **kwargs)


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
