from django.shortcuts import render,  get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import MovieForm,CategoryForm, ComidaForm
from .models import MovieCategory
def home(request):
    movies = Movie.objects.all()
    context = {'movies': movies, 'range': range(1, 6)}
    return render(request, "home.html", context)

class HomePageView(TemplateView):
    template_name = 'home.html'

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home') 

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    context = {
        'movie': movie,
        'formatted_duration': movie.get_duration_display(),
    }
    return render(request, 'movie_detail.html', context)

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


@login_required(login_url='/login/')
def editar_filme(request, movie_uid=None):
    movies = Movie.objects.all()
    selected_movie = None
    categories = MovieCategory.objects.all()
    
    if movie_uid:
        selected_movie = get_object_or_404(Movie, uid=movie_uid)
    
    if request.method == 'POST':
        if selected_movie:
            form = MovieForm(request.POST, instance=selected_movie)
            if form.is_valid():
                form.save()
                messages.success(request, "Filme atualizado com sucesso.")
                return redirect('editar_filme')
            else:
                messages.error(request, "Erro ao atualizar filme.")
        else:
            messages.error(request, "Erro ao atualizar filme")
            return redirect('editar_filme')
    else:
        if selected_movie:
            form = MovieForm(instance=selected_movie)
        else:
            form= MovieForm(instance=None)
            messages.info(request, "Selecione um filme")
    
    return render(request, 'editar_filme.html', {'movies': movies, 'form': form, 'categories': categories, 'selected_movie': selected_movie})


@login_required(login_url='/login/')
def adicionar_genero(request):
    if request.method == 'POST':
        form2 = CategoryForm(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect('adicionar_genero')
    else:
        form2 = CategoryForm()
    return render(request, 'adicionar_genero.html', {'form2': form2})

@login_required(login_url='/login/')
def remover_genero(request):
    if request.method == 'POST':
        genero_uid = request.POST.get('genero_uid')  
        genero = get_object_or_404(MovieCategory, uid=genero_uid)  
        genero.delete()
        return redirect('remover_genero') 
    generos = MovieCategory.objects.all()
    return render(request, 'remover_genero.html', {'generos': generos})

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')

def add_cart(request, movie_uid):
    try:
        user = request.user
        movie_obj = get_object_or_404(Movie, uid=movie_uid)
        max_seats = request.GET.get('max_seats') 
        cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
        CartItems.objects.create(cart=cart, movie=movie_obj)
        messages.success(request, "Filme adicionado ao carrinho com sucesso!")
        return redirect('/')
    except Movie.DoesNotExist:
        messages.error(request, "Filme não encontrado.")
        return redirect('/')
    except Exception as e:
        messages.error(request, "Algo deu errado ao adicionar ao carrinho.")
        return redirect('/')
@login_required(login_url='/login/')



def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        return render(request, "cart.html", {'carts': cart})
    except Cart.DoesNotExist:
        messages.error(request, "Carrinho não encontrado.")
        return redirect('/')
    except Exception as e:
        messages.error(request, "Algo deu errado ao acessar o carrinho.")
        return redirect('/')



@login_required(login_url='/login/')

def remove_cart_item(request, cart_item_uid):
    try:
        cart_item = get_object_or_404(CartItems, uid=cart_item_uid)
        cart_item.delete()
        return redirect('/cart/')
    except CartItems.DoesNotExist:
        messages.error(request, "Item do carrinho não encontrado.")
        return redirect('/cart/')
    except Exception as e:
        messages.error(request, "Algo deu errado ao remover o item do carrinho.")
        return redirect('/cart/')
        
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

    return render(request, 'payment.html')

def payment_success(request):
    messages.success(request, "Filme pago com sucesso")
    return render(request, 'payment_success.html')

def escolha_acento(request):
        comidas = Comida.objects.all()
        return render(request, 'escolha_acento.html', {'comidas': comidas})



def usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email:
            messages.error(request, 'Nome de usuário e e-mail são obrigatórios.')
            return render(request, 'usuario.html', {'user': request.user})

        user = request.user
        user.username = username
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, 'Informações atualizadas com sucesso.')
        return redirect('home')

    return render(request, 'usuario.html', {'user': request.user})

def adicionar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('escolha_acento')
    else:
        form = ComidaForm()
    
    return render(request, 'adicionar_comida.html', {'form': form})

def remover_comida(request):
    if request.method == 'POST':
        comida_id = request.POST.get('comida')
        try:
            comida = Comida.objects.get(id=comida_id)
            comida.delete()
            return redirect('/pagina_adm/') 
        except Comida.DoesNotExist:
            pass 
    comidas = Comida.objects.all()
    return render(request, 'remover_comida.html', {'comidas': comidas})

def lista_filmes(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'lista_filmes.html', context)
