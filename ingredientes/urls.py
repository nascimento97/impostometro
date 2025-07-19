from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuração do roteador para o ViewSet
router = DefaultRouter()
router.register(r'ingredientes', views.IngredienteViewSet, basename='ingrediente')

# URLs do app ingredientes
urlpatterns = [
    # Inclui todas as rotas do ViewSet
    path('api/', include(router.urls)),
]

# Padrão de nomenclatura das URLs geradas automaticamente pelo router:
# - GET    /api/ingredientes/                    -> list (listar ingredientes)
# - POST   /api/ingredientes/                    -> create (criar ingrediente)
# - GET    /api/ingredientes/{id}/               -> retrieve (detalhes do ingrediente)
# - PUT    /api/ingredientes/{id}/               -> update (atualizar ingrediente completo)
# - PATCH  /api/ingredientes/{id}/               -> partial_update (atualizar ingrediente parcial)
# - DELETE /api/ingredientes/{id}/               -> destroy (deletar ingrediente)
#
# URLs customizadas adicionais:
# - GET    /api/ingredientes/search/             -> search_ingredientes (buscar ingredientes)
# - GET    /api/ingredientes/by-fornecedor/      -> by_fornecedor (ingredientes por fornecedor)
# - GET    /api/ingredientes/stats/              -> estatisticas (estatísticas dos ingredientes)
# - GET    /api/ingredientes/{id}/duplicar/      -> duplicar_ingrediente (duplicar ingrediente)
