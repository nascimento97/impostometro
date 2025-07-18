from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Usuario
import re


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Usuario.
    Usado para listagem e detalhes de usuários.
    """
    nome_completo = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'nome_comercial', 'telefone', 'cnpj', 'endereco',
            'is_active', 'date_joined', 'created_at', 'updated_at',
            'nome_completo', 'password', 'confirm_password'
        ]
        read_only_fields = ['id', 'date_joined', 'created_at', 'updated_at']
        extra_kwargs = {
            'email': {'required': True},
            'nome_comercial': {'required': True},
        }

    def validate_email(self, value):
        """Valida se o email é único"""
        if self.instance:
            # Se estamos atualizando, excluir o usuário atual da verificação
            if Usuario.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("Este email já está em uso.")
        else:
            # Se estamos criando, verificar se já existe
            if Usuario.objects.filter(email=value).exists():
                raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate_cnpj(self, value):
        """Valida o formato do CNPJ"""
        if value:
            # Remove caracteres não numéricos
            cnpj_limpo = ''.join(filter(str.isdigit, value))
            
            if len(cnpj_limpo) != 14:
                raise serializers.ValidationError("CNPJ deve ter 14 dígitos.")
            
            # Verifica se não é uma sequência de números iguais
            if len(set(cnpj_limpo)) == 1:
                raise serializers.ValidationError("CNPJ inválido.")
            
            # Formata o CNPJ
            value = f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return value

    def validate_telefone(self, value):
        """Valida o formato do telefone"""
        if value:
            # Remove caracteres não numéricos
            telefone_limpo = ''.join(filter(str.isdigit, value))
            
            if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
                raise serializers.ValidationError(
                    "Telefone deve ter entre 10 e 11 dígitos."
                )
        return value

    def validate(self, attrs):
        """Validações que envolvem múltiplos campos"""
        # Validar confirmação de senha
        if 'password' in attrs and 'confirm_password' in attrs:
            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError({
                    'confirm_password': 'As senhas não coincidem.'
                })
        
        # Validar senha usando os validadores do Django
        if 'password' in attrs:
            try:
                validate_password(attrs['password'])
            except ValidationError as e:
                raise serializers.ValidationError({'password': e.messages})

        return attrs

    def create(self, validated_data):
        """Cria um novo usuário"""
        # Remove confirm_password dos dados validados
        validated_data.pop('confirm_password', None)
        
        # Extrai a senha para hash
        password = validated_data.pop('password')
        
        # Cria o usuário
        usuario = Usuario.objects.create_user(
            password=password,
            **validated_data
        )
        
        return usuario

    def update(self, instance, validated_data):
        """Atualiza um usuário existente"""
        # Remove confirm_password dos dados validados
        validated_data.pop('confirm_password', None)
        
        # Se uma nova senha foi fornecida
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        # Atualiza os outros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class UsuarioCreateSerializer(UsuarioSerializer):
    """
    Serializer específico para criação de usuários.
    Inclui validações mais rigorosas.
    """
    class Meta(UsuarioSerializer.Meta):
        extra_kwargs = {
            **UsuarioSerializer.Meta.extra_kwargs,
            'password': {'required': True, 'write_only': True},
            'confirm_password': {'required': True, 'write_only': True},
        }


class UsuarioUpdateSerializer(UsuarioSerializer):
    """
    Serializer específico para atualização de usuários.
    Senha não é obrigatória na atualização.
    """
    password = serializers.CharField(
        write_only=True, 
        required=False,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True, 
        required=False,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validações específicas para atualização"""
        # Se password foi fornecido, confirm_password também deve ser
        if 'password' in attrs and not attrs.get('confirm_password'):
            raise serializers.ValidationError({
                'confirm_password': 'Confirmação de senha é obrigatória quando alterando a senha.'
            })
        
        return super().validate(attrs)


class UsuarioListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de usuários.
    Não inclui campos sensíveis.
    """
    nome_completo = serializers.ReadOnlyField()

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'nome_completo', 
            'nome_comercial', 'is_active', 'created_at'
        ]
