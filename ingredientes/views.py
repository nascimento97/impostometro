from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ingrediente
from .serializers import (
    IngredienteSerializer,
    IngredienteCreateSerializer,
    IngredienteUpdateSerializer,
    IngredienteListSerializer
)


class IngredienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo de ingredientes.
    
    Fornece operações CRUD completas:
    - GET /ingredientes/ - Lista todos os ingredientes do usuário
    - POST /ingredientes/ - Cria um novo ingrediente
    - GET /ingredientes/{id}/ - Detalhes de um ingrediente específico
    - PUT /ingredientes/{id}/ - Atualiza completamente um ingrediente
    - PATCH /ingredientes/{id}/ - Atualiza parcialmente um ingrediente
    - DELETE /ingredientes/{id}/ - Remove um ingrediente
    
    Endpoints adicionais:
    - GET /ingredientes/search/ - Busca ingredientes por nome
    - GET /ingredientes/by_fornecedor/ - Lista ingredientes por fornecedor
    - GET /ingredientes/stats/ - Estatísticas dos ingredientes
    """
    
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unidade_medida', 'fornecedor']
    search_fields = ['nome', 'fornecedor']
    ordering_fields = ['nome', 'preco_por_unidade', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Retorna apenas os ingredientes do usuário autenticado.
        """
        return Ingrediente.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        """
        Retorna o serializer apropriado baseado na ação.
        """
        if self.action == 'create':
            return IngredienteCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return IngredienteUpdateSerializer
        elif self.action == 'list':
            return IngredienteListSerializer
        return IngredienteSerializer

    def create(self, request, *args, **kwargs):
        """
        Cria um novo ingrediente para o usuário autenticado.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ingrediente = serializer.save()
        
        # Retorna o ingrediente criado com o serializer completo
        response_serializer = IngredienteSerializer(ingrediente, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Atualiza um ingrediente existente.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        ingrediente = serializer.save()
        
        # Retorna o ingrediente atualizado com o serializer completo
        response_serializer = IngredienteSerializer(ingrediente, context={'request': request})
        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Remove um ingrediente.
        """
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Ingrediente removido com sucesso.'}, 
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], url_path='search')
    def search_ingredientes(self, request):
        """
        Busca ingredientes por nome ou fornecedor.
        URL: /api/ingredientes/search/?q=termo_busca
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Parâmetro de busca "q" é obrigatório.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ingredientes = self.get_queryset().filter(
            Q(nome__icontains=query) | Q(fornecedor__icontains=query)
        )
        
        serializer = IngredienteListSerializer(ingredientes, many=True)
        return Response({
            'count': ingredientes.count(),
            'query': query,
            'results': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='by-fornecedor')
    def by_fornecedor(self, request):
        """
        Lista ingredientes agrupados por fornecedor.
        URL: /api/ingredientes/by-fornecedor/
        """
        fornecedor = request.query_params.get('fornecedor')
        if not fornecedor:
            return Response(
                {'error': 'Parâmetro "fornecedor" é obrigatório.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ingredientes = self.get_queryset().filter(fornecedor__icontains=fornecedor)
        serializer = IngredienteListSerializer(ingredientes, many=True)
        
        return Response({
            'fornecedor': fornecedor,
            'count': ingredientes.count(),
            'ingredientes': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='stats')
    def estatisticas(self, request):
        """
        Retorna estatísticas dos ingredientes do usuário.
        URL: /api/ingredientes/stats/
        """
        queryset = self.get_queryset()
        
        # Estatísticas básicas
        total_ingredientes = queryset.count()
        ingredientes_com_fornecedor = queryset.exclude(fornecedor__isnull=True, fornecedor__exact='').count()
        
        # Preços
        precos = queryset.values_list('preco_por_unidade', flat=True)
        preco_medio = sum(precos) / len(precos) if precos else 0
        preco_min = min(precos) if precos else 0
        preco_max = max(precos) if precos else 0
        
        # Unidades de medida mais usadas
        unidades = queryset.values_list('unidade_medida', flat=True)
        unidades_contagem = {}
        for unidade in unidades:
            unidades_contagem[unidade] = unidades_contagem.get(unidade, 0) + 1
        
        # Fornecedores mais usados
        fornecedores = queryset.exclude(
            fornecedor__isnull=True, fornecedor__exact=''
        ).values_list('fornecedor', flat=True)
        fornecedores_contagem = {}
        for fornecedor in fornecedores:
            fornecedores_contagem[fornecedor] = fornecedores_contagem.get(fornecedor, 0) + 1
        
        return Response({
            'total_ingredientes': total_ingredientes,
            'ingredientes_com_fornecedor': ingredientes_com_fornecedor,
            'percentual_com_fornecedor': round(
                (ingredientes_com_fornecedor / total_ingredientes * 100) if total_ingredientes > 0 else 0, 2
            ),
            'precos': {
                'medio': round(float(preco_medio), 2),
                'minimo': float(preco_min),
                'maximo': float(preco_max)
            },
            'unidades_mais_usadas': sorted(
                unidades_contagem.items(), key=lambda x: x[1], reverse=True
            )[:5],
            'fornecedores_mais_usados': sorted(
                fornecedores_contagem.items(), key=lambda x: x[1], reverse=True
            )[:5]
        })

    @action(detail=True, methods=['get'], url_path='duplicar')
    def duplicar_ingrediente(self, request, pk=None):
        """
        Duplica um ingrediente existente.
        URL: /api/ingredientes/{id}/duplicar/
        """
        ingrediente_original = self.get_object()
        
        # Cria uma cópia do ingrediente
        novo_nome = f"{ingrediente_original.nome} (Cópia)"
        contador = 1
        
        # Verifica se já existe um ingrediente com este nome
        while Ingrediente.objects.filter(usuario=request.user, nome=novo_nome).exists():
            contador += 1
            novo_nome = f"{ingrediente_original.nome} (Cópia {contador})"
        
        novo_ingrediente = Ingrediente.objects.create(
            usuario=request.user,
            nome=novo_nome,
            preco_por_unidade=ingrediente_original.preco_por_unidade,
            unidade_medida=ingrediente_original.unidade_medida,
            fornecedor=ingrediente_original.fornecedor
        )
        
        serializer = IngredienteSerializer(novo_ingrediente, context={'request': request})
        return Response(
            {
                'message': 'Ingrediente duplicado com sucesso.',
                'ingrediente_original': ingrediente_original.id,
                'novo_ingrediente': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
