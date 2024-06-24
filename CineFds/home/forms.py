from django import forms
from .models import Movie, MovieCategory, Rating,Comida

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['category', 'movie_name', 'price', 'images', 'rating', 'sinopse', 'duration_minutes']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = MovieCategory
        fields = ['category_name'] 

class MovieRemovalForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = []

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

class ComidaForm(forms.ModelForm):
    class Meta:
        model = Comida
        fields = ['nome', 'preco', 'imagem']