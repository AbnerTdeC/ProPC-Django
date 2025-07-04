from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da categoria")
    descricao = models.TextField(blank=True, null=True, help_text="Descrição da categoria")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

# Modelo original mantido para compatibilidade durante migração
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço do produto")
    estoque = models.PositiveIntegerField(default=0, help_text="Quantidade em estoque")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="produtos")
    tipo_componente = models.CharField(max_length=100, help_text="Tipo do componente para o configurador", default='hardware', blank=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

# Novo modelo para componentes base do configurador (todas as peças existentes)
class ComponenteConfiguradorBase(models.Model):
    TIPOS_COMPONENTE = [
        ('cpu', 'Processador'),
        ('cpu-cooler', 'Cooler CPU'),
        ('motherboard', 'Placa-Mãe'),
        ('memory', 'Memória RAM'),
        ('internal-hard-drive', 'Armazenamento'),
        ('video-card', 'Placa de Vídeo'),
        ('power-supply', 'Fonte'),
        ('case', 'Gabinete'),
        ('case-fan', 'Cooler Gabinete'),
        ('sound-card', 'Placa de Som'),
        ('wired-network-card', 'Placa de Rede'),
        ('wireless-network-card', 'Placa Wi-Fi'),
        ('optical-drive', 'Drive Óptico'),
        ('monitor', 'Monitor'),
        ('keyboard', 'Teclado'),
        ('mouse', 'Mouse'),
        ('speakers', 'Caixas de Som'),
        ('headphones', 'Fones de Ouvido'),
        ('hardware', 'Hardware Geral'),
    ]

    nome = models.CharField(max_length=255, help_text="Nome do componente")
    descricao = models.TextField(help_text="Descrição detalhada do componente")
    tipo_componente = models.CharField(
        max_length=100, 
        choices=TIPOS_COMPONENTE,
        help_text="Tipo do componente para o configurador"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.PROTECT, 
        related_name="componentes_configurador"
    )
    especificacoes = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Especificações técnicas em formato JSON"
    )
    imagem = models.ImageField(
        upload_to='componentes/', 
        blank=True, 
        null=True,
        help_text="Imagem do componente"
    )
    ativo = models.BooleanField(
        default=True,
        help_text="Se o componente está ativo no configurador"
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Componente do Configurador"
        verbose_name_plural = "Componentes do Configurador"
        ordering = ['tipo_componente', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_componente_display()})"

# Novo modelo para produtos do catálogo (apenas produtos em estoque/indisponíveis)
class ProdutoCatalogo(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
        ('descontinuado', 'Descontinuado'),
    ]

    componente_base = models.ForeignKey(
        ComponenteConfiguradorBase,
        on_delete=models.PROTECT,
        related_name="produtos_catalogo",
        help_text="Componente base do configurador"
    )
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Preço atual do produto"
    )
    preco_promocional = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Preço promocional (opcional)"
    )
    estoque = models.PositiveIntegerField(
        default=0, 
        help_text="Quantidade em estoque"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel',
        help_text="Status do produto no catálogo"
    )
    fornecedor = models.CharField(
        max_length=255,
        blank=True,
        help_text="Nome do fornecedor"
    )
    codigo_produto = models.CharField(
        max_length=100,
        blank=True,
        help_text="Código do produto no fornecedor"
    )
    observacoes = models.TextField(
        blank=True,
        help_text="Observações sobre o produto"
    )
    data_adicao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto do Catálogo"
        verbose_name_plural = "Produtos do Catálogo"
        ordering = ['-data_atualizacao']

    def __str__(self):
        return f"{self.componente_base.nome} - R$ {self.preco}"

    @property
    def preco_final(self):
        """Retorna o preço promocional se existir, senão o preço normal"""
        return self.preco_promocional if self.preco_promocional else self.preco

    @property
    def disponivel(self):
        """Verifica se o produto está disponível"""
        return self.status == 'disponivel' and self.estoque > 0

# Modelo para compatibilidade (pode ser removido após migração completa)
class Componente(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagem = models.ImageField(upload_to='componentes/', blank=True, null=True)

    class Meta:
        verbose_name = "Componente"
        verbose_name_plural = "Componentes"

    def __str__(self):
        return self.nome
