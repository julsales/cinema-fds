from django import forms
from .models import Movie, MovieCategory

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['category', 'movie_name', 'price', 'images']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = MovieCategory
        fields = ['category_name'] 

class MovieRemovalForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = []
