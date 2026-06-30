from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Categoria, Produto


def home(request):
    categorias = Categoria.objects.all()
    destaques = Produto.objects.filter(ativo=True, vendido=False, destaque=True).prefetch_related('imagens')[:8]
    novidades = Produto.objects.filter(ativo=True, vendido=False).prefetch_related('imagens')[:8]
    return render(request, 'loja/home.html', {
        'categorias': categorias,
        'destaques': destaques,
        'novidades': novidades,
    })


def produto_lista(request):
    produtos = Produto.objects.filter(ativo=True, vendido=False).select_related('categoria').prefetch_related('imagens')
    categorias = Categoria.objects.all()

    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        produtos = produtos.filter(categoria__slug=categoria_slug)

    termo = request.GET.get('q', '').strip()
    if termo:
        produtos = produtos.filter(
            Q(nome__icontains=termo) | Q(descricao__icontains=termo)
        )

    return render(request, 'loja/produto_lista.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_atual': categoria_slug,
        'termo': termo,
    })


def produto_detalhe(request, slug):
    produto = get_object_or_404(
        Produto.objects.select_related('categoria').prefetch_related('imagens'),
        slug=slug, ativo=True, vendido=False,
    )
    relacionados = Produto.objects.filter(
        ativo=True, vendido=False, categoria=produto.categoria
    ).exclude(pk=produto.pk).prefetch_related('imagens')[:4]
    return render(request, 'loja/produto_detalhe.html', {
        'produto': produto,
        'relacionados': relacionados,
    })
