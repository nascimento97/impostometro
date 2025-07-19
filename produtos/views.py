from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Sum, Avg
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from .models import Produto, ProdutoIngrediente, ProdutoDespesaFixa, ProdutoDespesaVariavel
from .serializers import (
    ProdutoSerializer,
    ProdutoCreateSerializer,
    ProdutoUpdateSerializer,
    ProdutoListSerializer,
    ProdutoDetalhadoSerializer,
    ProdutoIngredienteSerializer,
    ProdutoDespesaFixaSerializer,
    ProdutoDespesaVariavelSerializer
)


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo de produtos.
    
    Fornece operações CRUD completas:
    - GET /produtos/ - Lista todos os produtos do usuário
    - POST /produtos/ - Cria um novo produto
    - GET /produtos/{id}/ - Detalhes de um produto específico
    - PUT /produtos/{id}/ - Atualiza completamente um produto
    - PATCH /produtos/{id}/ - Atualiza parcialmente um produto
    - DELETE /produtos/{id}/ - Remove um produto
    
    Endpoints adicionais:
    - GET /produtos/search/ - Busca produtos por nome
    - GET /produtos/stats/ - Estatísticas dos produtos
    - POST /produtos/{id}/duplicar/ - Duplica um produto
    - GET /produtos/{id}/calcular/ - Calcula custos do produto
    """
    
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tempo_preparo', 'periodo_analise']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'tempo_preparo', 'margem_lucro', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Retorna apenas os produtos do usuário autenticado.
        """
        return Produto.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        """
        Retorna o serializer apropriado baseado na ação.
        """
        if self.action == 'create':
            return ProdutoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProdutoUpdateSerializer
        elif self.action == 'list':
            return ProdutoListSerializer
        elif self.action == 'retrieve':
            return ProdutoDetalhadoSerializer
        return ProdutoSerializer

    def perform_create(self, serializer):
        """
        Sobrescreve o método para definir o usuário automaticamente ao criar.
        """
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Endpoint para buscar produtos por nome.
        GET /api/produtos/search/?q=termo_busca
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({
                'error': 'Parâmetro de busca "q" é obrigatório'
            }, status=status.HTTP_400_BAD_REQUEST)

        produtos = self.get_queryset().filter(
            Q(nome__icontains=query) | Q(descricao__icontains=query)
        )

        serializer = ProdutoListSerializer(produtos, many=True)
        return Response({
            'count': produtos.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Endpoint para obter estatísticas dos produtos do usuário.
        GET /api/produtos/stats/
        """
        produtos = self.get_queryset()
        
        stats = {
            'total_produtos': produtos.count(),
            'tempo_preparo_medio': produtos.aggregate(
                media=Avg('tempo_preparo')
            )['media'] or 0,
            'margem_lucro_media': produtos.aggregate(
                media=Avg('margem_lucro')
            )['media'] or 0,
            'periodo_analise_medio': produtos.aggregate(
                media=Avg('periodo_analise')
            )['media'] or 0,
            'produto_mais_complexo': None,
            'produto_maior_margem': None
        }

        # Produto com maior tempo de preparo
        produto_complexo = produtos.order_by('-tempo_preparo').first()
        if produto_complexo:
            stats['produto_mais_complexo'] = {
                'id': produto_complexo.id,
                'nome': produto_complexo.nome,
                'tempo_preparo': produto_complexo.tempo_preparo
            }

        # Produto com maior margem de lucro
        produto_maior_margem = produtos.order_by('-margem_lucro').first()
        if produto_maior_margem:
            stats['produto_maior_margem'] = {
                'id': produto_maior_margem.id,
                'nome': produto_maior_margem.nome,
                'margem_lucro': produto_maior_margem.margem_lucro
            }

        return Response(stats)

    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        """
        Endpoint para duplicar um produto.
        POST /api/produtos/{id}/duplicar/
        """
        try:
            produto_original = self.get_object()
            
            # Criar nome único para o produto duplicado
            nome_base = f"Cópia de {produto_original.nome}"
            contador = 1
            nome_novo = nome_base
            
            while Produto.objects.filter(
                usuario=request.user, 
                nome=nome_novo
            ).exists():
                contador += 1
                nome_novo = f"{nome_base} ({contador})"

            # Duplicar o produto principal
            produto_novo = Produto.objects.create(
                usuario=request.user,
                nome=nome_novo,
                descricao=produto_original.descricao,
                tempo_preparo=produto_original.tempo_preparo,
                margem_lucro=produto_original.margem_lucro,
                periodo_analise=produto_original.periodo_analise
            )

            # Duplicar relacionamentos com ingredientes
            for produto_ingrediente in produto_original.produto_ingredientes.all():
                ProdutoIngrediente.objects.create(
                    produto=produto_novo,
                    ingrediente=produto_ingrediente.ingrediente,
                    quantidade=produto_ingrediente.quantidade
                )

            # Duplicar relacionamentos com despesas fixas
            for produto_despesa_fixa in produto_original.produto_despesas_fixas.all():
                ProdutoDespesaFixa.objects.create(
                    produto=produto_novo,
                    despesa_fixa=produto_despesa_fixa.despesa_fixa
                )

            # Duplicar relacionamentos com despesas variáveis
            for produto_despesa_variavel in produto_original.produto_despesas_variaveis.all():
                ProdutoDespesaVariavel.objects.create(
                    produto=produto_novo,
                    despesa_variavel=produto_despesa_variavel.despesa_variavel,
                    quantidade=produto_despesa_variavel.quantidade
                )

            serializer = ProdutoDetalhadoSerializer(produto_novo)
            return Response({
                'message': 'Produto duplicado com sucesso',
                'produto': serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': f'Erro ao duplicar produto: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def calcular(self, request, pk=None):
        """
        Endpoint para calcular custos e análise financeira do produto.
        GET /api/produtos/{id}/calcular/
        """
        produto = self.get_object()
        
        # Calcular custo dos ingredientes
        custo_ingredientes = Decimal('0.00')
        for produto_ingrediente in produto.produto_ingredientes.all():
            custo_ingredientes += produto_ingrediente.custo_total

        # Calcular custo das despesas fixas (rateado pelo período de análise)
        custo_despesas_fixas = Decimal('0.00')
        for produto_despesa_fixa in produto.produto_despesas_fixas.all():
            # Ratear despesa fixa pelo período de análise
            custo_diario = produto_despesa_fixa.despesa_fixa.valor / 30  # Assumindo mês de 30 dias
            custo_despesas_fixas += custo_diario * produto.periodo_analise

        # Calcular custo das despesas variáveis
        custo_despesas_variaveis = Decimal('0.00')
        for produto_despesa_variavel in produto.produto_despesas_variaveis.all():
            custo_despesas_variaveis += produto_despesa_variavel.custo_total

        # Custo total de produção
        custo_total_producao = custo_ingredientes + custo_despesas_fixas + custo_despesas_variaveis

        # Preço de venda com margem de lucro
        margem_decimal = produto.margem_lucro / 100
        preco_venda_sugerido = custo_total_producao * (1 + margem_decimal)

        # Estimativas para o período de análise (assumindo 1 produto por dia)
        quantidade_estimada = produto.periodo_analise
        faturamento_previsto = preco_venda_sugerido * quantidade_estimada
        custo_total_periodo = custo_total_producao * quantidade_estimada
        lucro_previsto = faturamento_previsto - custo_total_periodo

        analise = {
            'produto_id': produto.id,
            'produto_nome': produto.nome,
            'periodo_analise': produto.periodo_analise,
            'margem_lucro': produto.margem_lucro,
            'custos': {
                'ingredientes': float(custo_ingredientes),
                'despesas_fixas': float(custo_despesas_fixas),
                'despesas_variaveis': float(custo_despesas_variaveis),
                'total_producao': float(custo_total_producao)
            },
            'precificacao': {
                'preco_venda_sugerido': float(preco_venda_sugerido),
                'margem_lucro_percentual': float(produto.margem_lucro),
                'margem_lucro_valor': float(preco_venda_sugerido - custo_total_producao)
            },
            'projecoes_periodo': {
                'quantidade_estimada': quantidade_estimada,
                'faturamento_previsto': float(faturamento_previsto),
                'custo_total_periodo': float(custo_total_periodo),
                'lucro_previsto': float(lucro_previsto),
                'roi_percentual': float((lucro_previsto / custo_total_periodo) * 100) if custo_total_periodo > 0 else 0
            },
            'detalhamento_ingredientes': [
                {
                    'nome': pi.ingrediente.nome,
                    'quantidade': float(pi.quantidade),
                    'unidade': pi.ingrediente.unidade_medida,
                    'preco_unitario': float(pi.ingrediente.preco_por_unidade),
                    'custo_total': float(pi.custo_total)
                }
                for pi in produto.produto_ingredientes.all()
            ],
            'detalhamento_despesas_fixas': [
                {
                    'nome': pdf.despesa_fixa.nome,
                    'valor_mensal': float(pdf.despesa_fixa.valor),
                    'valor_rateado': float(pdf.despesa_fixa.valor / 30 * produto.periodo_analise)
                }
                for pdf in produto.produto_despesas_fixas.all()
            ],
            'detalhamento_despesas_variaveis': [
                {
                    'nome': pdv.despesa_variavel.nome,
                    'quantidade': float(pdv.quantidade),
                    'unidade': pdv.despesa_variavel.unidade_medida,
                    'valor_unitario': float(pdv.despesa_variavel.valor_por_unidade),
                    'custo_total': float(pdv.custo_total)
                }
                for pdv in produto.produto_despesas_variaveis.all()
            ]
        }

        return Response(analise)


class ProdutoIngredienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar relacionamentos entre produtos e ingredientes.
    """
    serializer_class = ProdutoIngredienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas os relacionamentos dos produtos do usuário autenticado."""
        return ProdutoIngrediente.objects.filter(produto__usuario=self.request.user)


class ProdutoDespesaFixaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar relacionamentos entre produtos e despesas fixas.
    """
    serializer_class = ProdutoDespesaFixaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas os relacionamentos dos produtos do usuário autenticado."""
        return ProdutoDespesaFixa.objects.filter(produto__usuario=self.request.user)


class ProdutoDespesaVariavelViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar relacionamentos entre produtos e despesas variáveis.
    """
    serializer_class = ProdutoDespesaVariavelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas os relacionamentos dos produtos do usuário autenticado."""
        return ProdutoDespesaVariavel.objects.filter(produto__usuario=self.request.user)
