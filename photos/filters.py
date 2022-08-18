from django.db.models import Q
import django_filters
from .models import Photo, Category
from django.contrib.auth.models import User

class PhotoFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), method='category_filter', label='Select category')
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), method='author_filter', label='Select author')
    q = django_filters.CharFilter(method='keyword_filter', label="Search by keywords")

    class Meta:
        model = Photo
        fields = ['category', 'author', 'q']
    
    def category_filter(self, queryset, name, value):
        return queryset.filter(category__name__exact=value)

    def author_filter(self, queryset, name, value):
        return queryset.filter(author__username__exact=value)

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(author__username__icontains=value)
        )
