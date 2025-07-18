from rest_framework import serializers
from decimal import Decimal
from .models import DespesaVariavel


class DespesaVariavelSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo DespesaVariavel.
    Usado para listagem e detalhes de despesas variáveis.
    """
    valor_formatado = serializers.ReadOnlyField()
    status_text = serializers.ReadOnlyField()
    info_completa = serializers.ReadOnlyField()
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = DespesaVariavel
        fields = [
            'id', 'usuario', 'nome', 'valor_por_unidade', 'unidade_medida', 
            'descricao', 'ativa', 'created_at', 'updated_at', 'valor_formatado', 
            'status_text', 'info_completa', 'usuario_nome'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_valor_por_unidade(self, value):
        """Valida o valor por unidade da despesa"""
        if value is not None and value < 0:
            raise serializers.ValidationError("O valor por unidade não pode ser negativo.")
        
        if value is not None and value > Decimal('999999.99'):
            raise serializers.ValidationError("O valor por unidade é muito alto.")
        
        return value

    def validate_nome(self, value):
        """Valida o nome da despesa"""
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da despesa é obrigatório.")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("O nome da despesa deve ter pelo menos 3 caracteres.")
        
        return value.strip()

    def validate_unidade_medida(self, value):
        """Valida a unidade de medida"""
        if not value or not value.strip():
            raise serializers.ValidationError("A unidade de medida é obrigatória.")
        
        if len(value.strip()) < 1:
            raise serializers.ValidationError("A unidade de medida deve ter pelo menos 1 caractere.")
        
        return value.strip()

    def validate(self, attrs):
        """Validações que envolvem múltiplos campos"""
        # Verifica se já existe uma despesa com o mesmo nome para o usuário
        nome = attrs.get('nome')
        usuario = attrs.get('usuario')
        
        if nome and usuario:
            # No caso de update, exclui o objeto atual da verificação
            queryset = DespesaVariavel.objects.filter(usuario=usuario, nome=nome)
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    'nome': 'Já existe uma despesa variável com este nome para este usuário.'
                })
        
        return attrs


class DespesaVariavelCreateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para criação de despesas variáveis.
    Remove campos desnecessários na criação.
    """
    class Meta:
        model = DespesaVariavel
        fields = [
            'nome', 'valor_por_unidade', 'unidade_medida', 'descricao', 'ativa'
        ]

    def validate_valor_por_unidade(self, value):
        """Valida o valor por unidade da despesa"""
        if value is not None and value < 0:
            raise serializers.ValidationError("O valor por unidade não pode ser negativo.")
        
        if value is not None and value > Decimal('999999.99'):
            raise serializers.ValidationError("O valor por unidade é muito alto.")
        
        return value

    def validate_nome(self, value):
        """Valida o nome da despesa"""
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da despesa é obrigatório.")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("O nome da despesa deve ter pelo menos 3 caracteres.")
        
        return value.strip()

    def validate_unidade_medida(self, value):
        """Valida a unidade de medida"""
        if not value or not value.strip():
            raise serializers.ValidationError("A unidade de medida é obrigatória.")
        
        if len(value.strip()) < 1:
            raise serializers.ValidationError("A unidade de medida deve ter pelo menos 1 caractere.")
        
        return value.strip()

    def create(self, validated_data):
        """Cria uma nova despesa variável associada ao usuário autenticado"""
        # O usuário é definido automaticamente na view
        return super().create(validated_data)


class DespesaVariavelUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para atualização de despesas variáveis.
    Permite atualizações parciais.
    """
    class Meta:
        model = DespesaVariavel
        fields = [
            'nome', 'valor_por_unidade', 'unidade_medida', 'descricao', 'ativa'
        ]

    def validate_valor_por_unidade(self, value):
        """Valida o valor por unidade da despesa"""
        if value is not None and value < 0:
            raise serializers.ValidationError("O valor por unidade não pode ser negativo.")
        
        if value is not None and value > Decimal('999999.99'):
            raise serializers.ValidationError("O valor por unidade é muito alto.")
        
        return value

    def validate_nome(self, value):
        """Valida o nome da despesa"""
        if value is not None:
            if not value or not value.strip():
                raise serializers.ValidationError("O nome da despesa é obrigatório.")
            
            if len(value.strip()) < 3:
                raise serializers.ValidationError("O nome da despesa deve ter pelo menos 3 caracteres.")
            
            return value.strip()
        return value

    def validate_unidade_medida(self, value):
        """Valida a unidade de medida"""
        if value is not None:
            if not value or not value.strip():
                raise serializers.ValidationError("A unidade de medida é obrigatória.")
            
            if len(value.strip()) < 1:
                raise serializers.ValidationError("A unidade de medida deve ter pelo menos 1 caractere.")
            
            return value.strip()
        return value


class DespesaVariavelListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de despesas variáveis.
    Usado em listas com muitos itens para otimizar performance.
    """
    valor_formatado = serializers.ReadOnlyField()
    status_text = serializers.ReadOnlyField()
    info_completa = serializers.ReadOnlyField()

    class Meta:
        model = DespesaVariavel
        fields = [
            'id', 'nome', 'valor_por_unidade', 'unidade_medida', 'ativa', 
            'created_at', 'valor_formatado', 'status_text', 'info_completa'
        ]
