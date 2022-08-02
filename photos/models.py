from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True, default='Other')

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField(upload_to='photos')
    title = models.CharField(max_length=50, blank=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
            return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'pk': self.pk})
