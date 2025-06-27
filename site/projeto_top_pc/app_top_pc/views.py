from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pcpartpicker import API
from .models import *
from .forms import ComponenteForm

@csrf_exempt
def configurador(request):
    api = API()
    supported_parts = api.supported_parts
    categorias = list(supported_parts)
    produtos_por_categoria = {}

    # Fetch parts data from API for each category
    for categoria in categorias:
        try:
            part_data = api.retrieve(categoria)
            # part_data.to_json() returns JSON string, parse it to dict
            import json
            parts_list = json.loads(part_data.to_json())
            # Map parts to a simplified product dict with id and nome
            produtos = []
            for part in parts_list:
                produto = {
                    'id': part.get('id', part.get('name', '')),
                    'nome': part.get('name', 'Unknown'),
                }
                produtos.append(produto)
            produtos_por_categoria[categoria] = produtos
        except Exception as e:
            produtos_por_categoria[categoria] = []
            print(f"Error fetching data for category {categoria}: {e}")

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
