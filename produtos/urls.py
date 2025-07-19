from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuração do roteador para os ViewSets
router = DefaultRouter()
router.register(r'produtos', views.ProdutoViewSet, basename='produto')
router.register(r'produto-ingredientes', views.ProdutoIngredienteViewSet, basename='produto-ingrediente')
router.register(r'produto-despesas-fixas', views.ProdutoDespesaFixaViewSet, basename='produto-despesa-fixa')
router.register(r'produto-despesas-variaveis', views.ProdutoDespesaVariavelViewSet, basename='produto-despesa-variavel')

# URLs do app produtos
urlpatterns = [
    # Inclui todas as rotas dos ViewSets
    path('api/', include(router.urls)),
]

# Padrão de nomenclatura das URLs geradas automaticamente pelo router:
#
# === PRODUTOS ===
# - GET    /api/produtos/                        -> list (listar produtos)
# - POST   /api/produtos/                        -> create (criar produto)
# - GET    /api/produtos/{id}/                   -> retrieve (detalhes do produto)
# - PUT    /api/produtos/{id}/                   -> update (atualizar produto completo)
# - PATCH  /api/produtos/{id}/                   -> partial_update (atualizar produto parcial)
# - DELETE /api/produtos/{id}/                   -> destroy (deletar produto)
#
# URLs customizadas adicionais:
# - GET    /api/produtos/search/                 -> search (buscar produtos)
# - GET    /api/produtos/stats/                  -> stats (estatísticas dos produtos)
# - POST   /api/produtos/{id}/duplicar/          -> duplicar (duplicar produto)
# - GET    /api/produtos/{id}/calcular/          -> calcular (calcular custos e análise)
#
# === PRODUTO INGREDIENTES ===
# - GET    /api/produto-ingredientes/            -> list (listar relacionamentos)
# - POST   /api/produto-ingredientes/            -> create (criar relacionamento)
# - GET    /api/produto-ingredientes/{id}/       -> retrieve (detalhes do relacionamento)
# - PUT    /api/produto-ingredientes/{id}/       -> update (atualizar relacionamento)
# - PATCH  /api/produto-ingredientes/{id}/       -> partial_update (atualizar parcial)
# - DELETE /api/produto-ingredientes/{id}/       -> destroy (deletar relacionamento)
#
# === PRODUTO DESPESAS FIXAS ===
# - GET    /api/produto-despesas-fixas/          -> list (listar relacionamentos)
# - POST   /api/produto-despesas-fixas/          -> create (criar relacionamento)
# - GET    /api/produto-despesas-fixas/{id}/     -> retrieve (detalhes do relacionamento)
# - PUT    /api/produto-despesas-fixas/{id}/     -> update (atualizar relacionamento)
# - PATCH  /api/produto-despesas-fixas/{id}/     -> partial_update (atualizar parcial)
# - DELETE /api/produto-despesas-fixas/{id}/     -> destroy (deletar relacionamento)
#
# === PRODUTO DESPESAS VARIÁVEIS ===
# - GET    /api/produto-despesas-variaveis/      -> list (listar relacionamentos)
# - POST   /api/produto-despesas-variaveis/      -> create (criar relacionamento)
# - GET    /api/produto-despesas-variaveis/{id}/ -> retrieve (detalhes do relacionamento)
# - PUT    /api/produto-despesas-variaveis/{id}/ -> update (atualizar relacionamento)
# - PATCH  /api/produto-despesas-variaveis/{id}/ -> partial_update (atualizar parcial)
# - DELETE /api/produto-despesas-variaveis/{id}/ -> destroy (deletar relacionamento)
