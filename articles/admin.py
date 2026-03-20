from django.contrib import admin
from .models import Article, ArticleImage, ArticleVideo

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 3  # shows 3 empty slots to upload
    can_delete = True 

class ArticleVideoInline(admin.TabularInline):
    model = ArticleVideo
    extra = 1
    can_delete = True 

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleImageInline, ArticleVideoInline]
    list_display = ['title', 'author', 'date'] 
   

admin.site.register(Article, ArticleAdmin)