from django.urls import path, re_path
from . import views


app_name='articles'

urlpatterns = [
    path('', views.article_list, name="list"),
    path('create', views.article_create, name="create"),
    path('bookmarks/', views.my_bookmarks, name="bookmarks"),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name="delete_comment"),
    re_path(r'^(?P<slug>[\w-]+)/$', views.article_detail, name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/comment/$', views.add_comment, name='add_comment'),
    re_path(r'^(?P<slug>[\w-]+)/like/$', views.toggle_like, name='toggle_like'),
    re_path(r'^(?P<slug>[\w-]+)/bookmark/$', views.toggle_bookmark, name='toggle_bookmark'),
]