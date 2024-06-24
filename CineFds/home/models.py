from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


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
    duration_minutes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    @property
    def get_duration_display(self):
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        return f"{hours}h {minutes}min" if hours else f"{minutes}min"
    
    def __str__(self):
        return self.movie_name
    
class MovieShowtimes(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    showtime1 = models.TimeField(default=timezone.now)
    showtime2 = models.TimeField(default=timezone.now, blank=True, null=True)
    showtime3 = models.TimeField(default=timezone.now, blank=True, null=True)
    showtime4 = models.TimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"Showtimes for {self.movie.movie_name}"    
    


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

class Comida(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    imagem = models.ImageField(upload_to='comidas/')

    def __str__(self):
        return self.nome
