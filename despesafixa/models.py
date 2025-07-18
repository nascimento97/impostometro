from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal

User = get_user_model()


class DespesaFixa(models.Model):
    """
    Modelo para despesas fixas dos usuários.
    Representa gastos fixos mensais que impactam no custo dos produtos.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='despesas_fixas',
        verbose_name="Usuário",
        help_text="Usuário proprietário da despesa fixa"
    )
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome da Despesa",
        help_text="Nome descritivo da despesa fixa (ex: Aluguel, Energia, etc.)"
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor",
        help_text="Valor mensal da despesa fixa em reais"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada da despesa (opcional)"
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Indica se a despesa está ativa e deve ser considerada nos cálculos"
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
        verbose_name = "Despesa Fixa"
        verbose_name_plural = "Despesas Fixas"
        ordering = ['-created_at']
        unique_together = ['usuario', 'nome']

    def __str__(self):
        return f"{self.nome} - R$ {self.valor} ({self.usuario.username})"

    def clean(self):
        """Validações customizadas"""
        super().clean()
        if self.valor and self.valor < 0:
            raise ValidationError({'valor': 'O valor da despesa não pode ser negativo.'})

    @property
    def valor_formatado(self):
        """Retorna o valor formatado em reais"""
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @property
    def status_text(self):
        """Retorna o status da despesa em texto"""
        return "Ativa" if self.ativa else "Inativa"
