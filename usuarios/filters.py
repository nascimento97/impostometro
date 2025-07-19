import django_filters
from django.db.models import Q
from .models import Usuario


class UsuarioFilter(django_filters.FilterSet):
    """
    Filtros personalizados para o modelo Usuario.
    """
    # Filtro de busca que procura em vários campos
    search = django_filters.CharFilter(
        method='filter_search',
        label='Buscar'
    )
    
    # Filtro por data de criação
    data_criacao_inicio = django_filters.DateFilter(
        field_name='date_joined',
        lookup_expr='gte',
        label='Data de criação (início)'
    )
    
    data_criacao_fim = django_filters.DateFilter(
        field_name='date_joined',
        lookup_expr='lte',
        label='Data de criação (fim)'
    )
    
    # Filtro por último login
    ultimo_login_inicio = django_filters.DateFilter(
        field_name='last_login',
        lookup_expr='gte',
        label='Último login (início)'
    )
    
    ultimo_login_fim = django_filters.DateFilter(
        field_name='last_login',
        lookup_expr='lte',
        label='Último login (fim)'
    )

    class Meta:
        model = Usuario
        fields = {
            'is_active': ['exact'],
            'is_staff': ['exact'],
            'is_superuser': ['exact'],
            'username': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'nome_comercial': ['exact', 'icontains'],
            'cnpj': ['exact', 'icontains'],
            'endereco': ['icontains'],
            'telefone': ['exact', 'icontains'],
        }

    def filter_search(self, queryset, name, value):
        """
        Filtro de busca personalizado que procura em múltiplos campos.
        """
        if value:
            return queryset.filter(
                Q(username__icontains=value) |
                Q(email__icontains=value) |
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(nome_comercial__icontains=value) |
                Q(cnpj__icontains=value) |
                Q(endereco__icontains=value) |
                Q(telefone__icontains=value)
            )
        return queryset
