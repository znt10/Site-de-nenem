# Panos & Cia

Site simples para divulgar e vender panos (chão, pia, mesa e cama). Os pedidos são feitos pelo WhatsApp.

## Como rodar o site

```
.\venv\Scripts\activate
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/** no navegador.

## Painel administrativo

Acesse **http://127.0.0.1:8000/admin/** e entre com o e-mail e senha do superusuário.

### Cadastrar um produto

1. No painel, clique em **Produtos** > **Adicionar Produto**.
2. Preencha nome, categoria, descrição (opcional) e preço.
3. Marque **Destaque** para aparecer na seção de destaques da página inicial.
4. Marque **Ativo** para o produto ficar visível no site.
5. Em **Imagens do Produto**, envie uma ou mais fotos.
6. Clique em **Salvar**.

### Editar ou apagar um produto

1. Vá em **Produtos** e clique no nome do produto.
2. Altere o que precisar e clique em **Salvar**.
3. Para apagar, marque a caixinha ao lado do produto na lista e escolha **Excluir**.

### Gerenciar categorias

1. No painel, clique em **Categorias**.
2. Para criar uma nova, clique em **Adicionar Categoria** e digite o nome.
3. Para editar ou apagar, clique na categoria desejada.

> ⚠️ Não é possível apagar uma categoria que ainda tem produtos cadastrados nela.

## Como o cliente faz o pedido

O cliente navega pelo site, clica em **"Pedir no WhatsApp"** no produto desejado e é redirecionado para o WhatsApp com uma mensagem pronta contendo o nome, preço e link do produto.

## Configurações

No arquivo `.env` você pode alterar:

- `WHATSAPP_NUMERO` — número que recebe os pedidos (formato: DDI+DDD+número, ex: `5500000000000`)
- `NOME_LOJA` — nome que aparece no site

Depois de alterar, reinicie o site.

## Favicon

O ícone da aba do navegador fica em `static/img/favicon.ico`. Para trocar, substitua esse arquivo por outro `.ico` com o mesmo nome.
