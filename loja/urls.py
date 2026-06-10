from django.urls import path

from . import views

app_name = 'loja'

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.produto_lista, name='produto_lista'),
    path('produtos/<slug:slug>/', views.produto_detalhe, name='produto_detalhe'),
]
