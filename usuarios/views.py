from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .models import Usuario
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
        Personaliza o queryset baseado no usuário autenticado.
        """
        queryset = Usuario.objects.all()
        
        # Filtro por busca
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(nome_comercial__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        # Filtro por status ativo
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

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
