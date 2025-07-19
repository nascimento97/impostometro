from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class AnaliseFinanceira(models.Model):
    """
    Modelo para análises financeiras de produtos.
    Armazena os resultados dos cálculos de precificação e lucratividade.
    """
    produto = models.ForeignKey(
        'produtos.Produto',
        on_delete=models.CASCADE,
        related_name='analises_financeiras',
        verbose_name="Produto",
        help_text="Produto analisado"
    )
    custo_ingredientes = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Custo dos Ingredientes",
        help_text="Custo total dos ingredientes utilizados"
    )
    custo_despesas_fixas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Custo das Despesas Fixas",
        help_text="Custo total das despesas fixas aplicáveis"
    )
    custo_despesas_variaveis = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Custo das Despesas Variáveis",
        help_text="Custo total das despesas variáveis aplicáveis"
    )
    custo_total_producao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Custo Total de Produção",
        help_text="Soma de todos os custos de produção"
    )
    preco_venda_sugerido = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Preço de Venda Sugerido",
        help_text="Preço sugerido baseado na margem de lucro desejada"
    )
    faturamento_previsto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Faturamento Previsto",
        help_text="Faturamento esperado no período de análise"
    )
    lucro_previsto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Lucro Previsto",
        help_text="Lucro esperado no período de análise"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação",
        help_text="Data e hora da criação da análise"
    )

    class Meta:
        verbose_name = "Análise Financeira"
        verbose_name_plural = "Análises Financeiras"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Análise de {self.produto.nome} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

    @property
    def margem_lucro_real(self):
        """Calcula a margem de lucro real baseada nos custos calculados"""
        if self.custo_total_producao > 0:
            return ((self.preco_venda_sugerido - self.custo_total_producao) / self.custo_total_producao) * 100
        return Decimal('0.00')

    @property
    def margem_lucro_formatada(self):
        """Retorna a margem de lucro formatada com símbolo %"""
        return f"{self.margem_lucro_real:.2f}%"

    @property
    def custo_total_formatado(self):
        """Retorna o custo total formatado com símbolo de moeda"""
        return f"R$ {self.custo_total_producao:.2f}"

    @property
    def preco_venda_formatado(self):
        """Retorna o preço de venda formatado com símbolo de moeda"""
        return f"R$ {self.preco_venda_sugerido:.2f}"

    @property
    def lucro_formatado(self):
        """Retorna o lucro formatado com símbolo de moeda"""
        return f"R$ {self.lucro_previsto:.2f}"

    @property
    def faturamento_formatado(self):
        """Retorna o faturamento formatado com símbolo de moeda"""
        return f"R$ {self.faturamento_previsto:.2f}"

    def save(self, *args, **kwargs):
        """Override do save para calcular automaticamente o custo total"""
        self.custo_total_producao = (
            self.custo_ingredientes + 
            self.custo_despesas_fixas + 
            self.custo_despesas_variaveis
        )
        super().save(*args, **kwargs)
