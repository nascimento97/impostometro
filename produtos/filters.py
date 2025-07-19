import django_filters
from django.db.models import Q
from .models import Produto


class ProdutoFilter(django_filters.FilterSet):
    """
    Filtros personalizados para o modelo Produto.
    """
    # Filtro de busca que procura em vários campos
    search = django_filters.CharFilter(
        method='filter_search',
        label='Buscar'
    )
    
    # Filtro por tempo de preparo mínimo e máximo
    tempo_preparo_min = django_filters.NumberFilter(
        field_name='tempo_preparo',
        lookup_expr='gte',
        label='Tempo de preparo (mínimo em minutos)'
    )
    
    tempo_preparo_max = django_filters.NumberFilter(
        field_name='tempo_preparo',
        lookup_expr='lte',
        label='Tempo de preparo (máximo em minutos)'
    )
    
    # Filtro por margem de lucro mínima e máxima
    margem_lucro_min = django_filters.NumberFilter(
        field_name='margem_lucro',
        lookup_expr='gte',
        label='Margem de lucro (mínima em %)'
    )
    
    margem_lucro_max = django_filters.NumberFilter(
        field_name='margem_lucro',
        lookup_expr='lte',
        label='Margem de lucro (máxima em %)'
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
    
    # Filtro por data de atualização
    data_atualizacao_inicio = django_filters.DateFilter(
        field_name='updated_at',
        lookup_expr='gte',
        label='Data de atualização (início)'
    )
    
    data_atualizacao_fim = django_filters.DateFilter(
        field_name='updated_at',
        lookup_expr='lte',
        label='Data de atualização (fim)'
    )

    class Meta:
        model = Produto
        fields = {
            'nome': ['exact', 'icontains'],
            'descricao': ['icontains'],
            'tempo_preparo': ['exact', 'gte', 'lte'],
            'margem_lucro': ['exact', 'gte', 'lte'],
            'periodo_analise': ['exact', 'icontains'],
        }

    def filter_search(self, queryset, name, value):
        """
        Filtro de busca personalizado que procura em múltiplos campos.
        """
        if value:
            return queryset.filter(
                Q(nome__icontains=value) |
                Q(descricao__icontains=value) |
                Q(periodo_analise__icontains=value)
            )
        return queryset
