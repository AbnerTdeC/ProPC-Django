from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from .forms import ComponenteForm, ComponenteConfiguradorBaseForm, ProdutoCatalogoForm

@csrf_exempt
def configurador(request):
    # Define all component categories
    categorias = [
        'cpu', 'cpu-cooler', 'motherboard', 'memory', 
        'internal-hard-drive', 'video-card', 'power-supply', 'case',
        'case-fan', 'sound-card', 'wired-network-card', 'wireless-network-card',
        'optical-drive', 'monitor', 'keyboard', 'mouse', 'speakers', 'headphones',
        'hardware'
    ]
    
    # Fetch all active components from the configurator database
    componentes = ComponenteConfiguradorBase.objects.filter(ativo=True)
    componentes_por_categoria = defaultdict(list)
    for componente in componentes:
        # Convert to a dictionary to maintain a consistent structure
        componentes_por_categoria[componente.tipo_componente].append({
            'id': componente.id,
            'nome': componente.nome,
            'descricao': componente.descricao,
            'especificacoes': componente.especificacoes,
            'imagem': componente.imagem.url if componente.imagem else ''
        })

    context = {
        'categorias': categorias,
        'componentes_por_categoria': dict(componentes_por_categoria),
    }

    if request.method == 'POST':
        selecionados = {}
        for categoria in categorias:
            componente_id = request.POST.get(f'categoria_{categoria}')
            if componente_id:
                try:
                    # Fetch the selected component from the database
                    componente = ComponenteConfiguradorBase.objects.get(id=componente_id)
                    selecionados[categoria] = {
                        'id': componente.id,
                        'nome': componente.nome,
                        'descricao': componente.descricao,
                        'especificacoes': componente.especificacoes,
                        'imagem': componente.imagem.url if componente.imagem else ''
                    }
                except ComponenteConfiguradorBase.DoesNotExist:
                    # Handle case where the component ID is invalid
                    pass
        context['selecionados'] = selecionados
        return render(request, 'app_top_pc/configurador.html', context)
    else:
        return render(request, 'app_top_pc/configurador.html', context)

def home(request):
    produtos = Produto.objects.all()
    
    produtos_por_tipo = defaultdict(list)
    for produto in produtos:
        produtos_por_tipo[produto.categoria.nome].append(produto)

    context = {
        "produtos": produtos_por_tipo,
    }

    return render(request, "app_top_pc/index.html", context)

def catalogo(request):
    # Usar o novo modelo ProdutoCatalogo para o catálogo
    produtos_catalogo = ProdutoCatalogo.objects.all().order_by('-data_atualizacao')
    context = {
        'produtos': produtos_catalogo,
    }
    return render(request, 'app_top_pc/catalogo.html', context)

def sobre_nos(request):
    return render(request, 'app_top_pc/sobre_nos.html')

def suporte(request):
    return render(request, 'app_top_pc/suporte.html')

def contato(request):
    return render(request, 'app_top_pc/contato.html')

def cadastrar_componente(request):
    if request.method == 'POST':
        form = ComponenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ComponenteForm()
    return render(request, 'app_top_pc/cadastrar_componente.html', {'form': form})

def editar_componente(request, id):
    componente = get_object_or_404(Componente, pk=id)
    if request.method == 'POST':
        form = ComponenteForm(request.POST, request.FILES, instance=componente)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ComponenteForm(instance=componente)
    return render(request, 'app_top_pc/editar_componente.html', {'form': form, 'componente': componente})

def remover_componente(request, id):
    componente = get_object_or_404(Componente, pk=id)
    if request.method == 'POST':
        componente.delete()
        return redirect('home')
    return render(request, 'app_top_pc/remover_componente.html', {'componente': componente})

# Novas views para gerenciar componentes do configurador
def cadastrar_componente_configurador(request):
    if request.method == 'POST':
        form = ComponenteConfiguradorBaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('configurador')
    else:
        form = ComponenteConfiguradorBaseForm()
    return render(request, 'app_top_pc/cadastrar_componente_configurador.html', {'form': form})

def editar_componente_configurador(request, id):
    componente = get_object_or_404(ComponenteConfiguradorBase, pk=id)
    if request.method == 'POST':
        form = ComponenteConfiguradorBaseForm(request.POST, request.FILES, instance=componente)
        if form.is_valid():
            form.save()
            return redirect('configurador')
    else:
        form = ComponenteConfiguradorBaseForm(instance=componente)
    return render(request, 'app_top_pc/editar_componente_configurador.html', {'form': form, 'componente': componente})

def remover_componente_configurador(request, id):
    componente = get_object_or_404(ComponenteConfiguradorBase, pk=id)
    if request.method == 'POST':
        componente.delete()
        return redirect('configurador')
    return render(request, 'app_top_pc/remover_componente_configurador.html', {'componente': componente})

# Novas views para gerenciar produtos do catálogo
def cadastrar_produto_catalogo(request):
    if request.method == 'POST':
        form = ProdutoCatalogoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalogo')
    else:
        form = ProdutoCatalogoForm()
    return render(request, 'app_top_pc/cadastrar_produto_catalogo.html', {'form': form})

def editar_produto_catalogo(request, id):
    produto = get_object_or_404(ProdutoCatalogo, pk=id)
    if request.method == 'POST':
        form = ProdutoCatalogoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('catalogo')
    else:
        form = ProdutoCatalogoForm(instance=produto)
    return render(request, 'app_top_pc/editar_produto_catalogo.html', {'form': form, 'produto': produto})

