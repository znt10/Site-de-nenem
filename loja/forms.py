from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Categoria, CaracteristicaProduto, ImagemProduto, Produto

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


class PainelLoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASSES, 'autofocus': True}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        password = self.cleaned_data.get('password')
        if password:
            staff = User.objects.filter(is_staff=True).first()
            if staff:
                self.user_cache = authenticate(
                    self.request, username=staff.username, password=password,
                )
            if self.user_cache is None:
                raise forms.ValidationError('Senha incorreta.')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


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
        fields = ['nome', 'categoria', 'descricao', 'preco', 'destaque', 'ativo', 'vendido']
        widgets = {
            'nome': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'categoria': forms.Select(attrs={'class': SELECT_CLASSES}),
            'descricao': forms.Textarea(attrs={'class': TEXTAREA_CLASSES, 'rows': 4}),
            'preco': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01', 'min': '0'}),
            'destaque': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
            'ativo': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
            'vendido': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
        }


CARAC_INICIAIS = [
    {'chave': 'Marca',            'secao': 'principal', 'valor': ''},
    {'chave': 'Cor',              'secao': 'principal', 'valor': ''},
    {'chave': 'Modelo',           'secao': 'principal', 'valor': ''},
    {'chave': 'Linha',            'secao': 'principal', 'valor': ''},
    {'chave': 'Comprimento',      'secao': 'principal', 'valor': ''},
    {'chave': 'Largura',          'secao': 'principal', 'valor': ''},
    {'chave': 'Diâmetro',         'secao': 'principal', 'valor': ''},
    {'chave': 'Formato de venda', 'secao': 'venda',     'valor': ''},
    {'chave': 'Unidades por kit', 'secao': 'venda',     'valor': ''},
]

CaracteristicaFormSet = inlineformset_factory(
    Produto,
    CaracteristicaProduto,
    fields=['chave', 'valor', 'secao'],
    extra=0,
    can_delete=True,
    widgets={
        'chave': forms.TextInput(attrs={
            'class': 'carac-input w-full rounded-lg border border-brand-200 bg-white py-1.5 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400 transition',
            'placeholder': 'Ex: Material',
        }),
        'valor': forms.TextInput(attrs={
            'class': 'carac-input w-full rounded-lg border border-brand-200 bg-white py-1.5 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400 transition',
            'placeholder': 'Ex: Crochê',
        }),
        'secao': forms.Select(attrs={
            'class': 'carac-secao rounded-lg border border-brand-200 bg-white py-1.5 px-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-400 transition',
        }),
    },
)

ImagemProdutoFormSet = inlineformset_factory(
    Produto,
    ImagemProduto,
    fields=['imagem'],
    extra=0,
    can_delete=True,
    widgets={
        'imagem': forms.ClearableFileInput(attrs={'class': 'imagem-input block w-full text-sm text-brand-700'}),
    },
)
