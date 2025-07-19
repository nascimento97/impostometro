from django.contrib import admin
from .models import Produto, ProdutoIngrediente, ProdutoDespesaFixa, ProdutoDespesaVariavel


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'usuario', 'tempo_preparo', 'margem_lucro', 
        'periodo_analise', 'created_at'
    ]
    list_filter = ['created_at', 'tempo_preparo', 'margem_lucro']
    search_fields = ['nome', 'descricao', 'usuario__nome_comercial']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'nome', 'descricao')
        }),
        ('Configurações do Produto', {
            'fields': ('tempo_preparo', 'margem_lucro', 'periodo_analise')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProdutoIngrediente)
class ProdutoIngredienteAdmin(admin.ModelAdmin):
    list_display = ['produto', 'ingrediente', 'quantidade', 'created_at']
    list_filter = ['created_at', 'produto', 'ingrediente']
    search_fields = ['produto__nome', 'ingrediente__nome']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(ProdutoDespesaFixa)
class ProdutoDespesaFixaAdmin(admin.ModelAdmin):
    list_display = ['produto', 'despesa_fixa', 'created_at']
    list_filter = ['created_at', 'produto', 'despesa_fixa']
    search_fields = ['produto__nome', 'despesa_fixa__nome']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(ProdutoDespesaVariavel)
class ProdutoDespesaVariavelAdmin(admin.ModelAdmin):
    list_display = ['produto', 'despesa_variavel', 'quantidade', 'created_at']
    list_filter = ['created_at', 'produto', 'despesa_variavel']
    search_fields = ['produto__nome', 'despesa_variavel__nome']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
