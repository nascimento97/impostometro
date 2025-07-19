from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuração do roteador para os ViewSets
router = DefaultRouter()
router.register(r'analises-financeiras', views.AnaliseFinanceiraViewSet, basename='analise-financeira')

# URLs do app analisefinanceira
urlpatterns = [
    # Inclui todas as rotas dos ViewSets
    path('api/', include(router.urls)),
]

# Padrão de nomenclatura das URLs geradas automaticamente pelo router:
#
# === ANÁLISES FINANCEIRAS ===
# GET    /api/analises-financeiras/              - Lista todas as análises do usuário
# POST   /api/analises-financeiras/              - Cria uma nova análise
# GET    /api/analises-financeiras/{id}/         - Detalhes de uma análise específica
# PUT    /api/analises-financeiras/{id}/         - Atualiza completamente uma análise
# PATCH  /api/analises-financeiras/{id}/         - Atualiza parcialmente uma análise
# DELETE /api/analises-financeiras/{id}/         - Remove uma análise
#
# === AÇÕES CUSTOMIZADAS ===
# GET    /api/analises-financeiras/stats/        - Estatísticas das análises
# POST   /api/analises-financeiras/comparar/     - Compara múltiplas análises
# POST   /api/analises-financeiras/{id}/duplicar/ - Duplica uma análise
# GET    /api/analises-financeiras/{id}/relatorio/ - Relatório detalhado da análise
#
# === FILTROS DISPONÍVEIS ===
# ?produto=<id>                    - Filtra por produto específico
# ?custo_total_producao__gte=<valor> - Custo total maior ou igual
# ?custo_total_producao__lte=<valor> - Custo total menor ou igual
# ?preco_venda_sugerido__gte=<valor> - Preço maior ou igual
# ?preco_venda_sugerido__lte=<valor> - Preço menor ou igual
# ?lucro_previsto__gte=<valor>     - Lucro maior ou igual
# ?lucro_previsto__lte=<valor>     - Lucro menor ou igual
# ?created_at__date__gte=<data>    - Criado após data (YYYY-MM-DD)
# ?created_at__date__lte=<data>    - Criado antes da data (YYYY-MM-DD)
# ?created_at__year=<ano>          - Criado no ano
# ?created_at__month=<mês>         - Criado no mês
#
# === BUSCA ===
# ?search=<termo>                  - Busca no nome e descrição do produto
#
# === ORDENAÇÃO ===
# ?ordering=created_at             - Ordena por data de criação (crescente)
# ?ordering=-created_at            - Ordena por data de criação (decrescente)
# ?ordering=custo_total_producao   - Ordena por custo total
# ?ordering=preco_venda_sugerido   - Ordena por preço de venda
# ?ordering=lucro_previsto         - Ordena por lucro previsto
#
# === EXEMPLOS DE USO ===
# Análises de um produto específico:
# GET /api/analises-financeiras/?produto=1
#
# Análises com lucro acima de R$ 100:
# GET /api/analises-financeiras/?lucro_previsto__gte=100.00
#
# Análises criadas em 2024:
# GET /api/analises-financeiras/?created_at__year=2024
#
# Buscar por nome de produto:
# GET /api/analises-financeiras/?search=brigadeiro
#
# Estatísticas das análises:
# GET /api/analises-financeiras/stats/
#
# Comparar análises:
# POST /api/analises-financeiras/comparar/
# {"analises_ids": [1, 2, 3]}
