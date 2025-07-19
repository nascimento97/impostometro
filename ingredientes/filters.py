import django_filters
from django.db.models import Q
from .models import Ingrediente


class IngredienteFilter(django_filters.FilterSet):
    """
    Filtros personalizados para o modelo Ingrediente.
    """
    # Filtro de busca que procura em vários campos
    search = django_filters.CharFilter(
        method='filter_search',
        label='Buscar'
    )
    
    # Filtro por preço mínimo e máximo
    preco_min = django_filters.NumberFilter(
        field_name='preco_por_unidade',
        lookup_expr='gte',
        label='Preço por unidade (mínimo)'
    )
    
    preco_max = django_filters.NumberFilter(
        field_name='preco_por_unidade',
        lookup_expr='lte',
        label='Preço por unidade (máximo)'
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
        model = Ingrediente
        fields = {
            'unidade_medida': ['exact', 'icontains'],
            'fornecedor': ['exact', 'icontains'],
            'nome': ['exact', 'icontains'],
            'preco_por_unidade': ['exact', 'gte', 'lte'],
        }

    def filter_search(self, queryset, name, value):
        """
        Filtro de busca personalizado que procura em múltiplos campos.
        """
        if value:
            return queryset.filter(
                Q(nome__icontains=value) |
                Q(fornecedor__icontains=value) |
                Q(unidade_medida__icontains=value)
            )
        return queryset
