from django.urls import path
from .views import *

app_name="news_app"

urlpatterns=[
   path('journalist/', JournalistView.as_view() ),
   path('articles/', ArticleView.as_view()),
]
