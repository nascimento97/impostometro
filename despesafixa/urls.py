from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuração do roteador para o ViewSet
router = DefaultRouter()
router.register(r'despesas-fixas', views.DespesaFixaViewSet, basename='despesafixa')

# URLs do app despesafixa
urlpatterns = [
    # Inclui todas as rotas do ViewSet
    path('api/', include(router.urls)),
]

# Padrão de nomenclatura das URLs geradas automaticamente pelo router:
# GET    /api/despesas-fixas/                    -> list (listar despesas fixas)
# POST   /api/despesas-fixas/                    -> create (criar despesa fixa)
# GET    /api/despesas-fixas/{id}/               -> retrieve (detalhar despesa fixa)
# PUT    /api/despesas-fixas/{id}/               -> update (atualizar despesa fixa completa)
# PATCH  /api/despesas-fixas/{id}/               -> partial_update (atualizar despesa fixa parcial)
# DELETE /api/despesas-fixas/{id}/               -> destroy (deletar despesa fixa)
# GET    /api/despesas-fixas/ativas/             -> ativas (ação customizada)
# POST   /api/despesas-fixas/{id}/toggle-status/ -> toggle_status (ação customizada)
# GET    /api/despesas-fixas/total/              -> total (ação customizada)
# GET    /api/despesas-fixas/estatisticas/       -> estatisticas (ação customizada)
