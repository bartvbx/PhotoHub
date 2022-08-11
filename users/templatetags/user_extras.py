from django import template
from django.shortcuts import get_object_or_404
from ..models import Profile


register = template.Library()


@register.simple_tag
def user_followed_by_user(followed_id, follower_id):
    profile = get_object_or_404(Profile, pk=followed_id)
    if profile.follows.filter(id=follower_id).exists():
        followed = True
    else:
        followed = False
    return followed
