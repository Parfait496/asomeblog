from django.contrib import admin
from .models import Article, ArticleImage, ArticleVideo

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 3  # shows 3 empty slots to upload

class ArticleVideoInline(admin.TabularInline):
    model = ArticleVideo
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageInline, ArticleVideoInline]

admin.site.register(Article, ArticleAdmin)