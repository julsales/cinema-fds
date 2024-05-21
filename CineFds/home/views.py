from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Movie
from .forms import MovieForm,CategoryForm, MovieRemovalForm

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

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = MovieForm()
    return render(request, 'cadastro_filme.html', {'form': form})

from django.contrib import messages


from django.shortcuts import redirect, render, get_object_or_404
from .models import Movie, MovieCategory

def editar_filme(request):
    movies = Movie.objects.all()
    categories = MovieCategory.objects.all()  # Query para todas as categorias de filme
    
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        new_name = request.POST.get('new_name')
        new_price = request.POST.get('new_price')
        new_category_id = request.POST.get('new_category')  # Receba o ID da nova categoria
        
        # Verificar se o ID do filme foi fornecido
        if movie_id:
            # Obter o objeto do filme ou retornar 404 se não encontrado
            movie = get_object_or_404(Movie, id=movie_id)
            
            # Atualizar os campos do filme com os novos valores
            if new_name:
                movie.movie_name = new_name
            if new_price:
                movie.price = new_price
            if new_category_id:
                new_category = get_object_or_404(MovieCategory, id=new_category_id)
                movie.category = new_category
            
            # Salvar as alterações no banco de dados
            movie.save()
            
            # Redirecionar para a página inicial após salvar
            return redirect('home')
    
    return render(request, 'editar_filme.html', {'movies': movies, 'categories': categories})

def adicionar_genero(request):
    if request.method == 'POST':
        form2 = CategoryForm(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect('home')
    else:
        form2 = CategoryForm()
    return render(request, 'adicionar_genero.html', {'form2': form2})

def remover_genero(request):
    return render(request, 'remover_genero.html')


def remover_filme(request):
    movies = Movie.objects.all()
    selected_movie = None

    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        if movie_id:
            try:
                selected_movie = Movie.objects.get(id=movie_id)
                selected_movie.delete()  
                return redirect('pagina_adm') 
            except Movie.DoesNotExist:
                pass

    return render(request, 'remover_filme.html', {'movies': movies, 'selected_movie': selected_movie})

def delete_movie_by_name(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name')
        normalized_name = normalize_text(movie_name)
        try:
            movie = Movie.objects.filter(movie_name__iexact=normalized_name)
            movie.delete()
            messages.success(request, "Filme removido com sucesso!")
        except Movie.DoesNotExist:
            messages.error(request, "Filme não encontrado.")
        return redirect('remover_filme')

    movies = Movie.objects.all()
    return render(request, 'remover_filme.html', {'movies': movies})

def normalize_text(text):
    return text.lower()

def pag_fim(request):
    return render(request, 'pag_fim.html')

def add_cart(request, movie_uid):
    user = request.user
    movie_obj = Movie.objects.get(uid=movie_uid)
    max_seats = request.GET.get('max_seats')
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_items = CartItems.objects.create(cart=cart, movie=movie_obj)
     
    return redirect('/')
@login_required(login_url='/login/')

def cart(request):
    print(request.user)
    cart = Cart.objects.get(is_paid=False, user=request.user)
    return render(request, "cart.html", {'carts': cart})
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


def pagina_adm(request):
    return render(request, 'pagina_adm.html')


def payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        numero_cartao = request.POST.get('numero_cartao')
        endereco = request.POST.get('endereco')
        return render(request, 'payment_success.html')  

    return render(request, 'payment.html')

def payment_success(request):
    return render(request, 'payment_success.html')

def escolha_acento(request):
    return render(request, 'escolha_acento.html')