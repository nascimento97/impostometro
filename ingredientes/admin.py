from django.contrib import admin
from .models import Ingrediente


@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Ingrediente.
    """
    list_display = [
        'nome', 'usuario', 'preco_por_unidade', 'unidade_medida', 
        'fornecedor', 'created_at'
    ]
    list_filter = [
        'unidade_medida', 'fornecedor', 'created_at', 'usuario'
    ]
    search_fields = [
        'nome', 'fornecedor', 'usuario__username', 'usuario__nome_comercial'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'nome', 'preco_por_unidade', 'unidade_medida')
        }),
        ('Informações Adicionais', {
            'fields': ('fornecedor',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Customiza o queryset para otimizar consultas.
        """
        return super().get_queryset(request).select_related('usuario')
    
    def has_change_permission(self, request, obj=None):
        """
        Permite que usuários editem apenas seus próprios ingredientes.
        """
        if obj is None:
            return True
        return obj.usuario == request.user or request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """
        Permite que usuários deletem apenas seus próprios ingredientes.
        """
        if obj is None:
            return True
        return obj.usuario == request.user or request.user.is_superuser
