from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import os
from .validators import file_size_validator


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True, default='Other')

    def __str__(self):
        return self.name


def rename_uploaded_photo(instance, filename):
    file_base, file_extension = os.path.splitext(filename)
    return f'photos/{instance.slug + file_extension}'


class Photo(models.Model):
    image = models.ImageField(upload_to=rename_uploaded_photo, validators=[file_size_validator])
    title = models.CharField(max_length=70, blank=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_photos')
    slug = models.SlugField(max_length=70, blank=True)
    
    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)

    def __str__(self):
            return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('photo_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
            return f'{self.content}'
