from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pcpartpicker import API
from .models import *
from .forms import ComponenteForm

@csrf_exempt
def configurador(request):
    import time
    
    # Define categorias principais de PC - priorizadas por importância
    categorias_principais = [
        'cpu', 'cpu-cooler', 'motherboard', 'memory', 
        'internal-hard-drive', 'video-card', 'power-supply', 'case'
    ]
    
    categorias_extras = [
        'case-fan', 'sound-card', 'wired-network-card', 'wireless-network-card',
        'optical-drive', 'monitor', 'keyboard', 'mouse', 'speakers', 'headphones'
    ]
    
    categorias = categorias_principais + categorias_extras
    produtos_por_categoria = {}

    # Sistema híbrido: API para categorias principais, mock para extras
    use_api_for_main = True  # Temporariamente desabilitado devido a problemas de asyncio
    timeout_seconds = 30  # Timeout total para evitar travamento
    
    # Dados mock para todas as categorias (usado como fallback)
    mock_data = {
        'cpu': [
            {'id': 'intel-i5-12400f', 'nome': 'Intel Core i5-12400F'},
            {'id': 'amd-ryzen-5-5600x', 'nome': 'AMD Ryzen 5 5600X'},
            {'id': 'intel-i7-12700k', 'nome': 'Intel Core i7-12700K'},
            {'id': 'amd-ryzen-7-5800x', 'nome': 'AMD Ryzen 7 5800X'},
            {'id': 'intel-i9-12900k', 'nome': 'Intel Core i9-12900K'},
            {'id': 'amd-ryzen-9-5900x', 'nome': 'AMD Ryzen 9 5900X'},
            {'id': 'intel-i5-13600k', 'nome': 'Intel Core i5-13600K'},
            {'id': 'amd-ryzen-7-7700x', 'nome': 'AMD Ryzen 7 7700X'},
            {'id': 'intel-i7-13700k', 'nome': 'Intel Core i7-13700K'},
            {'id': 'amd-ryzen-9-7900x', 'nome': 'AMD Ryzen 9 7900X'},
            {'id': 'intel-i3-12100f', 'nome': 'Intel Core i3-12100F'},
            {'id': 'amd-ryzen-5-7600x', 'nome': 'AMD Ryzen 5 7600X'},
            {'id': 'intel-i5-14600k', 'nome': 'Intel Core i5-14600K'},
            {'id': 'amd-ryzen-7-7800x3d', 'nome': 'AMD Ryzen 7 7800X3D'},
            {'id': 'intel-i7-14700k', 'nome': 'Intel Core i7-14700K'},
        ],
        'cpu-cooler': [
            {'id': 'cooler-master-212', 'nome': 'Cooler Master Hyper 212'},
            {'id': 'noctua-nh-d15', 'nome': 'Noctua NH-D15'},
            {'id': 'corsair-h100i', 'nome': 'Corsair H100i RGB'},
            {'id': 'be-quiet-dark-rock-4', 'nome': 'be quiet! Dark Rock 4'},
            {'id': 'arctic-liquid-freezer-ii', 'nome': 'Arctic Liquid Freezer II 280'},
            {'id': 'nzxt-kraken-x63', 'nome': 'NZXT Kraken X63'},
            {'id': 'cooler-master-ml240l', 'nome': 'Cooler Master MasterLiquid ML240L'},
            {'id': 'noctua-nh-u12s', 'nome': 'Noctua NH-U12S'},
            {'id': 'corsair-h150i', 'nome': 'Corsair H150i Elite Capellix'},
            {'id': 'scythe-fuma-2', 'nome': 'Scythe Fuma 2'},
            {'id': 'deepcool-ak620', 'nome': 'DeepCool AK620'},
            {'id': 'thermalright-peerless-assassin', 'nome': 'Thermalright Peerless Assassin 120'},
        ],
        'motherboard': [
            {'id': 'asus-b550-plus', 'nome': 'ASUS TUF Gaming B550-PLUS'},
            {'id': 'msi-b450-tomahawk', 'nome': 'MSI B450 Tomahawk MAX'},
            {'id': 'gigabyte-z690-aorus', 'nome': 'Gigabyte Z690 AORUS Elite'},
            {'id': 'asus-z690-prime', 'nome': 'ASUS PRIME Z690-P'},
            {'id': 'msi-x570-gaming-plus', 'nome': 'MSI X570 Gaming Plus'},
            {'id': 'asrock-b550m-pro4', 'nome': 'ASRock B550M Pro4'},
            {'id': 'gigabyte-b450-aorus', 'nome': 'Gigabyte B450 AORUS Elite'},
            {'id': 'asus-rog-strix-b550', 'nome': 'ASUS ROG Strix B550-F Gaming'},
            {'id': 'msi-z690-gaming-edge', 'nome': 'MSI MAG Z690 Gaming Edge'},
            {'id': 'asrock-x570-phantom', 'nome': 'ASRock X570 Phantom Gaming 4'},
            {'id': 'asus-z790-prime', 'nome': 'ASUS PRIME Z790-P'},
            {'id': 'gigabyte-b650-aorus-elite', 'nome': 'Gigabyte B650 AORUS Elite AX'},
        ],
        'memory': [
            {'id': 'corsair-16gb-3200', 'nome': 'Corsair Vengeance LPX 16GB DDR4-3200'},
            {'id': 'gskill-32gb-3600', 'nome': 'G.Skill Trident Z 32GB DDR4-3600'},
            {'id': 'kingston-16gb-2666', 'nome': 'Kingston HyperX Fury 16GB DDR4-2666'},
            {'id': 'corsair-32gb-3600', 'nome': 'Corsair Vengeance RGB Pro 32GB DDR4-3600'},
            {'id': 'gskill-16gb-4000', 'nome': 'G.Skill Ripjaws V 16GB DDR4-4000'},
            {'id': 'crucial-32gb-3200', 'nome': 'Crucial Ballistix 32GB DDR4-3200'},
            {'id': 'teamgroup-16gb-3600', 'nome': 'Team T-FORCE Vulcan Z 16GB DDR4-3600'},
            {'id': 'corsair-64gb-3200', 'nome': 'Corsair Vengeance LPX 64GB DDR4-3200'},
            {'id': 'gskill-16gb-ddr5-5600', 'nome': 'G.Skill Trident Z5 16GB DDR5-5600'},
            {'id': 'corsair-32gb-ddr5-5200', 'nome': 'Corsair Dominator Platinum 32GB DDR5-5200'},
            {'id': 'kingston-fury-32gb-ddr5', 'nome': 'Kingston FURY Beast 32GB DDR5-5600'},
            {'id': 'crucial-16gb-ddr5-4800', 'nome': 'Crucial 16GB DDR5-4800'},
        ],
        'internal-hard-drive': [
            {'id': 'samsung-970-evo-1tb', 'nome': 'Samsung 970 EVO Plus 1TB NVMe SSD'},
            {'id': 'wd-blue-500gb', 'nome': 'Western Digital Blue 500GB SSD'},
            {'id': 'seagate-2tb-hdd', 'nome': 'Seagate Barracuda 2TB HDD'},
            {'id': 'samsung-980-pro-2tb', 'nome': 'Samsung 980 PRO 2TB NVMe SSD'},
            {'id': 'wd-black-sn850-1tb', 'nome': 'WD Black SN850 1TB NVMe SSD'},
            {'id': 'crucial-mx500-1tb', 'nome': 'Crucial MX500 1TB SATA SSD'},
            {'id': 'seagate-firecuda-2tb', 'nome': 'Seagate FireCuda 520 2TB NVMe SSD'},
            {'id': 'wd-blue-4tb-hdd', 'nome': 'Western Digital Blue 4TB HDD'},
            {'id': 'samsung-870-evo-2tb', 'nome': 'Samsung 870 EVO 2TB SATA SSD'},
            {'id': 'kingston-nv2-1tb', 'nome': 'Kingston NV2 1TB NVMe SSD'},
            {'id': 'samsung-990-pro-1tb', 'nome': 'Samsung 990 PRO 1TB NVMe SSD'},
            {'id': 'wd-black-sn850x-2tb', 'nome': 'WD Black SN850X 2TB NVMe SSD'},
        ],
        'video-card': [
            {'id': 'rtx-4060-ti', 'nome': 'NVIDIA GeForce RTX 4060 Ti'},
            {'id': 'rtx-4070', 'nome': 'NVIDIA GeForce RTX 4070'},
            {'id': 'rx-7600-xt', 'nome': 'AMD Radeon RX 7600 XT'},
            {'id': 'rtx-4080', 'nome': 'NVIDIA GeForce RTX 4080'},
            {'id': 'rtx-4090', 'nome': 'NVIDIA GeForce RTX 4090'},
            {'id': 'rx-7800-xt', 'nome': 'AMD Radeon RX 7800 XT'},
            {'id': 'rtx-4060', 'nome': 'NVIDIA GeForce RTX 4060'},
            {'id': 'rx-7700-xt', 'nome': 'AMD Radeon RX 7700 XT'},
            {'id': 'rtx-3060-ti', 'nome': 'NVIDIA GeForce RTX 3060 Ti'},
            {'id': 'rx-6700-xt', 'nome': 'AMD Radeon RX 6700 XT'},
            {'id': 'rtx-3070', 'nome': 'NVIDIA GeForce RTX 3070'},
            {'id': 'rx-6800-xt', 'nome': 'AMD Radeon RX 6800 XT'},
            {'id': 'rtx-4070-super', 'nome': 'NVIDIA GeForce RTX 4070 SUPER'},
            {'id': 'rx-7900-xt', 'nome': 'AMD Radeon RX 7900 XT'},
            {'id': 'rtx-4080-super', 'nome': 'NVIDIA GeForce RTX 4080 SUPER'},
        ],
        'power-supply': [
            {'id': 'corsair-rm750x', 'nome': 'Corsair RM750x 750W 80+ Gold'},
            {'id': 'evga-650-gq', 'nome': 'EVGA SuperNOVA 650 GQ 80+ Gold'},
            {'id': 'seasonic-focus-850', 'nome': 'Seasonic Focus GX-850 80+ Gold'},
            {'id': 'corsair-rm850x', 'nome': 'Corsair RM850x 850W 80+ Gold'},
            {'id': 'evga-750-g5', 'nome': 'EVGA SuperNOVA 750 G5 80+ Gold'},
            {'id': 'seasonic-prime-1000', 'nome': 'Seasonic Prime TX-1000 80+ Titanium'},
            {'id': 'be-quiet-straight-power-650', 'nome': 'be quiet! Straight Power 11 650W'},
            {'id': 'cooler-master-v850', 'nome': 'Cooler Master V850 SFX Gold'},
            {'id': 'thermaltake-toughpower-750', 'nome': 'Thermaltake Toughpower GF1 750W'},
            {'id': 'antec-hcg-850', 'nome': 'Antec HCG850 Gold 850W'},
            {'id': 'corsair-hx1000', 'nome': 'Corsair HX1000 1000W 80+ Platinum'},
            {'id': 'seasonic-focus-gx-1000', 'nome': 'Seasonic Focus GX-1000 80+ Gold'},
        ],
        'case': [
            {'id': 'fractal-define-7', 'nome': 'Fractal Design Define 7'},
            {'id': 'nzxt-h510', 'nome': 'NZXT H510'},
            {'id': 'corsair-4000d', 'nome': 'Corsair 4000D Airflow'},
            {'id': 'lian-li-o11-dynamic', 'nome': 'Lian Li O11 Dynamic'},
            {'id': 'phanteks-p400a', 'nome': 'Phanteks Eclipse P400A'},
            {'id': 'be-quiet-pure-base-500dx', 'nome': 'be quiet! Pure Base 500DX'},
            {'id': 'cooler-master-h500', 'nome': 'Cooler Master MasterBox H500'},
            {'id': 'fractal-meshify-c', 'nome': 'Fractal Design Meshify C'},
            {'id': 'nzxt-h7-flow', 'nome': 'NZXT H7 Flow'},
            {'id': 'corsair-5000d', 'nome': 'Corsair 5000D Airflow'},
            {'id': 'lian-li-lancool-215', 'nome': 'Lian Li LANCOOL 215'},
            {'id': 'fractal-north', 'nome': 'Fractal Design North'},
        ],
        'case-fan': [
            {'id': 'noctua-nf-a12x25', 'nome': 'Noctua NF-A12x25 PWM'},
            {'id': 'arctic-p12', 'nome': 'Arctic P12 PWM PST'},
            {'id': 'corsair-ml120', 'nome': 'Corsair ML120 Pro RGB'},
            {'id': 'be-quiet-silent-wings-3', 'nome': 'be quiet! Silent Wings 3'},
            {'id': 'nzxt-aer-rgb-2', 'nome': 'NZXT Aer RGB 2'},
            {'id': 'cooler-master-sickleflow', 'nome': 'Cooler Master SickleFlow 120'},
            {'id': 'thermaltake-riing-trio', 'nome': 'Thermaltake Riing Trio 12'},
            {'id': 'lian-li-uni-fan', 'nome': 'Lian Li Uni Fan SL120'},
        ],
        'sound-card': [
            {'id': 'creative-ae-5-plus', 'nome': 'Creative Sound Blaster AE-5 Plus'},
            {'id': 'asus-xonar-ae', 'nome': 'ASUS Xonar AE'},
            {'id': 'creative-z', 'nome': 'Creative Sound Blaster Z'},
            {'id': 'evga-nu-audio', 'nome': 'EVGA NU Audio Card'},
            {'id': 'creative-ae-7', 'nome': 'Creative Sound Blaster AE-7'},
        ],
        'wired-network-card': [
            {'id': 'intel-i225-v', 'nome': 'Intel Ethernet Controller I225-V'},
            {'id': 'tp-link-tg-3468', 'nome': 'TP-Link TG-3468 Gigabit'},
            {'id': 'asus-xg-c100c', 'nome': 'ASUS XG-C100C 10G'},
            {'id': 'intel-x550-t2', 'nome': 'Intel Ethernet Converged X550-T2'},
        ],
        'wireless-network-card': [
            {'id': 'intel-ax200', 'nome': 'Intel Wi-Fi 6 AX200'},
            {'id': 'asus-pce-ax58bt', 'nome': 'ASUS PCE-AX58BT Wi-Fi 6'},
            {'id': 'tp-link-archer-t6e', 'nome': 'TP-Link Archer T6E AC1300'},
            {'id': 'intel-ax210', 'nome': 'Intel Wi-Fi 6E AX210'},
            {'id': 'asus-pce-ax3000', 'nome': 'ASUS PCE-AX3000 Wi-Fi 6'},
        ],
        'optical-drive': [
            {'id': 'asus-drw-24b1st', 'nome': 'ASUS DRW-24B1ST DVD Writer'},
            {'id': 'lg-wh14ns40', 'nome': 'LG WH14NS40 Blu-ray Writer'},
            {'id': 'pioneer-bdr-xd07b', 'nome': 'Pioneer BDR-XD07B Portable Blu-ray'},
            {'id': 'asus-bc-12d2ht', 'nome': 'ASUS BC-12D2HT Blu-ray Combo'},
        ],
        'monitor': [
            {'id': 'lg-27gn950-b', 'nome': 'LG 27GN950-B 27" 4K 144Hz'},
            {'id': 'asus-vg248qe', 'nome': 'ASUS VG248QE 24" 1080p 144Hz'},
            {'id': 'dell-s2721dgf', 'nome': 'Dell S2721DGF 27" 1440p 165Hz'},
            {'id': 'samsung-odyssey-g7', 'nome': 'Samsung Odyssey G7 32" 1440p 240Hz'},
            {'id': 'acer-predator-x27', 'nome': 'Acer Predator X27 27" 4K 144Hz HDR'},
            {'id': 'lg-34gn850-b', 'nome': 'LG 34GN850-B 34" Ultrawide 1440p'},
            {'id': 'asus-rog-swift-pg279q', 'nome': 'ASUS ROG Swift PG279Q 27" 1440p'},
        ],
        'keyboard': [
            {'id': 'corsair-k95-rgb', 'nome': 'Corsair K95 RGB Platinum XT'},
            {'id': 'logitech-g915', 'nome': 'Logitech G915 TKL Wireless'},
            {'id': 'razer-huntsman-elite', 'nome': 'Razer Huntsman Elite'},
            {'id': 'steelseries-apex-pro', 'nome': 'SteelSeries Apex Pro'},
            {'id': 'ducky-one-2-mini', 'nome': 'Ducky One 2 Mini 60%'},
            {'id': 'keychron-k8', 'nome': 'Keychron K8 Wireless Mechanical'},
        ],
        'mouse': [
            {'id': 'logitech-g502-hero', 'nome': 'Logitech G502 HERO'},
            {'id': 'razer-deathadder-v3', 'nome': 'Razer DeathAdder V3'},
            {'id': 'steelseries-rival-600', 'nome': 'SteelSeries Rival 600'},
            {'id': 'corsair-dark-core-rgb', 'nome': 'Corsair Dark Core RGB Pro'},
            {'id': 'finalmouse-ultralight-2', 'nome': 'Finalmouse Ultralight 2'},
            {'id': 'glorious-model-o', 'nome': 'Glorious Model O'},
        ],
        'speakers': [
            {'id': 'logitech-z623', 'nome': 'Logitech Z623 2.1 System'},
            {'id': 'creative-pebble-v3', 'nome': 'Creative Pebble V3'},
            {'id': 'audioengine-a2plus', 'nome': 'Audioengine A2+ Wireless'},
            {'id': 'klipsch-promedia-2.1', 'nome': 'Klipsch ProMedia 2.1 THX'},
            {'id': 'edifier-r1280t', 'nome': 'Edifier R1280T Powered Bookshelf'},
        ],
        'headphones': [
            {'id': 'steelseries-arctis-7', 'nome': 'SteelSeries Arctis 7 Wireless'},
            {'id': 'hyperx-cloud-ii', 'nome': 'HyperX Cloud II'},
            {'id': 'sennheiser-hd-660s', 'nome': 'Sennheiser HD 660S'},
            {'id': 'audio-technica-ath-m50x', 'nome': 'Audio-Technica ATH-M50x'},
            {'id': 'corsair-hs80-rgb', 'nome': 'Corsair HS80 RGB Wireless'},
            {'id': 'beyerdynamic-dt-990-pro', 'nome': 'Beyerdynamic DT 990 PRO'},
        ],
    }
    
    # Primeiro carrega dados mock para categorias extras
    for categoria in categorias_extras:
        produtos_por_categoria[categoria] = mock_data.get(categoria, [])
    
    if use_api_for_main:
        # Usa API apenas para categorias principais
        try:
            api = API()
            print("Inicializando API do PCPartPicker para categorias principais...")
            
            start_time = time.time()
            for categoria in categorias_principais:
                # Verifica timeout
                if time.time() - start_time > timeout_seconds:
                    print(f"Timeout atingido, usando fallback para categorias restantes")
                    break
                    
                try:
                    print(f"Buscando dados da API para categoria: {categoria}")
                    
                    # Reduz delay para melhor performance
                    time.sleep(0.5)
                    
                    part_data = api.retrieve(categoria)  # Remove o parâmetro limit que está causando erro
                    
                    if part_data is None or (hasattr(part_data, 'empty') and part_data.empty):
                        print(f"Nenhum dado retornado para categoria: {categoria}")
                        produtos_por_categoria[categoria] = mock_data.get(categoria, [])
                        continue

                    # Convert DataFrame to dict if it's a pandas DataFrame
                    if hasattr(part_data, 'to_dict'):
                        parts_list = part_data.to_dict('records')
                    elif hasattr(part_data, 'iterrows'):
                        # Se for DataFrame, converte para lista de dicts
                        parts_list = []
                        for index, row in part_data.iterrows():
                            parts_list.append(row.to_dict())
                    else:
                        # Se for outro tipo, tenta converter
                        try:
                            import json
                            if isinstance(part_data, str):
                                parts_list = json.loads(part_data)
                            else:
                                parts_list = list(part_data)
                        except:
                            parts_list = []

                    # Map parts to a simplified product dict with id and nome
                    produtos = []
                    for i, part in enumerate(parts_list[:15]):  # Limita a 15 produtos
                        if isinstance(part, dict):
                            # Try different possible field names for name and id
                            nome = part.get('name', part.get('modelo', part.get('title', f'Produto {i+1}')))
                            id_value = part.get('id', part.get('name', f'{categoria}_{i}'))
                            
                            produto = {
                                'id': str(id_value),
                                'nome': str(nome),
                            }
                            produtos.append(produto)
                            print(f"Produto da API adicionado: {nome}")

                    produtos_por_categoria[categoria] = produtos
                    print(f"Total de produtos da API para {categoria}: {len(produtos)}")

                except Exception as e:
                    import traceback
                    print(f"Erro ao buscar dados da API para categoria {categoria}:")
                    print(traceback.format_exc())
                    # Fallback para dados mock se a API falhar
                    produtos_por_categoria[categoria] = mock_data.get(categoria, [])
                    
        except Exception as e:
            print(f"Erro geral na API: {e}")
            print("Usando dados mock para todas as categorias principais")
            # Fallback completo para dados mock
            for categoria in categorias_principais:
                produtos_por_categoria[categoria] = mock_data.get(categoria, [])

    context = {
        'categorias': categorias,
        'produtos_por_categoria': produtos_por_categoria,
    }

    if request.method == 'POST':
        selecionados = {}
        for categoria in categorias:
            produto_id = request.POST.get(f'categoria_{categoria}')
            if produto_id:
                # Find selected product in produtos_por_categoria
                produto = next((p for p in produtos_por_categoria[categoria] if str(p['id']) == produto_id), None)
                if produto:
                    selecionados[categoria] = produto
        context['selecionados'] = selecionados
        return render(request, 'app_top_pc/configurador.html', context)
    else:
        return render(request, 'app_top_pc/configurador.html', context)

def home(request):
    produtos = Produto.objects.all()
    
    produtos_por_tipo = defaultdict(list)
    for produto in produtos:
        # Assuming Produto has a 'categoria' field with a 'nome' attribute
        produtos_por_tipo[produto.categoria.nome].append(produto)

    context = {
        "produtos": produtos_por_tipo,
    }

    return render(request, "app_top_pc/index.html", context)

def catalogo(request):
    produtos = Produto.objects.all()
    context = {
        'produtos': produtos,
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
        return redirect('app_top_pc:home')
    return render(request, 'app_top_pc/remover_componente.html', {'componente': componente})
