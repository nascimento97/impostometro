from django.contrib import admin
from .models import DespesaFixa


@admin.register(DespesaFixa)
class DespesaFixaAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo DespesaFixa.
    """
    list_display = [
        'nome', 'usuario', 'valor_formatado', 'ativa', 
        'created_at', 'updated_at'
    ]
    list_filter = [
        'ativa', 'created_at', 'updated_at', 'usuario'
    ]
    search_fields = [
        'nome', 'descricao', 'usuario__username', 
        'usuario__nome_comercial'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'valor_formatado', 'status_text'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'nome', 'valor', 'ativa')
        }),
        ('Detalhes', {
            'fields': ('descricao',),
            'classes': ('collapse',)
        }),
        ('Informações do Sistema', {
            'fields': ('valor_formatado', 'status_text', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Otimiza as consultas incluindo o usuário relacionado"""
        return super().get_queryset(request).select_related('usuario')
    
    def has_change_permission(self, request, obj=None):
        """Permite edição apenas pelo próprio usuário ou superusuário"""
        if obj is not None and not request.user.is_superuser:
            return obj.usuario == request.user
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Permite exclusão apenas pelo próprio usuário ou superusuário"""
        if obj is not None and not request.user.is_superuser:
            return obj.usuario == request.user
        return True
