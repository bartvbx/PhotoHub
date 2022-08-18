from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


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
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'You successfully updated your profile info!')
            return redirect('user_settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
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


@login_required
def follow_user(request, pk):
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    if request.user == user:
        messages.warning(request, f'You can\'t follow yourself!')
    elif user.profile.follows.filter(id=request.user.id).exists():
        user.profile.follows.remove(request.user.profile)
        messages.success(request, f'You are no longer following {user}!')
    else:
        user.profile.follows.add(request.user.profile)
        messages.success(request, f'You are following {user}!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
