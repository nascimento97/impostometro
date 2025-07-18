from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuração do admin para o modelo Usuario customizado.
    """
    # Campos a serem exibidos na lista de usuários
    list_display = (
        'username', 'email', 'nome_comercial', 'first_name', 
        'last_name', 'is_active', 'is_staff', 'created_at'
    )
    
    # Campos pelos quais é possível filtrar
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 
        'created_at', 'last_login'
    )
    
    # Campos de busca
    search_fields = (
        'username', 'email', 'nome_comercial', 
        'first_name', 'last_name', 'cnpj'
    )
    
    # Ordenação padrão
    ordering = ('-created_at',)
    
    # Campos somente leitura
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    
    # Configuração dos fieldsets para o formulário de edição
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Informações Comerciais', {
            'fields': ('nome_comercial', 'cnpj', 'telefone', 'endereco')
        }),
        ('Permissões', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 
                'groups', 'user_permissions'
            )
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Configuração dos fieldsets para criação de novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'nome_comercial', 'first_name', 'last_name'
            ),
        }),
        ('Informações Comerciais', {
            'classes': ('wide',),
            'fields': ('cnpj', 'telefone', 'endereco'),
        }),
        ('Permissões', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    # Ações customizadas
    actions = ['ativar_usuarios', 'desativar_usuarios']
    
    def ativar_usuarios(self, request, queryset):
        """Ativa os usuários selecionados"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request, 
            f'{updated} usuário(s) foram ativados com sucesso.'
        )
    ativar_usuarios.short_description = 'Ativar usuários selecionados'
    
    def desativar_usuarios(self, request, queryset):
        """Desativa os usuários selecionados"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request, 
            f'{updated} usuário(s) foram desativados com sucesso.'
        )
    desativar_usuarios.short_description = 'Desativar usuários selecionados'
