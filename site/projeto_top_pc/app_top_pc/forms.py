from django import forms
from .models import (
    Produto, 
    ComponenteConfiguradorBase, 
    ProdutoCatalogo
)

class ComponenteConfiguradorBaseForm(forms.ModelForm):
    class Meta:
        model = ComponenteConfiguradorBase
        fields = ['nome', 'descricao', 'tipo_componente', 'categoria', 'especificacoes', 'imagem', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo_componente': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'especificacoes': forms.JSONField(widget=forms.Textarea(attrs={'class': 'form-control'})),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome do Componente',
            'descricao': 'Descrição',
            'tipo_componente': 'Tipo de Componente',
            'categoria': 'Categoria',
            'especificacoes': 'Especificações Técnicas (JSON)',
            'imagem': 'Imagem do Componente',
            'ativo': 'Ativo no Configurador',
        }
        help_texts = {
            'especificacoes': 'Insira as especificações técnicas em formato JSON.',
            'tipo_componente': 'Selecione o tipo de componente para o configurador.',
        }

class ProdutoCatalogoForm(forms.ModelForm):
    class Meta:
        model = ProdutoCatalogo
        fields = [
            'componente_base', 'preco', 'preco_promocional', 
            'estoque', 'status', 'fornecedor', 
            'codigo_produto', 'observacoes'
        ]
        widgets = {
            'componente_base': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_promocional': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_produto': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'componente_base': 'Componente Base',
            'preco': 'Preço (R$)',
            'preco_promocional': 'Preço Promocional (R$)',
            'estoque': 'Quantidade em Estoque',
            'status': 'Status do Produto',
            'fornecedor': 'Fornecedor',
            'codigo_produto': 'Código do Produto',
            'observacoes': 'Observações',
        }
        help_texts = {
            'preco': 'Informe o preço em Reais (ex: 1250.99).',
            'preco_promocional': 'Opcional: Informe o preço promocional em Reais.',
            'estoque': 'Quantidade disponível em estoque.',
            'codigo_produto': 'Código do produto no fornecedor (opcional).',
        }

    def clean(self):
        cleaned_data = super().clean()
        preco = cleaned_data.get('preco')
        preco_promocional = cleaned_data.get('preco_promocional')

        if preco_promocional and preco and preco_promocional >= preco:
            raise forms.ValidationError(
                "O preço promocional deve ser menor que o preço normal."
            )
        return cleaned_data

# Mantido para compatibilidade durante migração
class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'categoria', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Produto',
            'descricao': 'Descrição',
            'preco': 'Preço (R$)',
            'estoque': 'Quantidade em Estoque',
            'categoria': 'Categoria',
            'imagem': 'Imagem do Produto',
        }
        help_texts = {
            'preco': 'Informe o preço em Reais (ex: 1250.99).',
            'estoque': 'Quantidade disponível em estoque.',
        }
        error_messages = {
            'nome': {
                'max_length': "O nome do produto é muito longo.",
                'required': "O nome do produto é obrigatório."
            },
            'preco': {
                'invalid': "Por favor, insira um valor numérico válido para o preço."
            }
        }
