from django.conf import settings

from .models import Categoria


def configuracoes_loja(request):
    return {
        'WHATSAPP_NUMERO': settings.WHATSAPP_NUMERO,
        'NOME_LOJA': settings.NOME_LOJA,
        'categorias_footer': Categoria.objects.all(),
    }
