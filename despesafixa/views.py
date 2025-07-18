from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import DespesaFixa
from .serializers import (
    DespesaFixaSerializer,
    DespesaFixaCreateSerializer,
    DespesaFixaUpdateSerializer,
    DespesaFixaListSerializer
)


class DespesaFixaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo de despesas fixas.
    
    Fornece operações CRUD completas:
    - GET /despesas-fixas/ - Lista todas as despesas fixas do usuário
    - POST /despesas-fixas/ - Cria uma nova despesa fixa
    - GET /despesas-fixas/{id}/ - Detalhes de uma despesa fixa específica
    - PUT /despesas-fixas/{id}/ - Atualiza completamente uma despesa fixa
    - PATCH /despesas-fixas/{id}/ - Atualiza parcialmente uma despesa fixa
    - DELETE /despesas-fixas/{id}/ - Remove uma despesa fixa
    
    Endpoints adicionais:
    - GET /despesas-fixas/ativas/ - Lista apenas despesas fixas ativas
    - POST /despesas-fixas/{id}/toggle-status/ - Ativa/desativa uma despesa fixa
    - GET /despesas-fixas/total/ - Calcula o total das despesas fixas ativas
    """
    serializer_class = DespesaFixaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ativa', 'created_at']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'valor', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Retorna apenas as despesas fixas do usuário autenticado.
        """
        return DespesaFixa.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        """
        Define o serializer baseado na ação.
        """
        if self.action == 'create':
            return DespesaFixaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DespesaFixaUpdateSerializer
        elif self.action == 'list':
            return DespesaFixaListSerializer
        return DespesaFixaSerializer

    def perform_create(self, serializer):
        """
        Associa a despesa fixa ao usuário autenticado ao criar.
        """
        serializer.save(usuario=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Cria uma nova despesa fixa.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Retorna a resposta com o serializer completo
        response_serializer = DespesaFixaSerializer(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            response_serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        Atualiza uma despesa fixa.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Retorna a resposta com o serializer completo
        response_serializer = DespesaFixaSerializer(serializer.instance)
        return Response(response_serializer.data)

    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """
        Lista apenas as despesas fixas ativas do usuário.
        
        GET /api/despesas-fixas/ativas/
        """
        queryset = self.get_queryset().filter(ativa=True)
        
        # Aplicar filtros de busca se fornecidos
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) | Q(descricao__icontains=search)
            )
        
        # Ordenação
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DespesaFixaListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = DespesaFixaListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        Alterna o status ativo/inativo de uma despesa fixa.
        
        POST /api/despesas-fixas/{id}/toggle-status/
        """
        despesa = self.get_object()
        despesa.ativa = not despesa.ativa
        despesa.save()
        
        serializer = DespesaFixaSerializer(despesa)
        return Response({
            'message': f'Despesa fixa {"ativada" if despesa.ativa else "desativada"} com sucesso.',
            'despesa': serializer.data
        })

    @action(detail=False, methods=['get'])
    def total(self, request):
        """
        Calcula o total das despesas fixas ativas do usuário.
        
        GET /api/despesas-fixas/total/
        """
        queryset = self.get_queryset().filter(ativa=True)
        total = sum(despesa.valor for despesa in queryset)
        
        return Response({
            'total_despesas_fixas': total,
            'total_formatado': f"R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            'quantidade_despesas': queryset.count()
        })

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        Retorna estatísticas das despesas fixas do usuário.
        
        GET /api/despesas-fixas/estatisticas/
        """
        queryset = self.get_queryset()
        ativas = queryset.filter(ativa=True)
        inativas = queryset.filter(ativa=False)
        
        total_ativas = sum(despesa.valor for despesa in ativas)
        total_inativas = sum(despesa.valor for despesa in inativas)
        total_geral = total_ativas + total_inativas
        
        return Response({
            'total': {
                'quantidade': queryset.count(),
                'valor': total_geral,
                'valor_formatado': f"R$ {total_geral:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            },
            'ativas': {
                'quantidade': ativas.count(),
                'valor': total_ativas,
                'valor_formatado': f"R$ {total_ativas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            },
            'inativas': {
                'quantidade': inativas.count(),
                'valor': total_inativas,
                'valor_formatado': f"R$ {total_inativas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            }
        })
