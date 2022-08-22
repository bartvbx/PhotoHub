from django.db.models import Q
import django_filters
from .models import Photo, Category
from django.contrib.auth.models import User
from django.forms.widgets import TextInput

class PhotoFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), method='category_filter', empty_label="All categories")
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), method='author_filter', empty_label="All users")
    q = django_filters.CharFilter(method='keyword_filter', widget=TextInput(attrs={'placeholder': 'Search by keywords'}))

    class Meta:
        model = Photo
        fields = ['category', 'author', 'q']

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(PhotoFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['category'].field.widget.attrs.update({'class': 'photo-search-form-input'})
        self.filters['author'].field.widget.attrs.update({'class': 'photo-search-form-input'})
        self.filters['q'].field.widget.attrs.update({'class': 'photo-search-form-input'})
    
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
