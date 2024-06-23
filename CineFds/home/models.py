from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
     
    class Meta:
        abstract = True

class MovieCategory(BaseModel):
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name

class Movie(BaseModel):
    category = models.ForeignKey(MovieCategory, on_delete=models.CASCADE, related_name="movies")
    movie_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.CharField(max_length=500)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    sinopse = models.TextField(max_length=1000, blank=True)
    user_rating = models.FloatField(default=0)
    num_ratings = models.IntegerField(default=0)  # Novo campo

class Cart(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="cart")
    is_paid = models.BooleanField(default=False)

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Rating(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.FloatField(choices=[(i, i) for i in range(6)], default=0)  # Permite valores flutuantes

class UserRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.FloatField()  # Permite valores flutuantes

    class Meta:
        unique_together = ('movie', 'user')

class Comida(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    imagem = models.ImageField(upload_to='comidas/')

    def __str__(self):
        return self.nome
