from django import forms
from .models import Produto

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Você pode adicionar personalizações adicionais aqui se necessário
        # Por exemplo, se você não quiser adicionar a classe 'form-control' via widgets para todos:
        # for field_name, field in self.fields.items():
        #     if not field.widget.attrs.get('class'):
        #          field.widget.attrs.update({'class': 'form-control'})
