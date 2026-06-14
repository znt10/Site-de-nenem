from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import staff_required
from .forms import CategoriaForm, ImagemProdutoFormSet, PainelLoginForm, ProdutoForm
from .models import Categoria, Produto


class PainelLoginView(LoginView):
    template_name = 'loja/painel/login.html'
    authentication_form = PainelLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            form.add_error(None, 'Esta conta não tem acesso ao painel.')
            return self.form_invalid(form)
        return super().form_valid(form)


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

@staff_required
def produto_lista(request):
    produtos = Produto.objects.select_related('categoria').prefetch_related('imagens')
    return render(request, 'loja/painel/produto_lista.html', {
        'produtos': produtos,
        'total_produtos': Produto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'produtos_inativos': Produto.objects.filter(ativo=False).count(),
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
def produto_excluir(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído.')
        return redirect('painel:produto_lista')
    return render(request, 'loja/painel/produto_confirmar_exclusao.html', {'produto': produto})
