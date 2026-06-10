import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import ImagemProduto


@receiver(post_delete, sender=ImagemProduto)
def apagar_arquivo_ao_excluir(sender, instance, **kwargs):
    """Remove o arquivo de imagem do disco quando o registro é excluído
    (também dispara quando o produto é excluído, por causa do CASCADE)."""
    if instance.imagem and os.path.isfile(instance.imagem.path):
        os.remove(instance.imagem.path)


@receiver(pre_save, sender=ImagemProduto)
def apagar_arquivo_antigo_ao_trocar(sender, instance, **kwargs):
    """Remove o arquivo antigo do disco quando a imagem é substituída."""
    if not instance.pk:
        return

    try:
        antiga = ImagemProduto.objects.get(pk=instance.pk)
    except ImagemProduto.DoesNotExist:
        return

    arquivo_antigo = antiga.imagem
    arquivo_novo = instance.imagem
    if arquivo_antigo and arquivo_antigo != arquivo_novo and os.path.isfile(arquivo_antigo.path):
        os.remove(arquivo_antigo.path)
