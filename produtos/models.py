from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal

User = get_user_model()


class Produto(models.Model):
    """
    Modelo para produtos dos usuários.
    Representa os produtos que os comerciantes fabricam/vendem.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='produtos',
        verbose_name="Usuário",
        help_text="Usuário proprietário do produto"
    )
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome do Produto",
        help_text="Nome descritivo do produto"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada do produto"
    )
    tempo_preparo = models.PositiveIntegerField(
        verbose_name="Tempo de Preparo (minutos)",
        help_text="Tempo necessário para preparar o produto em minutos"
    )
    margem_lucro = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Margem de Lucro (%)",
        help_text="Margem de lucro desejada em percentual"
    )
    periodo_analise = models.PositiveIntegerField(
        verbose_name="Período de Análise (dias)",
        help_text="Período em dias para análise financeira"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-created_at']
        unique_together = ['usuario', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.usuario.nome_comercial}"

    def clean(self):
        """
        Validações customizadas do modelo.
        """
        if self.margem_lucro is not None:
            if self.margem_lucro < 0:
                raise ValidationError({
                    'margem_lucro': 'A margem de lucro não pode ser negativa.'
                })
            if self.margem_lucro > 100:
                raise ValidationError({
                    'margem_lucro': 'A margem de lucro não pode ser superior a 100%.'
                })

        if self.tempo_preparo is not None and self.tempo_preparo <= 0:
            raise ValidationError({
                'tempo_preparo': 'O tempo de preparo deve ser maior que zero.'
            })

        if self.periodo_analise is not None and self.periodo_analise <= 0:
            raise ValidationError({
                'periodo_analise': 'O período de análise deve ser maior que zero.'
            })

    @property
    def margem_lucro_formatada(self):
        """Retorna a margem de lucro formatada"""
        return f"{self.margem_lucro}%"

    @property
    def tempo_preparo_formatado(self):
        """Retorna o tempo de preparo formatado"""
        if self.tempo_preparo >= 60:
            horas = self.tempo_preparo // 60
            minutos = self.tempo_preparo % 60
            if minutos > 0:
                return f"{horas}h {minutos}min"
            else:
                return f"{horas}h"
        else:
            return f"{self.tempo_preparo}min"

    @property
    def info_completa(self):
        """Retorna informações resumidas do produto"""
        return {
            'id': self.id,
            'nome': self.nome,
            'tempo_preparo': self.tempo_preparo_formatado,
            'margem_lucro': self.margem_lucro_formatada,
            'periodo_analise': f"{self.periodo_analise} dias",
            'usuario': self.usuario.nome_comercial
        }


class ProdutoIngrediente(models.Model):
    """
    Modelo para relacionar produtos com ingredientes e suas quantidades.
    """
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='produto_ingredientes',
        verbose_name="Produto"
    )
    ingrediente = models.ForeignKey(
        'ingredientes.Ingrediente',
        on_delete=models.CASCADE,
        related_name='produto_ingredientes',
        verbose_name="Ingrediente"
    )
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Quantidade",
        help_text="Quantidade do ingrediente utilizada no produto"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = "Produto Ingrediente"
        verbose_name_plural = "Produtos Ingredientes"
        unique_together = ['produto', 'ingrediente']
        ordering = ['produto', 'ingrediente__nome']

    def __str__(self):
        return f"{self.produto.nome} - {self.ingrediente.nome} ({self.quantidade})"

    def clean(self):
        """Validações customizadas"""
        if self.quantidade is not None and self.quantidade <= 0:
            raise ValidationError({
                'quantidade': 'A quantidade deve ser maior que zero.'
            })

        # Verificar se o ingrediente pertence ao mesmo usuário do produto
        if (self.produto and self.ingrediente and 
            self.produto.usuario != self.ingrediente.usuario):
            raise ValidationError({
                'ingrediente': 'O ingrediente deve pertencer ao mesmo usuário do produto.'
            })

    @property
    def custo_total(self):
        """Calcula o custo total deste ingrediente no produto"""
        return self.quantidade * self.ingrediente.preco_por_unidade


class ProdutoDespesaFixa(models.Model):
    """
    Modelo para relacionar produtos com despesas fixas.
    """
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='produto_despesas_fixas',
        verbose_name="Produto"
    )
    despesa_fixa = models.ForeignKey(
        'despesafixa.DespesaFixa',
        on_delete=models.CASCADE,
        related_name='produto_despesas_fixas',
        verbose_name="Despesa Fixa"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = "Produto Despesa Fixa"
        verbose_name_plural = "Produtos Despesas Fixas"
        unique_together = ['produto', 'despesa_fixa']
        ordering = ['produto', 'despesa_fixa__nome']

    def __str__(self):
        return f"{self.produto.nome} - {self.despesa_fixa.nome}"

    def clean(self):
        """Validações customizadas"""
        # Verificar se a despesa fixa pertence ao mesmo usuário do produto
        if (self.produto and self.despesa_fixa and 
            self.produto.usuario != self.despesa_fixa.usuario):
            raise ValidationError({
                'despesa_fixa': 'A despesa fixa deve pertencer ao mesmo usuário do produto.'
            })


class ProdutoDespesaVariavel(models.Model):
    """
    Modelo para relacionar produtos com despesas variáveis e suas quantidades.
    """
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='produto_despesas_variaveis',
        verbose_name="Produto"
    )
    despesa_variavel = models.ForeignKey(
        'despesavariavel.DespesaVariavel',
        on_delete=models.CASCADE,
        related_name='produto_despesas_variaveis',
        verbose_name="Despesa Variável"
    )
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Quantidade",
        help_text="Quantidade da despesa variável utilizada no produto"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = "Produto Despesa Variável"
        verbose_name_plural = "Produtos Despesas Variáveis"
        unique_together = ['produto', 'despesa_variavel']
        ordering = ['produto', 'despesa_variavel__nome']

    def __str__(self):
        return f"{self.produto.nome} - {self.despesa_variavel.nome} ({self.quantidade})"

    def clean(self):
        """Validações customizadas"""
        if self.quantidade is not None and self.quantidade <= 0:
            raise ValidationError({
                'quantidade': 'A quantidade deve ser maior que zero.'
            })

        # Verificar se a despesa variável pertence ao mesmo usuário do produto
        if (self.produto and self.despesa_variavel and 
            self.produto.usuario != self.despesa_variavel.usuario):
            raise ValidationError({
                'despesa_variavel': 'A despesa variável deve pertencer ao mesmo usuário do produto.'
            })

    @property
    def custo_total(self):
        """Calcula o custo total desta despesa variável no produto"""
        return self.quantidade * self.despesa_variavel.valor_por_unidade
