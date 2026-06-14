from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory

from .models import Categoria, ImagemProduto, Produto

INPUT_CLASSES = (
    'w-full rounded-full border border-brand-200 bg-white py-2 px-4 text-sm '
    'focus:outline-none focus:ring-2 focus:ring-brand-400 transition'
)
SELECT_CLASSES = (
    'w-full rounded-2xl border border-brand-200 bg-white py-2 px-4 text-sm '
    'focus:outline-none focus:ring-2 focus:ring-brand-400 transition'
)
TEXTAREA_CLASSES = (
    'w-full rounded-2xl border border-brand-200 bg-white py-2 px-4 text-sm '
    'focus:outline-none focus:ring-2 focus:ring-brand-400 transition'
)
CHECKBOX_CLASSES = 'h-5 w-5 rounded text-brand-500 focus:ring-brand-400'


class PainelLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': INPUT_CLASSES, 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES}))


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Nome da categoria'}),
        }


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'descricao', 'preco', 'destaque', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'categoria': forms.Select(attrs={'class': SELECT_CLASSES}),
            'descricao': forms.Textarea(attrs={'class': TEXTAREA_CLASSES, 'rows': 4}),
            'preco': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01', 'min': '0'}),
            'destaque': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
            'ativo': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
        }


ImagemProdutoFormSet = inlineformset_factory(
    Produto,
    ImagemProduto,
    fields=['imagem'],
    extra=3,
    can_delete=True,
    widgets={
        'imagem': forms.ClearableFileInput(attrs={'class': 'block w-full text-sm text-brand-700'}),
    },
)
