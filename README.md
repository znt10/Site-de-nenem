# Panos & Cia — Guia Rápido

Site simples para divulgar e vender panos (chão, pia, mesa e cama). Os pedidos são feitos pelo WhatsApp.

## Como acessar o painel administrativo

1. Abra o navegador e acesse: **http://127.0.0.1:8000/admin/**
   *(se o site estiver online, troque pelo endereço do site + `/admin/`)*
2. Entre com:
   - **E-mail:** admin@gmail.com
   - **Senha:** admin123

## Como cadastrar um produto

1. No painel, clique em **Produtos**.
2. Clique no botão **Adicionar Produto** (canto superior direito).
3. Preencha:
   - **Nome**: ex. "Pano de Mesa Floral"
   - **Categoria**: escolha entre Pano de Chão, Pia, Mesa ou Cama
   - **Descrição**: detalhes do produto (opcional)
   - **Preço**: ex. 25.90
4. Marque **Destaque** se quiser que o produto apareça na seção "Produtos em Destaque" da página inicial.
5. Marque **Ativo** para o produto aparecer no site (desmarque para escondê-lo sem apagar).
6. Role a página até **Imagens do Produto** e clique em **Escolher arquivo** para enviar uma ou mais fotos.
7. Clique em **Salvar**.

Pronto! O produto já aparece no site automaticamente.

## Como editar ou apagar um produto

1. Vá em **Produtos** e clique no nome do produto desejado.
2. Altere o que precisar e clique em **Salvar**.
3. Para apagar, marque a caixinha ao lado do produto na lista e escolha **Excluir** no menu de ações.

## Como gerenciar categorias

1. No painel, clique em **Categorias**.
2. Para criar uma nova, clique em **Adicionar Categoria** e digite o nome.
3. Para editar ou apagar, clique na categoria desejada.

> ⚠️ Não é possível apagar uma categoria que ainda tem produtos cadastrados nela.

## Como o cliente faz o pedido

O cliente navega pelo site, clica em **"Pedir no WhatsApp"** no produto desejado, e é redirecionado para o WhatsApp com uma mensagem pronta contendo o nome, preço e link do produto.

## Como rodar o site no computador

```
.\venv\Scripts\activate
python manage.py runserver
```

Depois acesse **http://127.0.0.1:8000/** no navegador.

## Configurações úteis

No arquivo `.env` (ou `panoslar/settings.py`) você pode alterar:

- `WHATSAPP_NUMERO`: número de WhatsApp que recebe os pedidos (formato: DDI+DDD+número, ex: 5583982217869)
- `NOME_LOJA`: nome que aparece no site

Depois de alterar, é só reiniciar o site.

## Como trocar o ícone do site (favicon)

O ícone que aparece na aba do navegador fica em `static/img/favicon.ico`. Para trocar, basta substituir esse arquivo por outro `.ico` com o mesmo nome (`favicon.ico`).

## Deploy no Railway

1. Suba o projeto para um repositório no GitHub (o `.gitignore` já evita subir `venv/`, `db.sqlite3`, `media/` e `.env`).
2. No Railway, clique em **New Project > Deploy from GitHub repo** e selecione o repositório. O Railway detecta o `Dockerfile` automaticamente.
3. Adicione um **Volume** ao serviço (aba *Volumes*), com mount path `/data`. É nele que ficam as fotos enviadas (e o banco SQLite, caso não use MySQL) — sem isso, tudo se perde a cada novo deploy.
4. Em **Variables**, configure:
   - `SECRET_KEY` → gere uma chave nova (ex: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG=False`
   - `DATA_DIR=/data`
   - `WHATSAPP_NUMERO=5583982217869`
   - `NOME_LOJA=Panos & Cia`
   - `DJANGO_SUPERUSER_EMAIL=admin@gmail.com`
   - `DJANGO_SUPERUSER_PASSWORD=admin123`
   - `ALLOWED_HOSTS=localhost,127.0.0.1` (ajuste no passo 6)

   ### Usando o MySQL do Railway
   Adicione o plugin **MySQL** ao projeto (New > Database > Add MySQL) e clique em **Variables > Add Variable Reference** no serviço web para importar do MySQL: `MYSQLHOST`, `MYSQLPORT`, `MYSQLDATABASE`, `MYSQLUSER`, `MYSQLPASSWORD`. O `settings.py` detecta essas variáveis automaticamente e passa a usar MySQL no lugar do SQLite — não precisa mudar nada no código.
5. Faça o deploy e, em **Settings > Networking**, clique em **Generate Domain**. Você receberá algo como `panos-cia.up.railway.app`.
6. Volte em **Variables** e atualize `ALLOWED_HOSTS` incluindo esse domínio:
   ```
   ALLOWED_HOSTS=panos-cia.up.railway.app,localhost,127.0.0.1
   ```
7. O Railway reinicia automaticamente. Acesse `https://panos-cia.up.railway.app/admin/` para confirmar que o login funciona.

> O `entrypoint.sh` já roda as migrations, coleta os arquivos estáticos e cria o superusuário automaticamente a cada deploy.
