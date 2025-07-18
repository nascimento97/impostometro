from django.contrib import admin
from .models import DespesaVariavel


@admin.register(DespesaVariavel)
class DespesaVariavelAdmin(admin.ModelAdmin):
    """
    Configuração do admin para DespesaVariavel.
    """
    list_display = ['nome', 'usuario', 'valor_por_unidade', 'unidade_medida', 'ativa', 'created_at']
    list_filter = ['ativa', 'unidade_medida', 'created_at', 'updated_at']
    search_fields = ['nome', 'usuario__username', 'usuario__email', 'descricao', 'unidade_medida']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'nome', 'descricao')
        }),
        ('Valores', {
            'fields': ('valor_por_unidade', 'unidade_medida')
        }),
        ('Status', {
            'fields': ('ativa',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Otimiza consultas incluindo dados do usuário"""
        return super().get_queryset(request).select_related('usuario')
    
    def has_change_permission(self, request, obj=None):
        """Permite edição apenas para superusuários ou proprietários"""
        if request.user.is_superuser:
            return True
        if obj and obj.usuario == request.user:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Permite exclusão apenas para superusuários ou proprietários"""
        if request.user.is_superuser:
            return True
        if obj and obj.usuario == request.user:
            return True
        return False
