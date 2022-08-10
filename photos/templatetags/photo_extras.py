from django import template
from django.shortcuts import get_object_or_404
from ..models import Photo


register = template.Library()


@register.simple_tag
def photo_liked_by_user(photo_id, user_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    if photo.likes.filter(id=user_id).exists():
        liked = True
    else:
        liked = False
    return liked
