from django.contrib import admin
from .models import AnaliseFinanceira


@admin.register(AnaliseFinanceira)
class AnaliseFinanceiraAdmin(admin.ModelAdmin):
    """
    Configuração do admin para AnaliseFinanceira.
    """
    list_display = [
        'id', 'produto', 'get_usuario', 'custo_total_producao',
        'preco_venda_sugerido', 'lucro_previsto', 'margem_lucro_formatada',
        'created_at'
    ]
    list_filter = [
        'created_at', 'produto__usuario', 'custo_total_producao',
        'preco_venda_sugerido', 'lucro_previsto'
    ]
    search_fields = [
        'produto__nome', 'produto__descricao',
        'produto__usuario__username', 'produto__usuario__nome_comercial'
    ]
    readonly_fields = [
        'custo_total_producao', 'margem_lucro_real', 'margem_lucro_formatada',
        'custo_total_formatado', 'preco_venda_formatado', 'lucro_formatado',
        'faturamento_formatado', 'created_at'
    ]
    fieldsets = (
        ('Produto', {
            'fields': ('produto',)
        }),
        ('Custos', {
            'fields': (
                'custo_ingredientes', 'custo_despesas_fixas',
                'custo_despesas_variaveis', 'custo_total_producao'
            )
        }),
        ('Precificação', {
            'fields': (
                'preco_venda_sugerido', 'margem_lucro_real',
                'margem_lucro_formatada'
            )
        }),
        ('Projeções', {
            'fields': (
                'faturamento_previsto', 'lucro_previsto'
            )
        }),
        ('Metadados', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_per_page = 25
    list_max_show_all = 100

    def get_usuario(self, obj):
        """Retorna o nome comercial do usuário proprietário do produto"""
        return obj.produto.usuario.nome_comercial
    get_usuario.short_description = 'Usuário'
    get_usuario.admin_order_field = 'produto__usuario__nome_comercial'

    def get_queryset(self, request):
        """Otimiza as consultas incluindo related objects"""
        return super().get_queryset(request).select_related(
            'produto', 'produto__usuario'
        )
