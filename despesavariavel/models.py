from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal

User = get_user_model()


class DespesaVariavel(models.Model):
    """
    Modelo para despesas variáveis dos usuários.
    Representa gastos que variam conforme a produção e impactam no custo dos produtos.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='despesas_variaveis',
        verbose_name="Usuário",
        help_text="Usuário proprietário da despesa variável"
    )
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome da Despesa",
        help_text="Nome descritivo da despesa variável (ex: Embalagem, Combustível, etc.)"
    )
    valor_por_unidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor por Unidade",
        help_text="Valor unitário da despesa variável"
    )
    unidade_medida = models.CharField(
        max_length=50,
        verbose_name="Unidade de Medida",
        help_text="Unidade de medida da despesa (ex: peça, kg, litro, etc.)"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada da despesa variável"
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Define se a despesa variável está ativa para uso"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )

    class Meta:
        verbose_name = "Despesa Variável"
        verbose_name_plural = "Despesas Variáveis"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['usuario', 'ativa']),
            models.Index(fields=['nome']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'nome'],
                name='unique_despesa_variavel_por_usuario'
            )
        ]

    def __str__(self):
        return f"{self.nome} - {self.usuario.username}"

    def clean(self):
        """Validações personalizadas do modelo"""
        super().clean()
        
        if self.valor_por_unidade is not None and self.valor_por_unidade < 0:
            raise ValidationError({
                'valor_por_unidade': 'O valor por unidade não pode ser negativo.'
            })
        
        if self.valor_por_unidade is not None and self.valor_por_unidade > Decimal('999999.99'):
            raise ValidationError({
                'valor_por_unidade': 'O valor por unidade é muito alto.'
            })

        if not self.nome or not self.nome.strip():
            raise ValidationError({
                'nome': 'O nome da despesa é obrigatório.'
            })

        if not self.unidade_medida or not self.unidade_medida.strip():
            raise ValidationError({
                'unidade_medida': 'A unidade de medida é obrigatória.'
            })

    def save(self, *args, **kwargs):
        """Override do save para executar validações"""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def valor_formatado(self):
        """Retorna o valor formatado em real brasileiro"""
        if self.valor_por_unidade:
            return f"R$ {self.valor_por_unidade:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"

    @property
    def status_text(self):
        """Retorna o status em texto"""
        return "Ativa" if self.ativa else "Inativa"

    @property
    def info_completa(self):
        """Retorna informação completa da despesa"""
        return f"{self.nome} - {self.valor_formatado}/{self.unidade_medida}"
