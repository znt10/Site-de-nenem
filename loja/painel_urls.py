from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views_painel

app_name = 'painel'

urlpatterns = [
    path('login/', views_painel.PainelLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('categorias/', views_painel.categoria_lista, name='categoria_lista'),
    path('categorias/nova/', views_painel.categoria_form, name='categoria_criar'),
    path('categorias/<int:pk>/editar/', views_painel.categoria_form, name='categoria_editar'),
    path('categorias/<int:pk>/excluir/', views_painel.categoria_excluir, name='categoria_excluir'),

    path('produtos/', views_painel.produto_lista, name='produto_lista'),
    path('produtos/vendidos/', views_painel.produto_lista, {'vendidos': True}, name='produto_lista_vendidos'),
    path('produtos/novo/', views_painel.produto_form, name='produto_criar'),
    path('produtos/<int:pk>/editar/', views_painel.produto_form, name='produto_editar'),
    path('produtos/<int:pk>/excluir/', views_painel.produto_excluir, name='produto_excluir'),
    path('produtos/<int:pk>/vendido/', views_painel.produto_toggle_vendido, name='produto_toggle_vendido'),
]
