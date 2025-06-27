from django.urls import path
from . import views  # Garante que suas views estão sendo importadas do local correto

app_name = 'app_top_pc'  # Define o namespace do aplicativo

urlpatterns = [
    # URL para a página inicial do seu aplicativo
    path('', views.home, name='home'),
    
    # URLs para as funcionalidades de Componente
    path('componente/adicionar/', views.cadastrar_componente, name='adicionar_componente'),
    path('componente/editar/<int:id>/', views.editar_componente, name='editar_componente'),
    path('componente/remover/<int:id>/', views.remover_componente, name='remover_componente'),

    # URL para a página de catálogo
    path('catalogo/', views.catalogo, name='catalogo'),

    path('configurador/', views.configurador, name='configurador'),
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('suporte/', views.suporte, name='suporte'),
    path('contato/', views.contato, name='contato'),
]
