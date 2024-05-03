from django.shortcuts import render,  get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Movie
from .forms import MovieForm

def home(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, "home.html", context)

class HomePageView(TemplateView):
    template_name = 'home.html'

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home') 

def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
             
            if not user_obj.exists():
                messages.error(request, "Usuário não encontrado")
                return redirect('/login/')
             
            user_obj = authenticate(username=username, password=password)
             
            if user_obj:
                login(request, user_obj)
                return redirect('/')
             
            messages.error(request, "Senha errada")
            return redirect('/login/')
         
        except Exception as e:
            messages.error(request, "Algo deu errado.....")
            return redirect('/register/')
     
    return render(request, "login.html")

def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
             
            if user_obj.exists():
                messages.error(request, "Nome de usuário já utilizado")
                return redirect('/register/')
             
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
             
            messages.success(request, "Conta criada com sucesso")
            return redirect('/login/')
         
        except Exception as e:
            messages.error(request, "Algo deu errado....")
            return redirect('/register/')
     
    return render(request, "register.html")
@login_required(login_url="/login/")

def add_cart(request, movie_uid):
    user = request.user
    movie_obj = Movie.objects.get(uid=movie_uid)
     
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_items = CartItems.objects.create(cart=cart, movie=movie_obj)
     
    return redirect('/')
@login_required(login_url='/login/')

def cart(request):
    print(request.user)
    cart = Cart.objects.get(is_paid=False, user=request.user)
    context = {'carts': cart}
    return render(request, "cart.html", context)
@login_required(login_url='/login/')

def remove_cart_item(request, cart_item_uid):
    try:
        CartItems.objects.get(uid=cart_item_uid).delete()
        return redirect('/cart/')
    except Exception as e:
        print(e)
        
def search_movies(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(movie_name__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'search_results.html', {'movies': movies, 'query': query})

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MovieForm()
    return render(request, 'cadastro_filme.html', {'form': form})
def index(request):
    return render(request, 'index.html')


def pagina_adm(request):
    return render(request, 'pagina_adm.html')

def adicionar_filme(request):
    return render(request, 'adicionar_filme.html')

def adicionar_genero(request):
    return render(request, 'adicionar_genero.html')

def remover_genero(request):
    return render(request, 'remover_genero.html')

from django.shortcuts import render

def remover_filme(request,movie_id):
    movie = get_object_or_404(Movie, uid=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie')
    return render(request, 'remover_filme.html', {'movie': movie})
