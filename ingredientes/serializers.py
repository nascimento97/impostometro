from rest_framework import serializers
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Ingrediente


class IngredienteSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Ingrediente.
    Usado para listagem e detalhes de ingredientes.
    """
    usuario_nome = serializers.CharField(source='usuario.nome_comercial', read_only=True)
    custo_formatado = serializers.ReadOnlyField()
    info_completa = serializers.ReadOnlyField()

    class Meta:
        model = Ingrediente
        fields = [
            'id', 'usuario', 'nome', 'preco_por_unidade', 'unidade_medida',
            'fornecedor', 'created_at', 'updated_at', 'usuario_nome',
            'custo_formatado', 'info_completa'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_preco_por_unidade(self, value):
        """Validação customizada para preço por unidade"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("O preço não pode ser negativo.")
            if value > Decimal('999999.99'):
                raise serializers.ValidationError("O preço não pode ser superior a R$ 999.999,99.")
        return value

    def validate_unidade_medida(self, value):
        """Validação customizada para unidade de medida"""
        if value:
            value = value.lower().strip()
            if len(value) < 1:
                raise serializers.ValidationError("A unidade de medida é obrigatória.")
            if len(value) > 50:
                raise serializers.ValidationError("A unidade de medida não pode ter mais de 50 caracteres.")
        return value

    def validate_nome(self, value):
        """Validação customizada para nome"""
        if value:
            value = value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("O nome deve ter pelo menos 2 caracteres.")
        return value

    def validate(self, attrs):
        """Validação geral do serializer"""
        # Verificar se já existe um ingrediente com o mesmo nome para o usuário
        if self.instance is None:  # Criação
            usuario = attrs.get('usuario') or (self.context.get('request') and self.context['request'].user)
            nome = attrs.get('nome', '').strip()
            
            if usuario and nome:
                if Ingrediente.objects.filter(usuario=usuario, nome__iexact=nome).exists():
                    raise serializers.ValidationError({
                        'nome': 'Você já possui um ingrediente com este nome.'
                    })
        else:  # Atualização
            nome = attrs.get('nome', self.instance.nome).strip()
            
            if nome and nome.lower() != self.instance.nome.lower():
                if Ingrediente.objects.filter(
                    usuario=self.instance.usuario, 
                    nome__iexact=nome
                ).exclude(id=self.instance.id).exists():
                    raise serializers.ValidationError({
                        'nome': 'Você já possui um ingrediente com este nome.'
                    })
        
        return attrs


class IngredienteCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de ingredientes.
    Remove campos desnecessários e adiciona validações específicas.
    """
    
    class Meta:
        model = Ingrediente
        fields = [
            'nome', 'preco_por_unidade', 'unidade_medida', 'fornecedor'
        ]
        extra_kwargs = {
            'nome': {'required': True},
            'preco_por_unidade': {'required': True},
            'unidade_medida': {'required': True},
        }

    def validate_preco_por_unidade(self, value):
        """Validação customizada para preço por unidade"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("O preço não pode ser negativo.")
            if value > Decimal('999999.99'):
                raise serializers.ValidationError("O preço não pode ser superior a R$ 999.999,99.")
        return value

    def validate_unidade_medida(self, value):
        """Validação customizada para unidade de medida"""
        if value:
            value = value.lower().strip()
            if len(value) < 1:
                raise serializers.ValidationError("A unidade de medida é obrigatória.")
            if len(value) > 50:
                raise serializers.ValidationError("A unidade de medida não pode ter mais de 50 caracteres.")
        return value

    def validate_nome(self, value):
        """Validação customizada para nome"""
        if value:
            value = value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("O nome deve ter pelo menos 2 caracteres.")
        return value

    def create(self, validated_data):
        """Criação do ingrediente com usuário automaticamente definido"""
        # Pega o usuário do contexto da requisição
        usuario = self.context['request'].user
        validated_data['usuario'] = usuario
        return super().create(validated_data)


class IngredienteUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de ingredientes.
    Permite atualização parcial dos campos.
    """
    
    class Meta:
        model = Ingrediente
        fields = [
            'nome', 'preco_por_unidade', 'unidade_medida', 'fornecedor'
        ]

    def validate_preco_por_unidade(self, value):
        """Validação customizada para preço por unidade"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("O preço não pode ser negativo.")
            if value > Decimal('999999.99'):
                raise serializers.ValidationError("O preço não pode ser superior a R$ 999.999,99.")
        return value

    def validate_unidade_medida(self, value):
        """Validação customizada para unidade de medida"""
        if value:
            value = value.lower().strip()
            if len(value) < 1:
                raise serializers.ValidationError("A unidade de medida é obrigatória.")
            if len(value) > 50:
                raise serializers.ValidationError("A unidade de medida não pode ter mais de 50 caracteres.")
        return value

    def validate_nome(self, value):
        """Validação customizada para nome"""
        if value:
            value = value.strip()
            if len(value) < 2:
                raise serializers.ValidationError("O nome deve ter pelo menos 2 caracteres.")
        return value


class IngredienteListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de ingredientes.
    Versão simplificada com menos campos para melhor performance.
    """
    custo_formatado = serializers.ReadOnlyField()
    
    class Meta:
        model = Ingrediente
        fields = [
            'id', 'nome', 'preco_por_unidade', 'unidade_medida',
            'fornecedor', 'custo_formatado', 'created_at'
        ]
