from rest_framework import serializers
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Produto, ProdutoIngrediente, ProdutoDespesaFixa, ProdutoDespesaVariavel


class ProdutoSerializer(serializers.ModelSerializer):
    """
    Serializer principal para o modelo Produto.
    Usado para listagem e detalhes de produtos.
    """
    usuario_nome = serializers.CharField(source='usuario.nome_comercial', read_only=True)
    margem_lucro_formatada = serializers.ReadOnlyField()
    tempo_preparo_formatado = serializers.ReadOnlyField()
    info_completa = serializers.ReadOnlyField()

    class Meta:
        model = Produto
        fields = [
            'id', 'usuario', 'nome', 'descricao', 'tempo_preparo', 
            'margem_lucro', 'periodo_analise', 'created_at', 'updated_at',
            'usuario_nome', 'margem_lucro_formatada', 'tempo_preparo_formatado',
            'info_completa'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_nome(self, value):
        """Validação customizada para nome"""
        if value:
            value = value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("O nome deve ter pelo menos 2 caracteres.")
        return value

    def validate_tempo_preparo(self, value):
        """Validação customizada para tempo de preparo"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("O tempo de preparo deve ser maior que zero.")
        if value is not None and value > 10080:  # 1 semana em minutos
            raise serializers.ValidationError("O tempo de preparo não pode ser superior a 1 semana (10.080 minutos).")
        return value

    def validate_margem_lucro(self, value):
        """Validação customizada para margem de lucro"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("A margem de lucro não pode ser negativa.")
            if value > 1000:  # 1000%
                raise serializers.ValidationError("A margem de lucro não pode ser superior a 1000%.")
        return value

    def validate_periodo_analise(self, value):
        """Validação customizada para período de análise"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("O período de análise deve ser maior que zero.")
        if value is not None and value > 3650:  # 10 anos
            raise serializers.ValidationError("O período de análise não pode ser superior a 10 anos (3650 dias).")
        return value

    def validate(self, data):
        """Validação geral dos dados"""
        # Verificar se já existe um produto com o mesmo nome para o usuário
        usuario = self.context['request'].user
        nome = data.get('nome')
        
        if nome:
            produtos_existentes = Produto.objects.filter(
                usuario=usuario, 
                nome__iexact=nome.strip()
            )
            
            # Se estamos editando, excluir o produto atual da verificação
            if self.instance:
                produtos_existentes = produtos_existentes.exclude(id=self.instance.id)
            
            if produtos_existentes.exists():
                raise serializers.ValidationError({
                    'nome': 'Já existe um produto com este nome.'
                })
        
        return data


class ProdutoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para criação de produtos.
    """
    class Meta:
        model = Produto
        fields = [
            'nome', 'descricao', 'tempo_preparo', 
            'margem_lucro', 'periodo_analise'
        ]

    def validate_nome(self, value):
        """Validação customizada para nome"""
        if value:
            value = value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("O nome deve ter pelo menos 2 caracteres.")
        return value

    def validate_tempo_preparo(self, value):
        """Validação customizada para tempo de preparo"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("O tempo de preparo deve ser maior que zero.")
        return value

    def validate_margem_lucro(self, value):
        """Validação customizada para margem de lucro"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("A margem de lucro não pode ser negativa.")
            if value > 1000:
                raise serializers.ValidationError("A margem de lucro não pode ser superior a 1000%.")
        return value

    def validate_periodo_analise(self, value):
        """Validação customizada para período de análise"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("O período de análise deve ser maior que zero.")
        return value

    def create(self, validated_data):
        """Sobrescreve o método create para definir o usuário automaticamente"""
        usuario = self.context['request'].user
        validated_data['usuario'] = usuario
        return super().create(validated_data)


class ProdutoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para atualização de produtos.
    """
    class Meta:
        model = Produto
        fields = [
            'nome', 'descricao', 'tempo_preparo', 
            'margem_lucro', 'periodo_analise'
        ]

    def validate_nome(self, value):
        """Validação customizada para nome"""
        if value:
            value = value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("O nome deve ter pelo menos 2 caracteres.")
        return value

    def validate_tempo_preparo(self, value):
        """Validação customizada para tempo de preparo"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("O tempo de preparo deve ser maior que zero.")
        return value

    def validate_margem_lucro(self, value):
        """Validação customizada para margem de lucro"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("A margem de lucro não pode ser negativa.")
            if value > 1000:
                raise serializers.ValidationError("A margem de lucro não pode ser superior a 1000%.")
        return value

    def validate_periodo_analise(self, value):
        """Validação customizada para período de análise"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("O período de análise deve ser maior que zero.")
        return value


class ProdutoListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para listagem de produtos.
    Inclui apenas campos essenciais para melhor performance.
    """
    usuario_nome = serializers.CharField(source='usuario.nome_comercial', read_only=True)
    margem_lucro_formatada = serializers.ReadOnlyField()
    tempo_preparo_formatado = serializers.ReadOnlyField()

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'tempo_preparo', 'margem_lucro', 
            'periodo_analise', 'created_at', 'usuario_nome',
            'margem_lucro_formatada', 'tempo_preparo_formatado'
        ]


class ProdutoIngredienteSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo ProdutoIngrediente.
    """
    ingrediente_nome = serializers.CharField(source='ingrediente.nome', read_only=True)
    ingrediente_preco = serializers.DecimalField(
        source='ingrediente.preco_por_unidade', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    ingrediente_unidade = serializers.CharField(source='ingrediente.unidade_medida', read_only=True)
    custo_total = serializers.ReadOnlyField()

    class Meta:
        model = ProdutoIngrediente
        fields = [
            'id', 'produto', 'ingrediente', 'quantidade', 'created_at',
            'ingrediente_nome', 'ingrediente_preco', 'ingrediente_unidade',
            'custo_total'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_quantidade(self, value):
        """Validação customizada para quantidade"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        if value is not None and value > Decimal('999999.999'):
            raise serializers.ValidationError("A quantidade não pode ser superior a 999.999,999.")
        return value


class ProdutoDespesaFixaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo ProdutoDespesaFixa.
    """
    despesa_nome = serializers.CharField(source='despesa_fixa.nome', read_only=True)
    despesa_valor = serializers.DecimalField(
        source='despesa_fixa.valor', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = ProdutoDespesaFixa
        fields = [
            'id', 'produto', 'despesa_fixa', 'created_at',
            'despesa_nome', 'despesa_valor'
        ]
        read_only_fields = ['id', 'created_at']


class ProdutoDespesaVariavelSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo ProdutoDespesaVariavel.
    """
    despesa_nome = serializers.CharField(source='despesa_variavel.nome', read_only=True)
    despesa_valor_unitario = serializers.DecimalField(
        source='despesa_variavel.valor_por_unidade', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    despesa_unidade = serializers.CharField(source='despesa_variavel.unidade_medida', read_only=True)
    custo_total = serializers.ReadOnlyField()

    class Meta:
        model = ProdutoDespesaVariavel
        fields = [
            'id', 'produto', 'despesa_variavel', 'quantidade', 'created_at',
            'despesa_nome', 'despesa_valor_unitario', 'despesa_unidade',
            'custo_total'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_quantidade(self, value):
        """Validação customizada para quantidade"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        if value is not None and value > Decimal('999999.999'):
            raise serializers.ValidationError("A quantidade não pode ser superior a 999.999,999.")
        return value


class ProdutoDetalhadoSerializer(serializers.ModelSerializer):
    """
    Serializer completo para visualização detalhada de produtos.
    Inclui todos os relacionamentos.
    """
    usuario_nome = serializers.CharField(source='usuario.nome_comercial', read_only=True)
    margem_lucro_formatada = serializers.ReadOnlyField()
    tempo_preparo_formatado = serializers.ReadOnlyField()
    ingredientes = ProdutoIngredienteSerializer(source='produto_ingredientes', many=True, read_only=True)
    despesas_fixas = ProdutoDespesaFixaSerializer(source='produto_despesas_fixas', many=True, read_only=True)
    despesas_variaveis = ProdutoDespesaVariavelSerializer(source='produto_despesas_variaveis', many=True, read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id', 'usuario', 'nome', 'descricao', 'tempo_preparo', 
            'margem_lucro', 'periodo_analise', 'created_at', 'updated_at',
            'usuario_nome', 'margem_lucro_formatada', 'tempo_preparo_formatado',
            'ingredientes', 'despesas_fixas', 'despesas_variaveis'
        ]
