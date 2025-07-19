from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Sum, Avg
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from .models import AnaliseFinanceira
from .serializers import (
    AnaliseFinanceiraSerializer,
    AnaliseFinanceiraCreateSerializer,
    AnaliseFinanceiraUpdateSerializer,
    AnaliseFinanceiraListSerializer,
    AnaliseFinanceiraDetalhadaSerializer
)


class AnaliseFinanceiraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo de análises financeiras.
    
    Fornece operações CRUD completas:
    - GET /analises-financeiras/ - Lista todas as análises do usuário
    - POST /analises-financeiras/ - Cria uma nova análise
    - GET /analises-financeiras/{id}/ - Detalhes de uma análise específica
    - PUT /analises-financeiras/{id}/ - Atualiza completamente uma análise
    - PATCH /analises-financeiras/{id}/ - Atualiza parcialmente uma análise
    - DELETE /analises-financeiras/{id}/ - Remove uma análise
    
    Ações customizadas:
    - GET /analises-financeiras/stats/ - Estatísticas das análises
    - POST /analises-financeiras/comparar/ - Comparar análises
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtros disponíveis
    filterset_fields = {
        'produto': ['exact'],
        'custo_total_producao': ['gte', 'lte'],
        'preco_venda_sugerido': ['gte', 'lte'],
        'lucro_previsto': ['gte', 'lte'],
        'created_at': ['date__gte', 'date__lte', 'year', 'month']
    }
    
    # Campos de busca
    search_fields = ['produto__nome', 'produto__descricao']
    
    # Campos de ordenação
    ordering_fields = [
        'created_at', 'custo_total_producao', 'preco_venda_sugerido',
        'lucro_previsto', 'faturamento_previsto'
    ]
    ordering = ['-created_at']  # Ordenação padrão

    def get_queryset(self):
        """
        Retorna apenas as análises financeiras do usuário logado.
        Inclui otimizações de consulta para melhor performance.
        """
        return AnaliseFinanceira.objects.filter(
            produto__usuario=self.request.user
        ).select_related(
            'produto', 'produto__usuario'
        ).order_by('-created_at')

    def get_serializer_class(self):
        """
        Retorna o serializer apropriado baseado na ação.
        """
        if self.action == 'list':
            return AnaliseFinanceiraListSerializer
        elif self.action == 'create':
            return AnaliseFinanceiraCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AnaliseFinanceiraUpdateSerializer
        elif self.action == 'retrieve':
            return AnaliseFinanceiraDetalhadaSerializer
        return AnaliseFinanceiraSerializer

    def perform_create(self, serializer):
        """
        Garante que a análise seja criada para um produto do usuário logado.
        """
        # O serializer já valida se o produto pertence ao usuário
        serializer.save()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Retorna estatísticas das análises financeiras do usuário.
        
        GET /api/analises-financeiras/stats/
        """
        queryset = self.get_queryset()
        
        stats = queryset.aggregate(
            total_analises=Count('id'),
            custo_medio=Avg('custo_total_producao'),
            preco_medio=Avg('preco_venda_sugerido'),
            lucro_total=Sum('lucro_previsto'),
            faturamento_total=Sum('faturamento_previsto')
        )
        
        # Adiciona estatísticas de margem de lucro
        analises_com_margem = []
        for analise in queryset:
            if analise.custo_total_producao > 0:
                margem = ((analise.preco_venda_sugerido - analise.custo_total_producao) / 
                         analise.custo_total_producao) * 100
                analises_com_margem.append(margem)
        
        if analises_com_margem:
            stats['margem_lucro_media'] = sum(analises_com_margem) / len(analises_com_margem)
            stats['margem_lucro_maxima'] = max(analises_com_margem)
            stats['margem_lucro_minima'] = min(analises_com_margem)
        else:
            stats['margem_lucro_media'] = 0
            stats['margem_lucro_maxima'] = 0
            stats['margem_lucro_minima'] = 0
        
        # Produtos mais analisados
        produtos_mais_analisados = queryset.values(
            'produto__nome'
        ).annotate(
            total_analises=Count('id')
        ).order_by('-total_analises')[:5]
        
        stats['produtos_mais_analisados'] = produtos_mais_analisados
        
        return Response(stats)

    @action(detail=False, methods=['post'])
    def comparar(self, request):
        """
        Compara múltiplas análises financeiras.
        
        POST /api/analises-financeiras/comparar/
        Body: {"analises_ids": [1, 2, 3]}
        """
        analises_ids = request.data.get('analises_ids', [])
        
        if not analises_ids or len(analises_ids) < 2:
            return Response(
                {'error': 'É necessário fornecer pelo menos 2 IDs de análises para comparação.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(analises_ids) > 10:
            return Response(
                {'error': 'Máximo de 10 análises podem ser comparadas por vez.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Busca as análises do usuário
        analises = self.get_queryset().filter(id__in=analises_ids)
        
        if len(analises) != len(analises_ids):
            return Response(
                {'error': 'Uma ou mais análises não foram encontradas ou não pertencem ao usuário.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serializa as análises para comparação
        serializer = AnaliseFinanceiraDetalhadaSerializer(analises, many=True)
        
        # Calcula estatísticas comparativas
        comparacao = {
            'analises': serializer.data,
            'resumo_comparativo': {
                'menor_custo': min(analises, key=lambda x: x.custo_total_producao),
                'maior_custo': max(analises, key=lambda x: x.custo_total_producao),
                'menor_preco': min(analises, key=lambda x: x.preco_venda_sugerido),
                'maior_preco': max(analises, key=lambda x: x.preco_venda_sugerido),
                'maior_lucro': max(analises, key=lambda x: x.lucro_previsto),
                'menor_lucro': min(analises, key=lambda x: x.lucro_previsto),
            }
        }
        
        # Converte objetos para dicionários serializáveis
        for key, analise in comparacao['resumo_comparativo'].items():
            comparacao['resumo_comparativo'][key] = {
                'id': analise.id,
                'produto_nome': analise.produto.nome,
                'valor': getattr(analise, {
                    'menor_custo': 'custo_total_producao',
                    'maior_custo': 'custo_total_producao',
                    'menor_preco': 'preco_venda_sugerido',
                    'maior_preco': 'preco_venda_sugerido',
                    'maior_lucro': 'lucro_previsto',
                    'menor_lucro': 'lucro_previsto',
                }[key])
            }
        
        return Response(comparacao)

    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        """
        Duplica uma análise financeira existente.
        
        POST /api/analises-financeiras/{id}/duplicar/
        """
        analise_original = self.get_object()
        
        # Cria uma nova análise baseada na original
        nova_analise = AnaliseFinanceira.objects.create(
            produto=analise_original.produto,
            custo_ingredientes=analise_original.custo_ingredientes,
            custo_despesas_fixas=analise_original.custo_despesas_fixas,
            custo_despesas_variaveis=analise_original.custo_despesas_variaveis,
            preco_venda_sugerido=analise_original.preco_venda_sugerido,
            faturamento_previsto=analise_original.faturamento_previsto,
            lucro_previsto=analise_original.lucro_previsto
        )
        
        serializer = AnaliseFinanceiraDetalhadaSerializer(nova_analise)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def relatorio(self, request, pk=None):
        """
        Gera um relatório detalhado da análise financeira.
        
        GET /api/analises-financeiras/{id}/relatorio/
        """
        analise = self.get_object()
        
        relatorio = {
            'analise': AnaliseFinanceiraDetalhadaSerializer(analise).data,
            'breakdown_custos': {
                'ingredientes': {
                    'valor': analise.custo_ingredientes,
                    'percentual': (analise.custo_ingredientes / analise.custo_total_producao * 100) if analise.custo_total_producao > 0 else 0
                },
                'despesas_fixas': {
                    'valor': analise.custo_despesas_fixas,
                    'percentual': (analise.custo_despesas_fixas / analise.custo_total_producao * 100) if analise.custo_total_producao > 0 else 0
                },
                'despesas_variaveis': {
                    'valor': analise.custo_despesas_variaveis,
                    'percentual': (analise.custo_despesas_variaveis / analise.custo_total_producao * 100) if analise.custo_total_producao > 0 else 0
                }
            },
            'metricas': {
                'margem_lucro_percentual': analise.margem_lucro_real,
                'markup': (analise.preco_venda_sugerido / analise.custo_total_producao * 100) if analise.custo_total_producao > 0 else 0,
                'retorno_investimento': (analise.lucro_previsto / analise.custo_total_producao * 100) if analise.custo_total_producao > 0 else 0
            }
        }
        
        return Response(relatorio)
