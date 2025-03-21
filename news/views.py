from .models import recommend_articles
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Article, Category, Comment, User, news_classifier
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class NewsClassificationView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        text = request.data.get("text", "")
        category = news_classifier.predict(text)
        return Response({"predicted_category": category})
    
class NewsRecommendationView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        recommended_articles = recommend_articles(request.user)
        serializer = ArticleSerializer(recommended_articles, many=True)
        return Response(serializer.data)
    
def home_view(request):
    return render(request, 'index.html')
