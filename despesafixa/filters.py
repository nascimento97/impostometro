import django_filters
from django.db.models import Q
from .models import DespesaFixa


class DespesaFixaFilter(django_filters.FilterSet):
    """
    Filtros personalizados para o modelo DespesaFixa.
    """
    # Filtro de busca que procura em vários campos
    search = django_filters.CharFilter(
        method='filter_search',
        label='Buscar'
    )
    
    # Filtro por valor mínimo e máximo
    valor_min = django_filters.NumberFilter(
        field_name='valor',
        lookup_expr='gte',
        label='Valor mínimo'
    )
    
    valor_max = django_filters.NumberFilter(
        field_name='valor',
        lookup_expr='lte',
        label='Valor máximo'
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
        model = DespesaFixa
        fields = {
            'ativa': ['exact'],
            'nome': ['exact', 'icontains'],
            'descricao': ['icontains'],
            'valor': ['exact', 'gte', 'lte'],
        }

    def filter_search(self, queryset, name, value):
        """
        Filtro de busca personalizado que procura em múltiplos campos.
        """
        if value:
            return queryset.filter(
                Q(nome__icontains=value) |
                Q(descricao__icontains=value)
            )
        return queryset
