from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuração do roteador para o ViewSet
router = DefaultRouter()
router.register(r'despesas-variaveis', views.DespesaVariavelViewSet, basename='despesavariavel')

# URLs do app despesavariavel
urlpatterns = [
    # Inclui todas as rotas do ViewSet
    path('api/', include(router.urls)),
]

# Padrão de nomenclatura das URLs geradas automaticamente pelo router:
# GET    /api/despesas-variaveis/                        -> list (listar despesas variáveis)
# POST   /api/despesas-variaveis/                        -> create (criar despesa variável)
# GET    /api/despesas-variaveis/{id}/                   -> retrieve (detalhar despesa variável)
# PUT    /api/despesas-variaveis/{id}/                   -> update (atualizar despesa variável completa)
# PATCH  /api/despesas-variaveis/{id}/                   -> partial_update (atualizar despesa variável parcial)
# DELETE /api/despesas-variaveis/{id}/                   -> destroy (deletar despesa variável)
# GET    /api/despesas-variaveis/ativas/                 -> ativas (ação customizada)
# POST   /api/despesas-variaveis/{id}/toggle-status/     -> toggle_status (ação customizada)
# GET    /api/despesas-variaveis/por-unidade/            -> por_unidade (ação customizada)
# GET    /api/despesas-variaveis/estatisticas/           -> estatisticas (ação customizada)
