from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

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

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.article.title}"


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f"{self.user} likes {self.article.title}"


class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f"{self.user} bookmarked {self.article.title}"


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='article_images/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.article.title}"


class ArticleVideo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='videos')
    video = CloudinaryField('video', resource_type='video', blank=True)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Video for {self.article.title}"