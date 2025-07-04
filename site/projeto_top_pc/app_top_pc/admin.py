from django.contrib import admin
from .models import (
    Categoria, 
    Produto, 
    ComponenteConfiguradorBase, 
    ProdutoCatalogo,
    Componente
)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(ComponenteConfiguradorBase)
class ComponenteConfiguradorBaseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_componente', 'categoria', 'ativo', 'data_atualizacao')
    list_filter = ('tipo_componente', 'categoria', 'ativo')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        (None, {
            'fields': ('nome', 'descricao', 'tipo_componente', 'categoria')
        }),
        ('Detalhes', {
            'fields': ('especificacoes', 'imagem', 'ativo')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProdutoCatalogo)
class ProdutoCatalogoAdmin(admin.ModelAdmin):
    list_display = ('componente_base', 'preco', 'preco_promocional', 'estoque', 'status', 'data_atualizacao')
    list_filter = ('status', 'fornecedor')
    search_fields = ('componente_base__nome', 'codigo_produto', 'fornecedor')
    readonly_fields = ('data_adicao', 'data_atualizacao')
    fieldsets = (
        (None, {
            'fields': ('componente_base', 'preco', 'preco_promocional', 'estoque')
        }),
        ('Status e Fornecedor', {
            'fields': ('status', 'fornecedor', 'codigo_produto')
        }),
        ('Informações Adicionais', {
            'fields': ('observacoes', 'data_adicao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

# Mantido para compatibilidade durante migração
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')

# Mantido para compatibilidade durante migração
@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')
