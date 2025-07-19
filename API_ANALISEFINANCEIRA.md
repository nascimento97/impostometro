# API - Análises Financeiras

## 📋 Visão Geral

O módulo **Análises Financeiras** é responsável por armazenar e gerenciar os resultados dos cálculos de precificação e análise de viabilidade dos produtos. Este app permite que os usuários salvem diferentes cenários de análise para um mesmo produto e comparem resultados ao longo do tempo.

## 🎯 Funcionalidades

### Operações CRUD
- ✅ **Criar** análises financeiras com validações
- ✅ **Listar** análises com filtros e paginação
- ✅ **Visualizar** detalhes completos de uma análise
- ✅ **Atualizar** análises existentes
- ✅ **Deletar** análises

### Funcionalidades Avançadas
- 📊 **Estatísticas** das análises do usuário
- 🔄 **Comparação** entre múltiplas análises
- 📋 **Duplicação** de análises existentes
- 📄 **Relatórios** detalhados com métricas

## 🏗️ Estrutura do Modelo

### AnaliseFinanceira
```python
- id: Primary Key
- produto: ForeignKey(Produto) - Produto analisado
- custo_ingredientes: Decimal - Custo total dos ingredientes
- custo_despesas_fixas: Decimal - Custo das despesas fixas aplicáveis
- custo_despesas_variaveis: Decimal - Custo das despesas variáveis
- custo_total_producao: Decimal - Soma de todos os custos (calculado automaticamente)
- preco_venda_sugerido: Decimal - Preço sugerido baseado na margem
- faturamento_previsto: Decimal - Faturamento esperado no período
- lucro_previsto: Decimal - Lucro esperado no período
- created_at: DateTime - Data de criação da análise
```

### Propriedades Calculadas
- `margem_lucro_real`: Margem de lucro real baseada nos custos
- `margem_lucro_formatada`: Margem formatada com símbolo %
- `custo_total_formatado`: Custo formatado com R$
- `preco_venda_formatado`: Preço formatado com R$
- `lucro_formatado`: Lucro formatado com R$
- `faturamento_formatado`: Faturamento formatado com R$

## 🚀 Endpoints da API

### Operações Básicas

#### Listar Análises
```http
GET /api/analises-financeiras/
```

**Parâmetros de Filtro:**
- `produto`: ID do produto
- `custo_total_producao__gte/lte`: Filtro por custo total
- `preco_venda_sugerido__gte/lte`: Filtro por preço de venda
- `lucro_previsto__gte/lte`: Filtro por lucro
- `created_at__date__gte/lte`: Filtro por data
- `created_at__year/month`: Filtro por ano/mês

**Parâmetros de Busca:**
- `search`: Busca no nome/descrição do produto

**Parâmetros de Ordenação:**
- `ordering`: created_at, custo_total_producao, preco_venda_sugerido, lucro_previsto

#### Criar Análise
```http
POST /api/analises-financeiras/
Content-Type: application/json

{
  "produto": 1,
  "custo_ingredientes": "15.00",
  "custo_despesas_fixas": "8.00",
  "custo_despesas_variaveis": "4.00",
  "preco_venda_sugerido": "35.00",
  "faturamento_previsto": "1050.00",
  "lucro_previsto": "378.00"
}
```

#### Detalhes da Análise
```http
GET /api/analises-financeiras/{id}/
```

#### Atualizar Análise
```http
PUT /api/analises-financeiras/{id}/
PATCH /api/analises-financeiras/{id}/
```

#### Deletar Análise
```http
DELETE /api/analises-financeiras/{id}/
```

### Ações Customizadas

#### Estatísticas
```http
GET /api/analises-financeiras/stats/
```

**Resposta:**
```json
{
  "total_analises": 15,
  "custo_medio": "22.50",
  "preco_medio": "35.75",
  "lucro_total": "2450.00",
  "faturamento_total": "7200.00",
  "margem_lucro_media": 45.67,
  "margem_lucro_maxima": 75.00,
  "margem_lucro_minima": 25.00,
  "produtos_mais_analisados": [
    {"produto__nome": "Brigadeiro", "total_analises": 5},
    {"produto__nome": "Bolo de Chocolate", "total_analises": 3}
  ]
}
```

#### Comparar Análises
```http
POST /api/analises-financeiras/comparar/
Content-Type: application/json

{
  "analises_ids": [1, 2, 3]
}
```

