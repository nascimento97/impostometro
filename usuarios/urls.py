from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuração do roteador para o ViewSet
router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')

# URLs do app usuarios
urlpatterns = [
    # Inclui todas as rotas do ViewSet
    path('api/', include(router.urls)),
    
    # URLs específicas para ações customizadas (opcional, já estão incluídas no ViewSet)
    # path('api/usuarios/login/', views.UsuarioViewSet.as_view({'post': 'login'}), name='usuario-login'),
    # path('api/usuarios/logout/', views.UsuarioViewSet.as_view({'post': 'logout'}), name='usuario-logout'),
    # path('api/usuarios/me/', views.UsuarioViewSet.as_view({'get': 'me', 'put': 'update_me', 'patch': 'update_me'}), name='usuario-me'),
]

# Padrão de nomenclatura das URLs geradas automaticamente pelo router:
# GET    /api/usuarios/           -> list (listar usuários)
# POST   /api/usuarios/           -> create (criar usuário)
# GET    /api/usuarios/{id}/      -> retrieve (detalhar usuário)
# PUT    /api/usuarios/{id}/      -> update (atualizar usuário completo)
# PATCH  /api/usuarios/{id}/      -> partial_update (atualizar usuário parcial)
# DELETE /api/usuarios/{id}/      -> destroy (deletar usuário)
# POST   /api/usuarios/login/     -> login (ação customizada)
# POST   /api/usuarios/logout/    -> logout (ação customizada)
# GET    /api/usuarios/me/        -> me (ação customizada)
# PUT    /api/usuarios/me/        -> update_me (ação customizada)
# PATCH  /api/usuarios/me/        -> update_me (ação customizada)
