from rest_framework import serializers
from decimal import Decimal
from .models import DespesaFixa


class DespesaFixaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo DespesaFixa.
    Usado para listagem e detalhes de despesas fixas.
    """
    valor_formatado = serializers.ReadOnlyField()
    status_text = serializers.ReadOnlyField()
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = DespesaFixa
        fields = [
            'id', 'usuario', 'nome', 'valor', 'descricao', 'ativa',
            'created_at', 'updated_at', 'valor_formatado', 'status_text',
            'usuario_nome'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_valor(self, value):
        """Valida o valor da despesa"""
        if value is not None and value < 0:
            raise serializers.ValidationError("O valor da despesa não pode ser negativo.")
        
        if value is not None and value > Decimal('999999.99'):
            raise serializers.ValidationError("O valor da despesa é muito alto.")
        
        return value

    def validate_nome(self, value):
        """Valida o nome da despesa"""
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da despesa é obrigatório.")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("O nome da despesa deve ter pelo menos 3 caracteres.")
        
        return value.strip()

    def validate(self, attrs):
        """Validações que envolvem múltiplos campos"""
        # Verifica se já existe uma despesa com o mesmo nome para o usuário
        nome = attrs.get('nome')
        usuario = attrs.get('usuario')
        
        if nome and usuario:
            # Se estamos criando uma nova despesa
            if not self.instance:
                if DespesaFixa.objects.filter(usuario=usuario, nome__iexact=nome).exists():
                    raise serializers.ValidationError({
                        'nome': 'Você já possui uma despesa fixa com este nome.'
                    })
            # Se estamos atualizando uma despesa existente
            else:
                if DespesaFixa.objects.filter(
                    usuario=usuario, 
                    nome__iexact=nome
                ).exclude(pk=self.instance.pk).exists():
                    raise serializers.ValidationError({
                        'nome': 'Você já possui uma despesa fixa com este nome.'
                    })
        
        return attrs


class DespesaFixaCreateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para criação de despesas fixas.
    Remove campos desnecessários e define validações específicas.
    """
    
    class Meta:
        model = DespesaFixa
        fields = ['nome', 'valor', 'descricao', 'ativa']

    def validate_valor(self, value):
        """Valida o valor da despesa"""
        if value is None:
            raise serializers.ValidationError("O valor da despesa é obrigatório.")
        
        if value < 0:
            raise serializers.ValidationError("O valor da despesa não pode ser negativo.")
        
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("O valor da despesa é muito alto.")
        
        return value

    def validate_nome(self, value):
        """Valida o nome da despesa"""
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da despesa é obrigatório.")
        
        if len(value.strip()) < 3:
            raise serializers.ValidationError("O nome da despesa deve ter pelo menos 3 caracteres.")
        
        return value.strip()

    def create(self, validated_data):
        """Cria uma nova despesa fixa associando ao usuário autenticado"""
        user = self.context['request'].user
        validated_data['usuario'] = user
        return super().create(validated_data)


class DespesaFixaUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para atualização de despesas fixas.
    Permite atualização parcial dos campos.
    """
    
    class Meta:
        model = DespesaFixa
        fields = ['nome', 'valor', 'descricao', 'ativa']

    def validate_valor(self, value):
        """Valida o valor da despesa"""
        if value is not None and value < 0:
            raise serializers.ValidationError("O valor da despesa não pode ser negativo.")
        
        if value is not None and value > Decimal('999999.99'):
            raise serializers.ValidationError("O valor da despesa é muito alto.")
        
        return value

    def validate_nome(self, value):
        """Valida o nome da despesa"""
        if value is not None:
            if not value.strip():
                raise serializers.ValidationError("O nome da despesa não pode estar vazio.")
            
            if len(value.strip()) < 3:
                raise serializers.ValidationError("O nome da despesa deve ter pelo menos 3 caracteres.")
            
            return value.strip()
        
        return value


class DespesaFixaListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para listagem de despesas fixas.
    Inclui apenas campos essenciais para performance.
    """
    valor_formatado = serializers.ReadOnlyField()
    status_text = serializers.ReadOnlyField()
    
    class Meta:
        model = DespesaFixa
        fields = [
            'id', 'nome', 'valor', 'valor_formatado', 
            'ativa', 'status_text', 'created_at'
        ]
