import os

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .imaging import optimize_to_webp


class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Produto(models.Model):
    nome = models.CharField('Nome', max_length=150)
    slug = models.SlugField('Slug', max_length=160, unique=True, blank=True)
    descricao = models.TextField('Descrição', blank=True)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria, related_name='produtos', on_delete=models.PROTECT, verbose_name='Categoria'
    )
    destaque = models.BooleanField('Produto em destaque', default=False)
    ativo = models.BooleanField('Ativo', default=True)
    vendido = models.BooleanField('Vendido', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            count = 1
            while Produto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                count += 1
                slug = f'{base_slug}-{count}'
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('loja:produto_detalhe', kwargs={'slug': self.slug})

    @property
    def imagem_principal(self):
        primeira = self.imagens.first()
        return primeira.imagem if primeira else None


class CaracteristicaProduto(models.Model):
    SECAO_CHOICES = [
        ('principal', 'Características principais'),
        ('venda', 'Características de venda'),
    ]
    produto = models.ForeignKey(
        Produto, related_name='caracteristicas', on_delete=models.CASCADE, verbose_name='Produto'
    )
    chave = models.CharField('Nome', max_length=100)
    valor = models.CharField('Valor', max_length=200, blank=True)
    secao = models.CharField('Seção', max_length=20, choices=SECAO_CHOICES, default='principal')
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Característica do Produto'
        verbose_name_plural = 'Características do Produto'
        ordering = ['secao', 'ordem', 'id']

    def __str__(self):
        return f'{self.chave}: {self.valor}'


class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name='imagens', on_delete=models.CASCADE, verbose_name='Produto')
    imagem = models.ImageField('Imagem', upload_to='produtos/')
    ordem = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens do Produto'
        ordering = ['ordem', 'id']

    def __str__(self):
        return f'Imagem de {self.produto.nome}'

    def save(self, *args, **kwargs):
        # Otimiza só quando há upload novo (_committed=False = arquivo ainda
        # não gravado no storage), evitando baixar/reprocessar o que já está
        # no MinIO a cada save.
        if self.imagem and not self.imagem._committed:
            try:
                webp = optimize_to_webp(self.imagem)
                base = os.path.splitext(os.path.basename(self.imagem.name))[0] + '.webp'
                # save=False: grava o WebP no storage sem salvar o model ainda;
                # o super().save() abaixo persiste a linha. Assim o original
                # nunca chega ao MinIO — só a versão otimizada.
                self.imagem.save(base, ContentFile(webp), save=False)
            except Exception:
                # Falha na otimização não pode perder a imagem: segue o fluxo
                # normal e grava o original.
                pass
        super().save(*args, **kwargs)
