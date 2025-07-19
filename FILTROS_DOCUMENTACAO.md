# Documentação dos Filtros - Django Filters

Este documento descreve como usar os filtros implementados em todos os apps do projeto Impostômetro.

## Configuração Global

O `django-filters` está configurado globalmente no projeto através das configurações do Django REST Framework em `core/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## Apps Configurados

Todos os seguintes apps possuem filtros configurados:

### 1. Usuários (`usuarios`)

**Endpoint:** `/usuarios/`

**Filtros Disponíveis:**
- `is_active` - Filtrar por usuários ativos (true/false)
- `is_staff` - Filtrar por usuários staff (true/false)
- `is_superuser` - Filtrar por superusuários (true/false)
- `username` - Filtro exato ou busca parcial (`?username=admin` ou `?username__icontains=adm`)
- `email` - Filtro exato ou busca parcial
- `first_name` - Filtro exato ou busca parcial
- `last_name` - Filtro exato ou busca parcial
- `nome_comercial` - Filtro exato ou busca parcial
- `cnpj` - Filtro exato ou busca parcial
- `endereco` - Busca parcial
- `telefone` - Filtro exato ou busca parcial
- `data_criacao_inicio` - Data de criação a partir de
- `data_criacao_fim` - Data de criação até
- `ultimo_login_inicio` - Último login a partir de
- `ultimo_login_fim` - Último login até
- `search` - Busca global em múltiplos campos

**Exemplos de Uso:**
```
GET /usuarios/?is_active=true
GET /usuarios/?search=joão
GET /usuarios/?username__icontains=admin
GET /usuarios/?data_criacao_inicio=2024-01-01&data_criacao_fim=2024-12-31
```

### 2. Despesas Fixas (`despesafixa`)

**Endpoint:** `/despesas-fixas/`

**Filtros Disponíveis:**
- `ativa` - Filtrar por despesas ativas (true/false)
- `nome` - Filtro exato ou busca parcial
- `descricao` - Busca parcial
- `valor` - Filtro exato, maior que, menor que
- `valor_min` - Valor mínimo
- `valor_max` - Valor máximo
- `data_criacao_inicio` - Data de criação a partir de
- `data_criacao_fim` - Data de criação até
- `data_atualizacao_inicio` - Data de atualização a partir de
- `data_atualizacao_fim` - Data de atualização até
- `search` - Busca global em nome e descrição

**Exemplos de Uso:**
```
GET /despesas-fixas/?ativa=true
GET /despesas-fixas/?valor_min=100&valor_max=500
GET /despesas-fixas/?search=aluguel
GET /despesas-fixas/?nome__icontains=energia
```

### 3. Despesas Variáveis (`despesavariavel`)

**Endpoint:** `/despesas-variaveis/`

**Filtros Disponíveis:**
- `ativa` - Filtrar por despesas ativas (true/false)
- `unidade_medida` - Filtro exato ou busca parcial
- `nome` - Filtro exato ou busca parcial
- `descricao` - Busca parcial
- `valor_por_unidade` - Filtro exato, maior que, menor que
- `valor_min` - Valor por unidade mínimo
- `valor_max` - Valor por unidade máximo
- `data_criacao_inicio` - Data de criação a partir de
- `data_criacao_fim` - Data de criação até
- `data_atualizacao_inicio` - Data de atualização a partir de
- `data_atualizacao_fim` - Data de atualização até
- `search` - Busca global em nome, descrição e unidade de medida

**Exemplos de Uso:**
```
GET /despesas-variaveis/?ativa=true
GET /despesas-variaveis/?unidade_medida=kg
GET /despesas-variaveis/?valor_min=10.50&valor_max=50.00
GET /despesas-variaveis/?search=combustivel
```

### 4. Ingredientes (`ingredientes`)

**Endpoint:** `/ingredientes/`

**Filtros Disponíveis:**
- `unidade_medida` - Filtro exato ou busca parcial
- `fornecedor` - Filtro exato ou busca parcial
- `nome` - Filtro exato ou busca parcial
- `preco_por_unidade` - Filtro exato, maior que, menor que
- `preco_min` - Preço por unidade mínimo
- `preco_max` - Preço por unidade máximo
- `data_criacao_inicio` - Data de criação a partir de
- `data_criacao_fim` - Data de criação até
- `data_atualizacao_inicio` - Data de atualização a partir de
- `data_atualizacao_fim` - Data de atualização até
- `search` - Busca global em nome, fornecedor e unidade de medida

**Exemplos de Uso:**
```
GET /ingredientes/?fornecedor=Distribuidora ABC
GET /ingredientes/?unidade_medida=kg
GET /ingredientes/?preco_min=5.00&preco_max=20.00
GET /ingredientes/?search=farinha
```

### 5. Produtos (`produtos`)

**Endpoint:** `/produtos/`

**Filtros Disponíveis:**
- `nome` - Filtro exato ou busca parcial
- `descricao` - Busca parcial
- `tempo_preparo` - Filtro exato, maior que, menor que
- `tempo_preparo_min` - Tempo de preparo mínimo (em minutos)
- `tempo_preparo_max` - Tempo de preparo máximo (em minutos)
- `margem_lucro` - Filtro exato, maior que, menor que
- `margem_lucro_min` - Margem de lucro mínima (em %)
- `margem_lucro_max` - Margem de lucro máxima (em %)
- `periodo_analise` - Filtro exato ou busca parcial
- `data_criacao_inicio` - Data de criação a partir de
- `data_criacao_fim` - Data de criação até
- `data_atualizacao_inicio` - Data de atualização a partir de
- `data_atualizacao_fim` - Data de atualização até
- `search` - Busca global em nome, descrição e período de análise

**Exemplos de Uso:**
```
GET /produtos/?tempo_preparo_min=30&tempo_preparo_max=120
GET /produtos/?margem_lucro_min=20
GET /produtos/?periodo_analise=mensal
GET /produtos/?search=bolo
```

### 6. Análise Financeira (`analisefinanceira`)

**Endpoint:** `/analises-financeiras/`

**Filtros Disponíveis:**
- `produto` - Filtro exato por ID do produto
- `custo_total_producao` - Filtro exato, maior que, menor que
- `custo_total_min` - Custo total mínimo
- `custo_total_max` - Custo total máximo
- `preco_venda_sugerido` - Filtro exato, maior que, menor que
- `preco_venda_min` - Preço de venda mínimo
- `preco_venda_max` - Preço de venda máximo
- `lucro_previsto` - Filtro exato, maior que, menor que
- `lucro_min` - Lucro mínimo
- `lucro_max` - Lucro máximo
- `data_criacao_inicio` - Data de criação a partir de
- `data_criacao_fim` - Data de criação até
- `ano` - Filtrar por ano
- `mes` - Filtrar por mês
- `search` - Busca global em nome e descrição do produto

**Exemplos de Uso:**
```
GET /analises-financeiras/?produto=1
GET /analises-financeiras/?custo_total_min=50.00&custo_total_max=200.00
GET /analises-financeiras/?ano=2024&mes=7
GET /analises-financeiras/?lucro_min=100.00
GET /analises-financeiras/?search=bolo
```

## Filtros Globais Disponíveis

### 1. Busca (SearchFilter)
Disponível em todos os endpoints através do parâmetro `search`:
```
GET /usuarios/?search=joão
```

### 2. Ordenação (OrderingFilter)
Disponível em todos os endpoints através do parâmetro `ordering`:
```
GET /usuarios/?ordering=username
GET /usuarios/?ordering=-date_joined
GET /produtos/?ordering=nome,-created_at
```

### 3. Paginação
Todos os endpoints possuem paginação configurada:
```
GET /usuarios/?page=2
```

## Operadores de Filtro

### Operadores Disponíveis:
- `exact` - Correspondência exata (padrão)
- `icontains` - Contém (case-insensitive)
- `gte` - Maior ou igual que
- `lte` - Menor ou igual que
- `gt` - Maior que
- `lt` - Menor que
- `in` - Em uma lista de valores
- `range` - Em um intervalo
- `year` - Por ano
- `month` - Por mês
- `date` - Por data

### Exemplos de Uso:
```
GET /usuarios/?username__icontains=admin
GET /despesas-fixas/?valor__gte=100
GET /despesas-fixas/?valor__lte=500
GET /analises-financeiras/?created_at__year=2024
GET /analises-financeiras/?created_at__month=7
```

## Combinando Filtros

Você pode combinar múltiplos filtros na mesma requisição:
```
GET /produtos/?tempo_preparo_min=30&margem_lucro_min=20&search=bolo&ordering=-created_at
GET /despesas-fixas/?ativa=true&valor_min=100&data_criacao_inicio=2024-01-01
```

## Considerações Importantes

1. **Autenticação**: Todos os endpoints requerem autenticação JWT
2. **Filtros por Usuário**: Exceto usuários, todos os outros endpoints filtram automaticamente pelos dados do usuário autenticado
3. **Performance**: Use filtros específicos em vez de busca global quando possível
4. **Formato de Data**: Use o formato ISO 8601 (YYYY-MM-DD) para filtros de data
5. **Case Sensitivity**: Use `__icontains` para buscas que ignoram maiúsculas/minúsculas

## Documentação Swagger

Todos os filtros estão documentados no Swagger UI disponível em `/swagger/` quando o servidor estiver rodando.
