from rest_framework import serializers
from .models import *

class JournalistSerializer(serializers.Serializer):
   first_name = serializers.CharField(max_length=60)
   last_name = serializers.CharField(max_length=60)
   email = serializers.EmailField()
   #bio = serializers.CharField()

   def validate_email(self, value):
        if Journalist.objects.filter(email=value).exists():
            raise serializers.ValidationError("A journalist with this email already exists.")
        return value

   def create(self, validated_data):
       return Journalist.objects.create(**validated_data)

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=120)
    description = serializers.CharField(max_length=200)
    body = serializers.CharField()
    location = serializers.CharField(max_length=120)
    publication_date = serializers.DateField()
    author_email = serializers.EmailField(write_only=True)  # only for input
    
    # This field will be shown when serializing Article objects (GET requests)
    author_email_display = serializers.SerializerMethodField(read_only=True)

    def get_author_email_display(self, obj):
        return obj.author.email if obj.author else None

    def create(self, validated_data):
        author_email = validated_data.pop('author_email')
        try:
            author = Journalist.objects.get(email=author_email)
        except Journalist.DoesNotExist:
            raise serializers.ValidationError(f"Journalist with email '{author_email}' does not exist.")
        return Article.objects.create(author=author, **validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        instance.location = validated_data.get('location', instance.location)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        #instance.author_email = validated_data.get('author_email', instance.author_email)

        instance.save()
        return instance


""" from rest_framework import serializers
from .models import Journalist, Article

class ArticleSerializer(serializers.ModelSerializer):
    # Accept author_email on input, but don't expect it as a model field on Article
    author_email = serializers.EmailField(write_only=True)

    # Show author's email on output
    author_email_display = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'description', 'body', 'location', 'publication_date',
            'author_email',      # for input only
            'author_email_display',  # for output only
        ]

    def create(self, validated_data):
        author_email = validated_data.pop('author_email')
        try:
            author = Journalist.objects.get(email=author_email)
        except Journalist.DoesNotExist:
            raise serializers.ValidationError(f"No journalist found with email '{author_email}'.")
        article = Article.objects.create(author=author, **validated_data)
        return article
 """