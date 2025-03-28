from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = 'admin'
    REPORTER = 'reporter'
    CLIENT = 'client'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (REPORTER, 'News Reporter'),
        (CLIENT, 'Client')
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CLIENT)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'reporter'})
    published_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('ne', 'Nepali')], default='en')
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


##Nepali News Classification Model##
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')

class NewsClassifier:
    def __init__(self):
        self.model = make_pipeline(TfidfVectorizer(tokenizer=word_tokenize), MultinomialNB())

    def train(self, data, labels):
        self.model.fit(data, labels)

    def predict(self, text):
        return self.model.predict([text])[0]
    
news_classifier = NewsClassifier()


##News Recommendation System##
import random

def recommend_articles(user):
    user_comments = Comment.objects.filter(user=user).values_list('article_category', flat=True)
    recommended_articles =Article.objects.filter(category__in=user_comments).order_by('-published_date')[:5]
    if not recommended_articles.exists():
        recommended_articles = Article.objects.order_by('?')[:5]
    return recommended_articles
