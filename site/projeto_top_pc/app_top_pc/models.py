from django.db import models
from django.utils import timezone

# -----------------------------------------------------------------------------
# Modelo para Categoria de Produtos
# -----------------------------------------------------------------------------
class Categoria(models.Model):
    """
    Representa a categoria de um produto.
    """
    nome = models.CharField(max_length=100, unique=True, help_text='Nome da categoria')
    descricao = models.TextField(blank=True, null=True, help_text='Descrição da categoria')

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

# -----------------------------------------------------------------------------
# Modelo para Usuário e Cliente (Relação de Especialização)
# -----------------------------------------------------------------------------
class Usuario(models.Model):
    """
    Modelo base de usuário, contendo informações comuns de login.
    No diagrama, Cliente herda de Usuário. Em Django, isso é geralmente
    modelado com uma relação OneToOneField.
    """
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)  # Em um projeto real, use o sistema de autenticação do Django
    data_nascimento = models.DateField()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email

class Cliente(models.Model):
    """
    Representa um cliente, que é um tipo especializado de Usuário.
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField(max_length=14, unique=True, help_text='Formato: 000.000.000-00')
    telefone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.usuario.nome

# -----------------------------------------------------------------------------
# Modelo de Endereço (Associado ao Cliente)
# -----------------------------------------------------------------------------
class Endereco(models.Model):
    """
    Armazena os endereços de um cliente.
    Um cliente pode ter vários endereços.
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, help_text='Sigla do estado (ex: SP, RJ)')
    cep = models.CharField(max_length=9, help_text='Formato: 00000-000')

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        # Garante que um cliente não tenha o mesmo endereço cadastrado duas vezes
        unique_together = [['cliente', 'cep', 'numero']]

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"

# -----------------------------------------------------------------------------
# Modelo de Produto
# -----------------------------------------------------------------------------
class Produto(models.Model):
    """
    Representa um produto disponível para venda.
    """
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2, help_text='Preço do produto')
    estoque = models.PositiveIntegerField(default=0, help_text='Quantidade em estoque')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT, # Impede a exclusão de uma categoria se houver produtos nela
        related_name='produtos'
    )
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True, help_text='Imagem do produto')

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

# -----------------------------------------------------------------------------
# Modelos de Pedido e ItemPedido (Relação Muitos-para-Muitos com Tabela Intermediária)
# -----------------------------------------------------------------------------
class Pedido(models.Model):
    """
    Representa um pedido feito por um cliente.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    data_pedido = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    produtos = models.ManyToManyField(
        Produto,
        through='ItemPedido', # Especifica o modelo intermediário
        related_name='pedidos'
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido'] # Ordena os pedidos mais recentes primeiro

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.usuario.nome}"

class ItemPedido(models.Model):
    """
    Modelo intermediário que representa a relação entre Pedido e Produto.
    Contém a quantidade e o preço do produto no momento da compra.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT) # Protege o produto de ser deletado se estiver em um pedido
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Preço do produto no momento da compra'
    )

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
        # Garante que o mesmo produto não seja adicionado duas vezes ao mesmo pedido
        unique_together = [['pedido', 'produto']]

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no Pedido #{self.pedido.id}"