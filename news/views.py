from .models import recommend_articles
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
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
    
#Added for Login and SignUp Template Viewa
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, 'news/login.html', {'error': 'Invalid credentials'})
    return render(request, 'news/login.html')

def signup_view(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST['email'],
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            password=request.POST['password'],
            role=request.POST['role']
        )
        auth_login(request, user)
        return redirect('/')
    return render(request, 'news/signup.html')

# --- Added Home View ---
def home_view(request):
    articles = Article.objects.all().order_by('-published_date')[:10]
    return render(request, 'news/home.html', {'articles': articles})
