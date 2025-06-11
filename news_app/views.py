from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Journalist, Article
from .serializers import JournalistSerializer, ArticleSerializer

# Journalist API
class JournalistView(APIView):
    def get(self, request):
        journalists = Journalist.objects.all()
        serializer = JournalistSerializer(journalists, many=True)
        return Response({"journalist": serializer.data})

    def post(self, request):
        serializer = JournalistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            saved_journalist = serializer.save()
            return Response({
                "success": f"Journalist '{saved_journalist.first_name}' created successfully"
            })


# Article API
class ArticleView(APIView):
    def get(self, request):
        limit = request.GET.get('_limit')
        articles = Article.objects.all().order_by('-id')
        if limit:
            articles = articles[:int(limit)]
        serializer = ArticleSerializer(articles, many=True)
        return Response({"Articles": serializer.data})

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            saved_article = serializer.save()
            return Response({
                "success": f"Article '{saved_article.title}' created successfully"
            })


# Article Detail API
class ArticleDetailView(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(instance=article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "message": "Article updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({"message": "Article deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
