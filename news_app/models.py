from django.db import models

# Create your models here.

class Journalist(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Article(models.Model):
    author = models.ForeignKey(Journalist,on_delete=models.CASCADE,related_name='articles')
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    body = models.TextField()
    location = models.CharField(max_length=120)
    publication_date = models.DateField()


    def __str__(self):
        return f"{self.author} - {self.title}"