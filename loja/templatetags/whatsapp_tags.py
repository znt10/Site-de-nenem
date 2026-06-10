from urllib.parse import quote

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def whatsapp_link_produto(produto, request=None):
    site_url = ''
    if request is not None:
        site_url = request.build_absolute_uri(produto.get_absolute_url())

    mensagem = (
        f'Olá! Tenho interesse no produto:\n\n'
        f'• {produto.nome} - R$ {produto.preco:.2f}'.replace('.', ',')
    )
    if site_url:
        mensagem += f'\n\n{site_url}'
    mensagem += '\n\nGostaria de mais informações.'

    return f'https://wa.me/{settings.WHATSAPP_NUMERO}?text={quote(mensagem)}'


@register.simple_tag
def whatsapp_link_geral(request=None):
    mensagem = 'Olá! Gostaria de saber mais sobre os produtos da loja.'
    if request is not None:
        site_url = request.build_absolute_uri('/')
        mensagem += f'\n\n{site_url}'
    return f'https://wa.me/{settings.WHATSAPP_NUMERO}?text={quote(mensagem)}'
