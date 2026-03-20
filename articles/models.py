from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(default='default.png', blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50]+'...'


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='article_images/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.article.title}"


class ArticleVideo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='article_videos/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Video for {self.article.title}"