from django import forms
from .models import Article, ArticleImage, ArticleVideo

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'body', 'thumb']

class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        fields = ['image', 'caption']

class ArticleVideoForm(forms.ModelForm):
    class Meta:
        model = ArticleVideo
        fields = ['video', 'caption']