**Resposta:**
```json
{
  "analises": [...],
  "resumo_comparativo": {
    "menor_custo": {"id": 1, "produto_nome": "Produto A", "valor": "20.00"},
    "maior_custo": {"id": 3, "produto_nome": "Produto C", "valor": "35.00"},
    "menor_preco": {"id": 1, "produto_nome": "Produto A", "valor": "30.00"},
    "maior_preco": {"id": 2, "produto_nome": "Produto B", "valor": "50.00"},
    "maior_lucro": {"id": 2, "produto_nome": "Produto B", "valor": "300.00"},
    "menor_lucro": {"id": 1, "produto_nome": "Produto A", "valor": "150.00"}
  }
}
```

#### Duplicar Análise
```http
POST /api/analises-financeiras/{id}/duplicar/
```

#### Relatório Detalhado
```http
GET /api/analises-financeiras/{id}/relatorio/
```

**Resposta:**
```json
{
  "analise": {...},
  "breakdown_custos": {
    "ingredientes": {"valor": "15.00", "percentual": 55.56},
    "despesas_fixas": {"valor": "8.00", "percentual": 29.63},
    "despesas_variaveis": {"valor": "4.00", "percentual": 14.81}
  },
  "metricas": {
    "margem_lucro_percentual": 29.63,
    "markup": 129.63,
    "retorno_investimento": 25.93
  }
}
```

## ✅ Validações

### Validações de Criação
- ✅ Produto deve existir e pertencer ao usuário
- ✅ Custos não podem ser negativos
- ✅ Preço de venda deve ser maior que zero
- ✅ Preço de venda deve ser maior que custo total
- ✅ Faturamento não pode ser negativo

### Validações de Atualização
- ✅ Não permite alterar o produto após criação
- ✅ Mantém validações de valores
- ✅ Recalcula custo total automaticamente

## 🔐 Segurança

### Autenticação
- ✅ Todas as operações requerem autenticação JWT
- ✅ Usuários só acessam suas próprias análises

### Autorização
- ✅ Análises filtradas por usuário automaticamente
- ✅ Validação de propriedade do produto

## 📊 Performance

### Otimizações de Consulta
- ✅ `select_related` para produto e usuário
- ✅ Filtros eficientes no banco de dados
- ✅ Paginação automática

### Serializers Específicos
- ✅ `ListSerializer` para listagem otimizada
- ✅ `DetailSerializer` para detalhes completos
- ✅ `CreateSerializer` para criação com validações
- ✅ `UpdateSerializer` para atualizações

## 🧪 Testes

### Cobertura de Testes
- ✅ Testes de modelo
- ✅ Testes de API
- ✅ Testes de validação
- ✅ Testes de segurança
- ✅ Testes de cálculos

### Exemplos de Uso

```python
# Executar testes
python manage.py test analisefinanceira

# Teste específico
python manage.py test analisefinanceira.tests.AnaliseFinanceiraModelTest.test_margem_lucro_real
```

## 🔄 Integração com Outros Apps

### Dependências
- **usuarios**: Model User (via get_user_model)
- **produtos**: Model Produto (ForeignKey)

### Relacionamentos
- `AnaliseFinanceira.produto → Produto`
- `Produto.analises_financeiras ← AnaliseFinanceira` (related_name)

## 📝 Exemplos de Uso

### Criar análise via Python
```python
from analisefinanceira.models import AnaliseFinanceira
from produtos.models import Produto

produto = Produto.objects.get(id=1)
analise = AnaliseFinanceira.objects.create(
    produto=produto,
    custo_ingredientes=Decimal('15.00'),
    custo_despesas_fixas=Decimal('8.00'),
    custo_despesas_variaveis=Decimal('4.00'),
    preco_venda_sugerido=Decimal('35.00'),
    faturamento_previsto=Decimal('1050.00'),
    lucro_previsto=Decimal('378.00')
)
```

### Filtrar análises por período
```python
from datetime import datetime, timedelta

# Análises do último mês
um_mes_atras = datetime.now() - timedelta(days=30)
analises_recentes = AnaliseFinanceira.objects.filter(
    created_at__gte=um_mes_atras,
    produto__usuario=user
)
```

### Calcular estatísticas personalizadas
```python
from django.db.models import Avg, Sum, Count

stats = AnaliseFinanceira.objects.filter(
    produto__usuario=user
).aggregate(
    media_margem=Avg('margem_lucro_real'),
    total_lucro=Sum('lucro_previsto'),
    total_analises=Count('id')
)
```
