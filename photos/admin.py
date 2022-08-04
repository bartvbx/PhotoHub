from django.contrib import admin
from .models import Category, Photo, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PhotoAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Category)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment)
