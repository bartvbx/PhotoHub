from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from photos.models import Photo
from users.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}! Now you can log in!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def user_settings(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'You successfully updated your profile info!')
            return redirect('user_settings')
        elif password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, f'Your password has been changed!')
            return redirect('user_settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'password_form' : password_form
    }
    return render(request, 'users/user_settings.html', context)


@login_required
def delete_profile_picture(request):
    if request.user.profile.image != 'default.jpg':
        request.user.profile.set_default_image()
        messages.success(request, f'You changed your profile picture to default!')
    return redirect('user_settings')


class UserListView(ListView):
    model = User
    paginate_by = 5
    template_name = 'users/user_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(username__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list


class UserDetalView(DetailView):
    model = User
    context_object_name = 'object'
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['photo_list'] = Photo.objects.filter(author=self.object).all()[:3]
        return context


def follow_user(request, pk):
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    if request.user.is_authenticated:
        if request.user == user:
            messages.warning(request, f'You can\'t follow yourself!')
        elif user.profile.follows.filter(id=request.user.id).exists():
            user.profile.follows.remove(request.user.profile)
            messages.success(request, f'You are no longer following {user}!')
        else:
            user.profile.follows.add(request.user.profile)
            messages.success(request, f'You are following {user}!')
    else:
        messages.error(request, f'You need to be logged in to follow users!', extra_tags='danger')   
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
