from django.urls import path, include
from django.contrib import admin
from . import views
from home.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import HomePageView

urlpatterns = [
    path("",views.home,name="home"),
    path('rate_movie/<movie_uid>/', views.rate_movie, name='rate_movie'),
    path('cart/', views.cart, name='cart'),
    path('remove_cart_item/<cart_item_uid>', remove_cart_item, name='remove_cart'),
    path('add_cart/<movie_uid>', add_cart , name="add-cart"),
    path('search/', search_movies, name='search_movies'),
    path("login/",views.login_page,name="login"),
    path('register/', views.register_page, name="register"),
    path("admin/", admin.site.urls),
    path('cadastro-filme/', views.add_movie, name='cadastro_filme'),
    path('', HomePageView.as_view(), name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('adicionar-genero/', views.adicionar_genero, name='adicionar_genero'),
    path('editar_filme/', views.editar_filme, name='editar_filme'),
    path('remover-genero/', views.remover_genero, name='remover_genero'),
    path('pagina_adm/', views.pagina_adm, name='pagina_adm'),
    path('remover_filme/', views.remover_filme, name='remover_filme'),
    path('pagamento/', views.payment, name='payment'),
    path('pagamento/sucesso/', views.payment_success, name='payment_success'),
    path('escolha_acento/', views.escolha_acento, name='escolha_acento'),
    path('pag_fim/', views.pag_fim, name='pag_fim'),
    path('delete_movie_by_name/', views.delete_movie_by_name, name='delete_movie_by_name'),
    path('editar_filme/', editar_filme, name='editar_filme'),
    path('usuario/', views.usuario, name='usuario'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()