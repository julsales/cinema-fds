from django.db import models

# Create your models here.

class cadastro(models.Model):
      
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    email = models.TextField(max_length=255)
    
class Question(models.Model):
    title = models.CharField(max_length=200, null=False)
    details = models.TextField(null=False)
    have_tried = models.TextField()
    created_date = models.DateTimeField("Created on")
