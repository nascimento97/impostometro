import django_filters
from django.db.models import Q
from .models import AnaliseFinanceira


class AnaliseFinanceiraFilter(django_filters.FilterSet):
    """
    Filtros personalizados para o modelo AnaliseFinanceira.
    """
    # Filtro de busca que procura em vários campos
    search = django_filters.CharFilter(
        method='filter_search',
        label='Buscar'
    )
    
    # Filtros por custo total de produção
    custo_total_min = django_filters.NumberFilter(
        field_name='custo_total_producao',
        lookup_expr='gte',
        label='Custo total de produção (mínimo)'
    )
    
    custo_total_max = django_filters.NumberFilter(
        field_name='custo_total_producao',
        lookup_expr='lte',
        label='Custo total de produção (máximo)'
    )
    
    # Filtros por preço de venda sugerido
    preco_venda_min = django_filters.NumberFilter(
        field_name='preco_venda_sugerido',
        lookup_expr='gte',
        label='Preço de venda sugerido (mínimo)'
    )
    
    preco_venda_max = django_filters.NumberFilter(
        field_name='preco_venda_sugerido',
        lookup_expr='lte',
        label='Preço de venda sugerido (máximo)'
    )
    
    # Filtros por lucro previsto
    lucro_min = django_filters.NumberFilter(
        field_name='lucro_previsto',
        lookup_expr='gte',
        label='Lucro previsto (mínimo)'
    )
    
    lucro_max = django_filters.NumberFilter(
        field_name='lucro_previsto',
        lookup_expr='lte',
        label='Lucro previsto (máximo)'
    )
    
    # Filtro por data de criação
    data_criacao_inicio = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Data de criação (início)'
    )
    
    data_criacao_fim = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Data de criação (fim)'
    )
    
    # Filtro por ano e mês
    ano = django_filters.NumberFilter(
        field_name='created_at',
        lookup_expr='year',
        label='Ano'
    )
    
    mes = django_filters.NumberFilter(
        field_name='created_at',
        lookup_expr='month',
        label='Mês'
    )

    class Meta:
        model = AnaliseFinanceira
        fields = {
            'produto': ['exact'],
            'custo_total_producao': ['exact', 'gte', 'lte'],
            'preco_venda_sugerido': ['exact', 'gte', 'lte'],
            'lucro_previsto': ['exact', 'gte', 'lte'],
        }

    def filter_search(self, queryset, name, value):
        """
        Filtro de busca personalizado que procura em múltiplos campos.
        """
        if value:
            return queryset.filter(
                Q(produto__nome__icontains=value) |
                Q(produto__descricao__icontains=value)
            )
        return queryset
