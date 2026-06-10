from django.db import models
from django.urls import reverse
from django.utils.text import slugify


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
