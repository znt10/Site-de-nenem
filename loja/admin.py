from admin_interface.models import Theme
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html

from .models import Categoria, ImagemProduto, Produto

admin.site.site_header = 'Panos & Cia'
admin.site.site_title = 'Panos & Cia Admin'
admin.site.index_title = 'Painel Administrativo'

# Deixa o admin enxuto: somente Categorias e Produtos aparecem no menu
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.unregister(Theme)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'total_produtos')
    exclude = ('slug',)
    search_fields = ('nome',)

    @admin.display(description='Produtos cadastrados')
    def total_produtos(self, obj):
        return obj.produtos.count()


class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1
    fields = ('imagem', 'preview', 'ordem')
    readonly_fields = ('preview',)

    @admin.display(description='Pré-visualização')
    def preview(self, obj):
        if obj.pk and obj.imagem:
            return format_html(
                '<img src="{}" style="height:70px; border-radius:8px; object-fit:cover;" />',
                obj.imagem.url,
            )
        return '—'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'nome', 'categoria', 'preco_formatado', 'destaque', 'ativo', 'created_at')
    list_filter = ('categoria', 'destaque', 'ativo')
    search_fields = ('nome', 'descricao')
    list_editable = ('destaque', 'ativo')
    inlines = [ImagemProdutoInline]
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Informações do produto', {
            'fields': ('nome', 'categoria', 'descricao', 'preco')
        }),
        ('Visibilidade', {
            'fields': ('destaque', 'ativo')
        }),
    )

    @admin.display(description='Foto')
    def thumbnail(self, obj):
        imagem = obj.imagem_principal
        if imagem:
            return format_html(
                '<img src="{}" style="height:50px; width:50px; object-fit:cover; border-radius:8px;" />',
                imagem.url,
            )
        return '—'

    @admin.display(description='Preço', ordering='preco')
    def preco_formatado(self, obj):
        return f'R$ {obj.preco:.2f}'.replace('.', ',')
