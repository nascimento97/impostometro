from rest_framework import serializers
from decimal import Decimal
from .models import AnaliseFinanceira


class AnaliseFinanceiraSerializer(serializers.ModelSerializer):
    """
    Serializer principal para o modelo AnaliseFinanceira.
    Usado para listagem e detalhes de análises financeiras.
    """
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    usuario_nome = serializers.CharField(source='produto.usuario.nome_comercial', read_only=True)
    margem_lucro_real = serializers.ReadOnlyField()
    margem_lucro_formatada = serializers.ReadOnlyField()
    custo_total_formatado = serializers.ReadOnlyField()
    preco_venda_formatado = serializers.ReadOnlyField()
    lucro_formatado = serializers.ReadOnlyField()
    faturamento_formatado = serializers.ReadOnlyField()

    class Meta:
        model = AnaliseFinanceira
        fields = [
            'id', 'produto', 'custo_ingredientes', 'custo_despesas_fixas',
            'custo_despesas_variaveis', 'custo_total_producao', 'preco_venda_sugerido',
            'faturamento_previsto', 'lucro_previsto', 'created_at',
            'produto_nome', 'usuario_nome', 'margem_lucro_real', 'margem_lucro_formatada',
            'custo_total_formatado', 'preco_venda_formatado', 'lucro_formatado',
            'faturamento_formatado'
        ]
        read_only_fields = ['id', 'custo_total_producao', 'created_at']

    def validate_custo_ingredientes(self, value):
        """Validação para custo de ingredientes"""
        if value < 0:
            raise serializers.ValidationError("O custo dos ingredientes não pode ser negativo.")
        return value

    def validate_custo_despesas_fixas(self, value):
        """Validação para custo de despesas fixas"""
        if value < 0:
            raise serializers.ValidationError("O custo das despesas fixas não pode ser negativo.")
        return value

    def validate_custo_despesas_variaveis(self, value):
        """Validação para custo de despesas variáveis"""
        if value < 0:
            raise serializers.ValidationError("O custo das despesas variáveis não pode ser negativo.")
        return value

    def validate_preco_venda_sugerido(self, value):
        """Validação para preço de venda sugerido"""
        if value <= 0:
            raise serializers.ValidationError("O preço de venda deve ser maior que zero.")
        return value

    def validate_faturamento_previsto(self, value):
        """Validação para faturamento previsto"""
        if value < 0:
            raise serializers.ValidationError("O faturamento previsto não pode ser negativo.")
        return value

    def validate_lucro_previsto(self, value):
        """Validação para lucro previsto"""
        # Lucro pode ser negativo (prejuízo), então apenas verificamos se é um número válido
        return value


class AnaliseFinanceiraCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de análises financeiras.
    Inclui validações específicas para criação.
    """
    class Meta:
        model = AnaliseFinanceira
        fields = [
            'produto', 'custo_ingredientes', 'custo_despesas_fixas',
            'custo_despesas_variaveis', 'preco_venda_sugerido',
            'faturamento_previsto', 'lucro_previsto'
        ]

    def validate_produto(self, value):
        """Validação para o produto"""
        if not value:
            raise serializers.ValidationError("É necessário informar um produto.")
        
        # Verifica se o produto pertence ao usuário logado
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if value.usuario != request.user:
                raise serializers.ValidationError("Você só pode criar análises para seus próprios produtos.")
        
        return value

    def validate(self, data):
        """Validação geral dos dados"""
        # Verifica se o preço de venda é maior que o custo total
        custo_total = (
            data.get('custo_ingredientes', Decimal('0.00')) +
            data.get('custo_despesas_fixas', Decimal('0.00')) +
            data.get('custo_despesas_variaveis', Decimal('0.00'))
        )
        
        if data.get('preco_venda_sugerido', Decimal('0.00')) <= custo_total:
            raise serializers.ValidationError({
                'preco_venda_sugerido': 
                'O preço de venda deve ser maior que o custo total de produção.'
            })
        
        return data


class AnaliseFinanceiraUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de análises financeiras.
    Não permite alterar o produto após criação.
    """
    class Meta:
        model = AnaliseFinanceira
        fields = [
            'custo_ingredientes', 'custo_despesas_fixas',
            'custo_despesas_variaveis', 'preco_venda_sugerido',
            'faturamento_previsto', 'lucro_previsto'
        ]

    def validate(self, data):
        """Validação geral dos dados para atualização"""
        instance = self.instance
        
        # Pega os valores atuais se não foram fornecidos novos
        custo_ingredientes = data.get('custo_ingredientes', instance.custo_ingredientes)
        custo_despesas_fixas = data.get('custo_despesas_fixas', instance.custo_despesas_fixas)
        custo_despesas_variaveis = data.get('custo_despesas_variaveis', instance.custo_despesas_variaveis)
        preco_venda = data.get('preco_venda_sugerido', instance.preco_venda_sugerido)
        
        custo_total = custo_ingredientes + custo_despesas_fixas + custo_despesas_variaveis
        
        if preco_venda <= custo_total:
            raise serializers.ValidationError({
                'preco_venda_sugerido': 
                'O preço de venda deve ser maior que o custo total de produção.'
            })
        
        return data


class AnaliseFinanceiraListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de análises financeiras.
    Inclui apenas campos essenciais para performance.
    """
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    margem_lucro_formatada = serializers.ReadOnlyField()
    custo_total_formatado = serializers.ReadOnlyField()
    preco_venda_formatado = serializers.ReadOnlyField()

    class Meta:
        model = AnaliseFinanceira
        fields = [
            'id', 'produto', 'produto_nome', 'custo_total_producao',
            'preco_venda_sugerido', 'lucro_previsto', 'created_at',
            'margem_lucro_formatada', 'custo_total_formatado', 'preco_venda_formatado'
        ]


class AnaliseFinanceiraDetalhadaSerializer(serializers.ModelSerializer):
    """
    Serializer completo para detalhes de análises financeiras.
    Inclui informações detalhadas do produto e todas as métricas.
    """
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_descricao = serializers.CharField(source='produto.descricao', read_only=True)
    produto_margem_lucro = serializers.DecimalField(
        source='produto.margem_lucro', 
        max_digits=5, 
        decimal_places=2, 
        read_only=True
    )
    usuario_nome = serializers.CharField(source='produto.usuario.nome_comercial', read_only=True)
    margem_lucro_real = serializers.ReadOnlyField()
    margem_lucro_formatada = serializers.ReadOnlyField()
    custo_total_formatado = serializers.ReadOnlyField()
    preco_venda_formatado = serializers.ReadOnlyField()
    lucro_formatado = serializers.ReadOnlyField()
    faturamento_formatado = serializers.ReadOnlyField()

    class Meta:
        model = AnaliseFinanceira
        fields = [
            'id', 'produto', 'produto_nome', 'produto_descricao', 'produto_margem_lucro',
            'usuario_nome', 'custo_ingredientes', 'custo_despesas_fixas',
            'custo_despesas_variaveis', 'custo_total_producao', 'preco_venda_sugerido',
            'faturamento_previsto', 'lucro_previsto', 'created_at',
            'margem_lucro_real', 'margem_lucro_formatada', 'custo_total_formatado',
            'preco_venda_formatado', 'lucro_formatado', 'faturamento_formatado'
        ]
