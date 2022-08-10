from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
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
from .filters import PhotoFilter
from .forms import CommentForm
from .models import Photo, Category


class PhotoListView(ListView):
    model = Photo
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = PhotoFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        queryset = self.get_queryset()
        filter = PhotoFilter(self.request.GET, queryset)
        context["filter"] = filter
        return context


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

def like_photo(request, pk):
    photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))
    if photo.likes.filter(id=request.user.id).exists():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def liked_photo_list(request):
    object_list = request.user.liked_photos.all()
    context = {'object_list' : object_list}
    return render(request, 'photos/liked_photo_list.html', context)