from django import forms
from .models import Article, ArticleImage, ArticleVideo, Comment

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share your thoughts...',
                'class': 'comment-input',
            })
        }
        labels = {'body': ''}