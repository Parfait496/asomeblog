from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, ArticleImage, ArticleVideo, Comment, Like, Bookmark
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, ArticleImageForm, ArticleVideoForm, CommentForm
from django.db.models import Q

def article_list(request):
    query = request.GET.get('q', '')
    articles = Article.objects.all().order_by('-date')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    return render(request, 'articles/article_list.html', {'articles': articles, 'query': query})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.all().order_by('-date')
    comment_form = CommentForm()
    user_liked = request.user.is_authenticated and article.likes.filter(user=request.user).exists()
    user_bookmarked = request.user.is_authenticated and article.bookmarks.filter(user=request.user).exists()
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'user_bookmarked': user_bookmarked,
    })

@login_required(login_url="/accounts/login/")
def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
    return redirect('articles:detail', slug=slug)

@login_required(login_url="/accounts/login/")
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    slug = comment.article.slug
    if comment.author == request.user or request.user.is_staff:
        comment.delete()
    return redirect('articles:detail', slug=slug)

@login_required(login_url="/accounts/login/")
def toggle_like(request, slug):
    article = get_object_or_404(Article, slug=slug)
    like, created = Like.objects.get_or_create(article=article, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': article.like_count()})

@login_required(login_url="/accounts/login/")
def toggle_bookmark(request, slug):
    article = get_object_or_404(Article, slug=slug)
    bookmark, created = Bookmark.objects.get_or_create(article=article, user=request.user)
    if not created:
        bookmark.delete()
        bookmarked = False
    else:
        bookmarked = True
    return JsonResponse({'bookmarked': bookmarked})

@login_required(login_url="/accounts/login/")
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('article').order_by('-date')
    return render(request, 'articles/bookmarks.html', {'bookmarks': bookmarks})

@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            for img in request.FILES.getlist('images'):
                ArticleImage.objects.create(
                    article=article,
                    image=img,
                    caption=request.POST.get('image_caption', '')
                )

            for vid in request.FILES.getlist('videos'):
                ArticleVideo.objects.create(
                    article=article,
                    video=vid,
                    caption=request.POST.get('video_caption', '')
                )

            return redirect('articles:detail', slug=article.slug)
    else:
        form = ArticleForm()
        image_form = ArticleImageForm()
        video_form = ArticleVideoForm()

    return render(request, 'articles/article_create.html', {
        'form': form,
        'image_form': image_form,
        'video_form': video_form,
    })