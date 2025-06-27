from django.contrib import admin
from django.urls import path, include  # Não se esqueça de importar 'include'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Abaixo, estamos incluindo as URLs do seu aplicativo 'app_top_pc'.
    # Você pode escolher um "prefixo" para essas URLs. Por exemplo, se usar 'app/',
    # todas as URLs do seu app_top_pc serão acessadas via http://127.0.0.1:8000/app/...
    # Se você quer que a página inicial do seu app_top_pc seja a página inicial do site
    # (http://127.0.0.1:8000/), você pode usar '' como prefixo.

    # Opção 1: Incluir com um prefixo (ex: 'aplicativo/')
    # As URLs do app_top_pc serão acessadas como:
    # /aplicativo/ -> home do app
    # /aplicativo/componente/adicionar/ -> adicionar_componente do app
    path('', include('app_top_pc.urls')), # Use um caminho vazio '' como prefixo

    # Opção 2: Incluir na raiz do site (sem prefixo)
    # A home do app_top_pc será a home do site (http://127.0.0.1:8000/)
    # As URLs do app_top_pc serão acessadas como:
    # / -> home do app
    # /componente/adicionar/ -> adicionar_componente do app
    # Se escolher esta opção, comente ou remova a Opção 1 acima.
    # path('', include('app_top_pc.urls')),

    # Você pode adicionar outras URLs de outros aplicativos ou URLs de nível de projeto aqui.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
