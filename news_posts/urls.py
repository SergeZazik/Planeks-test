from django.urls import path, include
from .views import (
    NewsPostListView,
    NewsPostDetailView,
    NewsPostCreateView,
    NewsPostUpdateView,
    NewsPostDeleteView,
    # subscribe_view,
    # unsubscribe_view,
)


app_name = 'news_posts'

urlpatterns = [
    path('', NewsPostListView.as_view(), name='news_post_list'),
    path('create/', NewsPostCreateView.as_view(), name='news_post_create'),
    path('<slug:slug>/', NewsPostDetailView.as_view(), name='news_post_detail'),
    path('<slug:slug>/update/', NewsPostUpdateView.as_view(), name='news_post_update'),
    path('<slug:slug>/delete/', NewsPostDeleteView.as_view(), name='news_post_delete'),
]
