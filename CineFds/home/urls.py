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

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()