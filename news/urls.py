from django.urls import path
from .views import UserListView, ArticleListView, ArticleDetailView, CategoryListView, CommentListView, NewsClassificationView, NewsRecommendationView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('classify-news/', NewsClassificationView.as_view(), name='classify-news'),
    path('recommend-news/', NewsRecommendationView.as_view(), name='recommend-news'),
]