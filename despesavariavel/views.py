from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Sum
from .models import DespesaVariavel
from .serializers import (
    DespesaVariavelSerializer,
    DespesaVariavelCreateSerializer,
    DespesaVariavelUpdateSerializer,
    DespesaVariavelListSerializer
)


class DespesaVariavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo de despesas variáveis.
    
    Fornece operações CRUD completas:
    - GET /despesas-variaveis/ - Lista todas as despesas variáveis do usuário
    - POST /despesas-variaveis/ - Cria uma nova despesa variável
    - GET /despesas-variaveis/{id}/ - Detalhes de uma despesa variável específica
    - PUT /despesas-variaveis/{id}/ - Atualiza completamente uma despesa variável
    - PATCH /despesas-variaveis/{id}/ - Atualiza parcialmente uma despesa variável
    - DELETE /despesas-variaveis/{id}/ - Remove uma despesa variável
    
    Endpoints adicionais:
    - GET /despesas-variaveis/ativas/ - Lista apenas despesas variáveis ativas
    - POST /despesas-variaveis/{id}/toggle-status/ - Ativa/desativa uma despesa variável
    - GET /despesas-variaveis/por-unidade/ - Lista despesas agrupadas por unidade de medida
    - GET /despesas-variaveis/estatisticas/ - Retorna estatísticas das despesas variáveis
    """
    serializer_class = DespesaVariavelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ativa', 'unidade_medida', 'created_at']
    search_fields = ['nome', 'descricao', 'unidade_medida']
    ordering_fields = ['nome', 'valor_por_unidade', 'unidade_medida', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Retorna apenas as despesas variáveis do usuário autenticado.
        """
        return DespesaVariavel.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        """
        Define o serializer baseado na ação.
        """
        if self.action == 'create':
            return DespesaVariavelCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DespesaVariavelUpdateSerializer
        elif self.action == 'list':
            return DespesaVariavelListSerializer
        return DespesaVariavelSerializer

    def perform_create(self, serializer):
        """
        Define o usuário automaticamente na criação.
        """
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        """
        Mantém o usuário na atualização.
        """
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def ativas(self, request):
        """
        Retorna apenas as despesas variáveis ativas do usuário.
        """
        despesas_ativas = self.get_queryset().filter(ativa=True)
        serializer = DespesaVariavelListSerializer(despesas_ativas, many=True)
        return Response({
            'count': despesas_ativas.count(),
            'results': serializer.data
        })

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        Alterna o status ativo/inativo de uma despesa variável.
        """
        despesa = self.get_object()
        despesa.ativa = not despesa.ativa
        despesa.save()
        
        serializer = DespesaVariavelSerializer(despesa)
        return Response({
            'message': f'Despesa variável {"ativada" if despesa.ativa else "desativada"} com sucesso.',
            'despesa': serializer.data
        })

    @action(detail=False, methods=['get'])
    def por_unidade(self, request):
        """
        Retorna despesas variáveis agrupadas por unidade de medida.
        """
        queryset = self.get_queryset().filter(ativa=True)
        
        # Agrupa por unidade de medida
        unidades = {}
        for despesa in queryset:
            unidade = despesa.unidade_medida
            if unidade not in unidades:
                unidades[unidade] = []
            unidades[unidade].append({
                'id': despesa.id,
                'nome': despesa.nome,
                'valor_por_unidade': despesa.valor_por_unidade,
                'valor_formatado': despesa.valor_formatado,
                'descricao': despesa.descricao
            })
        
        return Response({
            'unidades_medida': unidades,
            'total_unidades': len(unidades)
        })

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        Retorna estatísticas das despesas variáveis do usuário.
        """
        queryset = self.get_queryset()
        ativas = queryset.filter(ativa=True)
        inativas = queryset.filter(ativa=False)
        
        # Estatísticas básicas
        stats = {
            'total_despesas': queryset.count(),
            'despesas_ativas': ativas.count(),
            'despesas_inativas': inativas.count(),
            'unidades_medida_diferentes': queryset.values('unidade_medida').distinct().count(),
        }
        
        # Valor médio por unidade (apenas ativas)
        if ativas.exists():
            valores = [d.valor_por_unidade for d in ativas if d.valor_por_unidade]
            if valores:
                stats['valor_medio_por_unidade'] = sum(valores) / len(valores)
                stats['valor_minimo'] = min(valores)
                stats['valor_maximo'] = max(valores)
            else:
                stats['valor_medio_por_unidade'] = 0
                stats['valor_minimo'] = 0
                stats['valor_maximo'] = 0
        else:
            stats['valor_medio_por_unidade'] = 0
            stats['valor_minimo'] = 0
            stats['valor_maximo'] = 0
        
        # Unidades de medida mais utilizadas
        unidades_stats = {}
        for despesa in ativas:
            unidade = despesa.unidade_medida
            if unidade in unidades_stats:
                unidades_stats[unidade] += 1
            else:
                unidades_stats[unidade] = 1
        
        # Ordena por quantidade de uso
        unidades_ordenadas = sorted(
            unidades_stats.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        stats['unidades_mais_utilizadas'] = [
            {'unidade': unidade, 'quantidade': qtd} 
            for unidade, qtd in unidades_ordenadas[:5]
        ]
        
        return Response(stats)

    def destroy(self, request, *args, **kwargs):
        """
        Remove uma despesa variável com mensagem personalizada.
        """
        instance = self.get_object()
        nome_despesa = instance.nome
        self.perform_destroy(instance)
        return Response({
            'message': f'Despesa variável "{nome_despesa}" removida com sucesso.'
        }, status=status.HTTP_200_OK)
