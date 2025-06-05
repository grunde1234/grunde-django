from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import Journalist, Article
from .serializers import JournalistSerializer, ArticleSerializer

# Create your views here.
class JournalistView(APIView):
    def get(self, request):# handles get requests
        journalist = Journalist.objects.all()
        serializer = JournalistSerializer(journalist, many=True)
        return Response({"journalist":serializer.data})
    def post(self, request):
        serializer = JournalistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            saved_article = serializer.save()
        return Response({"success": "Article '{}' created successfully".format(saved_article.first_name)})
        
        


class ArticleView(APIView):
    def get(self, request):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        return Response({'Articles': serializer.data})
    def post(self, request):
       # article = request.data.get('article')

       serializer = ArticleSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):
           saved_article = serializer.save()
       return Response({"success": "Article '{}' created successfully".format(saved_article.title)})

