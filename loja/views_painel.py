from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.http import require_POST

from .decorators import staff_required
from .forms import CategoriaForm, ImagemProdutoFormSet, PainelLoginForm, ProdutoForm
from .models import Categoria, Produto


class PainelLoginView(View):
    template_name = 'loja/painel/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = PainelLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PainelLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_staff:
                form.add_error(None, 'Esta conta não tem acesso ao painel.')
                return render(request, self.template_name, {'form': form})
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': form})


# --- Categoria ---

@staff_required
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, 'loja/painel/categoria_lista.html', {
        'categorias': categorias,
        'total_produtos': Produto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'produtos_inativos': Produto.objects.filter(ativo=False).count(),
    })


@staff_required
def categoria_form(request, pk=None):
    categoria = get_object_or_404(Categoria, pk=pk) if pk else None
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria salva com sucesso.')
            return redirect('painel:categoria_lista')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'loja/painel/categoria_form.html', {'form': form, 'categoria': categoria})


@staff_required
def categoria_excluir(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoria excluída.')
        except ProtectedError:
            messages.error(request, 'Não é possível excluir: existem produtos nesta categoria.')
        return redirect('painel:categoria_lista')
    return render(request, 'loja/painel/categoria_confirmar_exclusao.html', {'categoria': categoria})


# --- Produto ---

ORDENACOES_PRODUTO = {
    'nome': 'nome',
    '-nome': '-nome',
    'preco': 'preco',
    '-preco': '-preco',
    '-created_at': '-created_at',
    'created_at': 'created_at',
}


@staff_required
def produto_lista(request, vendidos=False):
    busca = request.GET.get('q', '').strip()
    ordenar = request.GET.get('ordenar', '-created_at')
    if ordenar not in ORDENACOES_PRODUTO:
        ordenar = '-created_at'

    produtos = Produto.objects.select_related('categoria').prefetch_related('imagens').filter(vendido=vendidos)
    if busca:
        produtos = produtos.filter(nome__icontains=busca)
    produtos = produtos.order_by(ORDENACOES_PRODUTO[ordenar])

    return render(request, 'loja/painel/produto_lista.html', {
        'produtos': produtos,
        'total_produtos': Produto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_disponiveis': Produto.objects.filter(vendido=False).count(),
        'produtos_vendidos': Produto.objects.filter(vendido=True).count(),
        'busca': busca,
        'ordenar': ordenar,
        'mostrando_vendidos': vendidos,
    })


@staff_required
def produto_form(request, pk=None):
    produto = get_object_or_404(Produto, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        formset = ImagemProdutoFormSet(request.POST, request.FILES, instance=produto or Produto())
        if form.is_valid() and formset.is_valid():
            produto = form.save()
            formset.instance = produto
            formset.save()
            messages.success(request, 'Produto salvo com sucesso.')
            return redirect('painel:produto_lista')
    else:
        form = ProdutoForm(instance=produto)
        formset = ImagemProdutoFormSet(instance=produto)
    return render(request, 'loja/painel/produto_form.html', {
        'form': form, 'formset': formset, 'produto': produto,
    })


@staff_required
@require_POST
def produto_toggle_vendido(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.vendido = not produto.vendido
    produto.save(update_fields=['vendido'])
    if produto.vendido:
        messages.success(request, f'"{produto.nome}" marcado como vendido.')
    else:
        messages.success(request, f'"{produto.nome}" marcado como disponível.')

    next_url = request.POST.get('next')
    if next_url and next_url.startswith('/'):
        return redirect(next_url)
    return redirect('painel:produto_lista')


@staff_required
def produto_excluir(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído.')
        return redirect('painel:produto_lista')
    return render(request, 'loja/painel/produto_confirmar_exclusao.html', {'produto': produto})
