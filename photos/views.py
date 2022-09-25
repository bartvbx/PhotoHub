from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
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
from .models import Photo, Category, Comment


class PhotoListView(ListView):
    model = Photo
    paginate_by = 10

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


class PhotoComment(LoginRequiredMixin, SingleObjectMixin, SuccessMessageMixin, FormView):
    template_name = 'photos/photo_detail.html'
    form_class = CommentForm
    model = Photo
    success_message = "You added new comment!"

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
        return reverse('photo_detail', kwargs={'pk': self.object.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    fields = ['content']
    success_message = "Your comment was updated successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse('photo_detail', kwargs={"pk": comment.photo.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Comment
    success_message = "Your comment was deleted successfully!"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse('photo_detail', kwargs={"pk": comment.photo.pk})


class PhotoDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PhotoDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PhotoComment.as_view()
        return view(request, *args, **kwargs)


class PhotoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Photo
    fields = ['image', 'title', 'category', 'description']
    success_message = "Photo was added successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Photo
    fields = ['title', 'category', 'description']
    success_message = "Your photo was updated successfully!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        photo = self.get_object()
        if self.request.user == photo.author:
            return True
        return False


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Photo
    success_url = '/'
    success_message = "Photo was deleted successfully!"

    def test_func(self):
        photo = self.get_object()
        if self.request.user == photo.author:
            return True
        return False


def like_photo(request, pk):
    photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))
    if request.user.is_authenticated:
        if request.user == photo.author:
            messages.warning(request, f'You can\'t like your own photo!')
        elif photo.likes.filter(id=request.user.id).exists():
            photo.likes.remove(request.user)
            messages.success(request, f'You disliked photo "{photo.title}" by {photo.author}!')
        else:
            photo.likes.add(request.user)
            messages.success(request, f'You liked photo "{photo.title}" by {photo.author}!')
    else:
        messages.error(request, f'You need to be logged in to like photos!', extra_tags='danger')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def liked_photo_list(request):
    object_list = request.user.liked_photos.all()
    context = {'object_list' : object_list}
    return render(request, 'photos/liked_photo_list.html', context)
