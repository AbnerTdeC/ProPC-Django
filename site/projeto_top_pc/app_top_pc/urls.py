from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('suporte/', views.suporte, name='suporte'),
    path('contato/', views.contato, name='contato'),
    path('cadastrar-componente/', views.cadastrar_componente, name='cadastrar_componente'),
    path('editar-componente/<int:id>/', views.editar_componente, name='editar_componente'),
    path('remover-componente/<int:id>/', views.remover_componente, name='remover_componente'),
    path('cadastrar-componente-configurador/', views.cadastrar_componente_configurador, name='cadastrar_componente_configurador'),
    path('editar-componente-configurador/<int:id>/', views.editar_componente_configurador, name='editar_componente_configurador'),
    path('remover-componente-configurador/<int:id>/', views.remover_componente_configurador, name='remover_componente_configurador'),
    path('cadastrar-produto-catalogo/', views.cadastrar_produto_catalogo, name='cadastrar_produto_catalogo'),
    path('editar-produto-catalogo/<int:id>/', views.editar_produto_catalogo, name='editar_produto_catalogo'),
    path('remover-produto-catalogo/<int:id>/', views.remover_produto_catalogo, name='remover_produto_catalogo'),
    path('configurador/', views.configurador, name='configurador'),
    path('listar-processadores/', views.listar_processadores, name='listar_processadores'),
    path('listar-placas-video/', views.listar_placas_video, name='listar_placas_video'),
    path('listar-memorias/', views.listar_memorias, name='listar_memorias'),
    path('listar-placas-mae/', views.listar_placas_mae, name='listar_placas_mae'),
    path('listar-armazenamento/', views.listar_armazenamento, name='listar_armazenamento'),
    path('listar-fontes/', views.listar_fontes, name='listar_fontes'),
    path('listar-gabinetes/', views.listar_gabinetes, name='listar_gabinetes'),
    path('listar-coolers-cpu/', views.listar_coolers_cpu, name='listar_coolers_cpu'),
    path('listar-componentes-configurador/', views.listar_componentes_configurador, name='listar_componentes_configurador'),
    path('listar-perifericos/', views.listar_perifericos, name='listar_perifericos'),
    path('listar-placas-expansao/', views.listar_placas_expansao, name='listar_placas_expansao'),
    path('listar-case-fan/', views.listar_case_fan, name='listar_case_fan'),
    path('listar-sound-card/', views.listar_sound_card, name='listar_sound_card'),
    path('listar-wired-network-card/', views.listar_wired_network_card, name='listar_wired_network_card'),
    path('listar-wireless-network-card/', views.listar_wireless_network_card, name='listar_wireless_network_card'),
    path('listar-optical-drive/', views.listar_optical_drive, name='listar_optical_drive'),
    path('listar-monitor/', views.listar_monitor, name='listar_monitor'),
    path('listar-keyboard/', views.listar_keyboard, name='listar_keyboard'),
    path('listar-mouse/', views.listar_mouse, name='listar_mouse'),
    path('listar-speakers/', views.listar_speakers, name='listar_speakers'),
    path('listar-headphones/', views.listar_headphones, name='listar_headphones'),
]
