from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Usuario
from .filters import UsuarioFilter
from .serializers import (
    UsuarioSerializer, 
    UsuarioCreateSerializer, 
    UsuarioUpdateSerializer,
    UsuarioListSerializer
)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo de usuários.
    
    Fornece operações CRUD completas:
    - GET /usuarios/ - Lista todos os usuários
    - POST /usuarios/ - Cria um novo usuário
    - GET /usuarios/{id}/ - Detalhes de um usuário específico
    - PUT /usuarios/{id}/ - Atualiza completamente um usuário
    - PATCH /usuarios/{id}/ - Atualiza parcialmente um usuário
    - DELETE /usuarios/{id}/ - Remove um usuário
    
    Endpoints adicionais:
    - POST /usuarios/login/ - Login de usuário
    - POST /usuarios/logout/ - Logout de usuário
    - GET /usuarios/me/ - Dados do usuário autenticado
    - PUT /usuarios/me/ - Atualizar dados do usuário autenticado
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UsuarioFilter
    search_fields = ['username', 'first_name', 'last_name', 'email', 'nome_comercial']
    ordering_fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']
    ordering = ['-date_joined']

    @swagger_auto_schema(
        operation_summary="Listar usuários",
        operation_description="""
        Lista todos os usuários do sistema com paginação.
        
        Parâmetros de consulta opcionais:
        - search: Busca por nome, username ou email
        - is_active: Filtrar por usuários ativos (true/false)
        """,
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Buscar por nome, username ou email",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Filtrar por usuários ativos",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={
            200: UsuarioListSerializer(many=True),
            401: openapi.Response(description="Autenticação necessária"),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalhes do usuário",
        operation_description="Retorna os detalhes completos de um usuário específico.",
        responses={
            200: UsuarioSerializer,
            401: openapi.Response(description="Autenticação necessária"),
            404: openapi.Response(description="Usuário não encontrado"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_permissions(self):
        """
        Define permissões baseadas na ação.
        """
        if self.action == 'create' or self.action == 'login':
            # Criação de conta e login são públicos
            permission_classes = [permissions.AllowAny]
        elif self.action in ['me', 'update_me']:
            # Ações do próprio usuário requerem autenticação
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Outras ações requerem autenticação (você pode ajustar conforme necessário)
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Retorna a classe do serializer baseada na ação.
        """
        if self.action == 'create':
            return UsuarioCreateSerializer
        elif self.action in ['update', 'partial_update', 'update_me']:
            return UsuarioUpdateSerializer
        elif self.action == 'list':
            return UsuarioListSerializer
        return UsuarioSerializer

    def get_queryset(self):
        """
        Retorna o queryset padrão de usuários.
        Os filtros são aplicados automaticamente pelo django-filters.
        """
        return Usuario.objects.all()

    @swagger_auto_schema(
        operation_summary="Criar novo usuário",
        operation_description="""
        Cria um novo usuário no sistema.
        
        Após a criação bem-sucedida, retorna automaticamente tokens JWT 
        para que o usuário possa fazer login imediatamente.
        """,
        request_body=UsuarioCreateSerializer,
        responses={
            201: openapi.Response(
                description="Usuário criado com sucesso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'usuario': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(description="Dados inválidos fornecidos"),
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Cria um novo usuário.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        
        # Gera tokens JWT para o usuário recém-criado
        refresh = RefreshToken.for_user(usuario)
        
        return Response({
            'message': 'Usuário criado com sucesso!',
            'usuario': UsuarioSerializer(usuario).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Atualiza um usuário existente.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()

        return Response({
            'message': 'Usuário atualizado com sucesso!',
            'usuario': UsuarioSerializer(usuario).data
        })

    def destroy(self, request, *args, **kwargs):
        """
        Remove um usuário (soft delete - marca como inativo).
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        
        return Response({
            'message': 'Usuário desativado com sucesso!'
        }, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        method='post',
        operation_summary="Login de usuário",
        operation_description="""
        Realiza o login do usuário no sistema.
        
        Aceita login por username ou email.
        Retorna tokens JWT para autenticação nas próximas requisições.
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Username ou email do usuário'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Senha do usuário'
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login realizado com sucesso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'usuario': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                    }
                )
            ),
            400: openapi.Response(description="Dados obrigatórios não fornecidos"),
            401: openapi.Response(description="Credenciais inválidas"),
        }
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Endpoint para login de usuário.
        
        POST /usuarios/login/
        {
            "username": "usuario",
            "password": "senha"
        }
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': 'Username e password são obrigatórios.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Tenta autenticar com username ou email
        user = authenticate(username=username, password=password)
        if not user:
            # Tenta com email se o username falhou
            try:
                usuario_obj = Usuario.objects.get(email=username)
                user = authenticate(username=usuario_obj.username, password=password)
            except Usuario.DoesNotExist:
                pass

        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login realizado com sucesso!',
                'usuario': UsuarioSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        else:
            return Response({
                'error': 'Credenciais inválidas ou usuário inativo.'
            }, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Endpoint para logout de usuário.
        
        POST /usuarios/logout/
        {
            "refresh": "refresh_token_aqui"
        }
        """
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Logout realizado com sucesso!'
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({
                'error': 'Token inválido.'
            }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='get',
        operation_summary="Dados do usuário autenticado",
        operation_description="Retorna os dados completos do usuário atualmente autenticado.",
        responses={
            200: UsuarioSerializer,
            401: openapi.Response(description="Token de autenticação não fornecido ou inválido"),
        }
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Retorna os dados do usuário autenticado.
        
        GET /usuarios/me/
        """
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """
        Atualiza os dados do usuário autenticado.
        
        PUT/PATCH /usuarios/me/
        """
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(
            request.user, 
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()

        return Response({
            'message': 'Dados atualizados com sucesso!',
            'usuario': UsuarioSerializer(usuario).data
        })