def remover_produto_catalogo(request, id):
    produto = get_object_or_404(ProdutoCatalogo, pk=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('catalogo')
    return render(request, 'app_top_pc/remover_produto_catalogo.html', {'produto': produto})

# View para listar processadores
def listar_processadores(request):
    processadores = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='cpu',
        ativo=True
    ).order_by('nome')
    
    context = {
        'processadores': processadores,
    }
    return render(request, 'app_top_pc/componentes/processadores.html', context)

# Views para outras categorias de componentes
def listar_placas_video(request):
    placas_video = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='video-card',
        ativo=True
    ).order_by('nome')
    
    context = {
        'placas_video': placas_video,
    }
    return render(request, 'app_top_pc/componentes/placas_video.html', context)

def listar_memorias(request):
    memorias = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='memory',
        ativo=True
    ).order_by('nome')
    
    context = {
        'memorias': memorias,
    }
    return render(request, 'app_top_pc/componentes/memorias.html', context)

def listar_placas_mae(request):
    placas_mae = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='motherboard',
        ativo=True
    ).order_by('nome')
    
    context = {
        'placas_mae': placas_mae,
    }
    return render(request, 'app_top_pc/componentes/placas_mae.html', context)

def listar_armazenamento(request):
    armazenamento = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='internal-hard-drive',
        ativo=True
    ).order_by('nome')
    
    context = {
        'armazenamento': armazenamento,
    }
    return render(request, 'app_top_pc/componentes/armazenamento.html', context)

def listar_fontes(request):
    fontes = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='power-supply',
        ativo=True
    ).order_by('nome')
    
    context = {
        'fontes': fontes,
    }
    return render(request, 'app_top_pc/componentes/fontes.html', context)

def listar_gabinetes(request):
    gabinetes = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='case',
        ativo=True
    ).order_by('nome')
    
    context = {
        'gabinetes': gabinetes,
    }
    return render(request, 'app_top_pc/componentes/gabinetes.html', context)

def listar_coolers_cpu(request):
    coolers_cpu = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='cpu-cooler',
        ativo=True
    ).order_by('nome')
    
    context = {
        'coolers_cpu': coolers_cpu,
    }
    return render(request, 'app_top_pc/componentes/coolers_cpu.html', context)

# View para listar componentes do configurador (admin)
def listar_componentes_configurador(request):
    componentes = ComponenteConfiguradorBase.objects.all().order_by('tipo_componente', 'nome')
    context = {
        'componentes': componentes,
    }
    return render(request, 'app_top_pc/listar_componentes_configurador.html', context)

def listar_perifericos(request):
    perifericos = ComponenteConfiguradorBase.objects.filter(
        tipo_componente__in=['monitor', 'keyboard', 'mouse', 'speakers', 'headphones'],
        ativo=True
    ).order_by('nome')

    context = {
        'perifericos': perifericos,
    }
    return render(request, 'app_top_pc/componentes/perifericos.html', context)

def listar_placas_expansao(request):
    placas_expansao = ComponenteConfiguradorBase.objects.filter(
        tipo_componente__in=['sound-card', 'wired-network-card', 'wireless-network-card', 'optical-drive'],
        ativo=True
    ).order_by('nome')

    context = {
        'placas_expansao': placas_expansao,
    }
    return render(request, 'app_top_pc/componentes/placas_expansao.html', context)

def listar_case_fan(request):
    case_fans = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='case-fan',
        ativo=True
    ).order_by('nome')

    context = {
        'case_fans': case_fans,
    }
    return render(request, 'app_top_pc/componentes/case_fan.html', context)

def listar_sound_card(request):
    sound_cards = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='sound-card',
        ativo=True
    ).order_by('nome')

    context = {
        'sound_cards': sound_cards,
    }
    return render(request, 'app_top_pc/componentes/sound_card.html', context)

def listar_wired_network_card(request):
    wired_network_cards = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='wired-network-card',
        ativo=True
    ).order_by('nome')

    context = {
        'wired_network_cards': wired_network_cards,
    }
    return render(request, 'app_top_pc/componentes/wired_network_card.html', context)

def listar_wireless_network_card(request):
    wireless_network_cards = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='wireless-network-card',
        ativo=True
    ).order_by('nome')

    context = {
        'wireless_network_cards': wireless_network_cards,
    }
    return render(request, 'app_top_pc/componentes/wireless_network_card.html', context)

def listar_optical_drive(request):
    optical_drives = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='optical-drive',
        ativo=True
    ).order_by('nome')

    context = {
        'optical_drives': optical_drives,
    }
    return render(request, 'app_top_pc/componentes/optical_drive.html', context)

def listar_monitor(request):
    monitors = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='monitor',
        ativo=True
    ).order_by('nome')

    context = {
        'monitors': monitors,
    }
    return render(request, 'app_top_pc/componentes/monitor.html', context)

def listar_keyboard(request):
    keyboards = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='keyboard',
        ativo=True
    ).order_by('nome')

    context = {
        'keyboards': keyboards,
    }
    return render(request, 'app_top_pc/componentes/keyboard.html', context)

def listar_mouse(request):
    mice = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='mouse',
        ativo=True
    ).order_by('nome')

    context = {
        'mice': mice,
    }
    return render(request, 'app_top_pc/componentes/mouse.html', context)

def listar_speakers(request):
    speakers = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='speakers',
        ativo=True
    ).order_by('nome')

    context = {
        'speakers': speakers,
    }
    return render(request, 'app_top_pc/componentes/speakers.html', context)

def listar_headphones(request):
    headphones = ComponenteConfiguradorBase.objects.filter(
        tipo_componente='headphones',
        ativo=True
    ).order_by('nome')

    context = {
        'headphones': headphones,
    }
    return render(request, 'app_top_pc/componentes/headphones.html', context)

