from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal

User = get_user_model()


class Ingrediente(models.Model):
    """
    Modelo para ingredientes dos usuários.
    Representa matérias-primas e insumos utilizados na produção de produtos.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ingredientes',
        verbose_name="Usuário",
        help_text="Usuário proprietário do ingrediente"
    )
    nome = models.CharField(
        max_length=255,
        verbose_name="Nome do Ingrediente",
        help_text="Nome descritivo do ingrediente (ex: Farinha de Trigo, Açúcar, etc.)"
    )
    preco_por_unidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço por Unidade",
        help_text="Preço unitário do ingrediente em reais"
    )
    unidade_medida = models.CharField(
        max_length=50,
        verbose_name="Unidade de Medida",
        help_text="Unidade de medida do ingrediente (ex: kg, litro, unidade, etc.)"
    )
    fornecedor = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Fornecedor",
        help_text="Nome do fornecedor ou local de compra (opcional)"
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
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
        ordering = ['-created_at']
        unique_together = ['usuario', 'nome']  # Evita ingredientes duplicados para o mesmo usuário

    def __str__(self):
        return f"{self.nome} - R$ {self.preco_por_unidade}/{self.unidade_medida}"

    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        if self.preco_por_unidade is not None and self.preco_por_unidade < 0:
            raise ValidationError({'preco_por_unidade': 'O preço não pode ser negativo.'})
        
        if self.preco_por_unidade is not None and self.preco_por_unidade > Decimal('999999.99'):
            raise ValidationError({'preco_por_unidade': 'O preço não pode ser superior a R$ 999.999,99.'})
        
        # Padroniza a unidade de medida para minúsculas
        if self.unidade_medida:
            self.unidade_medida = self.unidade_medida.lower().strip()

    def save(self, *args, **kwargs):
        """Override do método save para executar validações"""
        self.clean()
        super().save(*args, **kwargs)

    @property
    def custo_formatado(self):
        """Retorna o custo formatado para exibição"""
        return f"R$ {self.preco_por_unidade:.2f} por {self.unidade_medida}"

    @property
    def info_completa(self):
        """Retorna informações completas do ingrediente"""
        fornecedor_info = f" - {self.fornecedor}" if self.fornecedor else ""
        return f"{self.nome} ({self.custo_formatado}){fornecedor_info}"
