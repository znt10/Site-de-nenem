"""
URL configuration for panoslar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('painel/', include('loja.painel_urls')),
    path('', include('loja.urls')),
]

# Admin do Django só fica disponível em desenvolvimento (DEBUG=True).
# Em produção o gerenciamento é feito pelo painel próprio (/painel/).
if settings.DEBUG:
    urlpatterns = [path('admin/', admin.site.urls)] + urlpatterns

# Serve os arquivos de media (fotos dos produtos) localmente, tanto em
# desenvolvimento quanto em produção sem MinIO. static() do Django só
# funciona com DEBUG=True, por isso usamos a view serve diretamente.
# Quando MEDIA_URL aponta para um host externo (MinIO), essa rota nunca é usada.
if '://' not in settings.MEDIA_URL:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

