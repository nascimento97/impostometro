# API de Produtos - ImpostoMetro

## Visão Geral

A API de Produtos permite gerenciar produtos, seus ingredientes, despesas fixas e variáveis associadas, além de realizar cálculos de custos e análises financeiras.

## Endpoints Principais

### 1. Produtos (CRUD Completo)

#### Listar Produtos
```http
GET /api/produtos/
```

**Parâmetros de consulta:**
- `search`: Busca por nome ou descrição
- `tempo_preparo`: Filtrar por tempo de preparo
- `periodo_analise`: Filtrar por período de análise
- `ordering`: Ordenar por campo (nome, tempo_preparo, margem_lucro, created_at)

**Resposta:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "Bolo de Chocolate",
      "tempo_preparo": 90,
      "margem_lucro": "25.50",
      "periodo_analise": 30,
      "created_at": "2024-01-15T10:30:00Z",
      "usuario_nome": "Padaria Central",
      "margem_lucro_formatada": "25.50%",
      "tempo_preparo_formatado": "1h 30min"
    }
  ]
}
```

#### Criar Produto
```http
POST /api/produtos/
```

**Corpo da requisição:**
```json
{
  "nome": "Torta de Limão",
  "descricao": "Torta cremosa de limão com merengue",
  "tempo_preparo": 120,
  "margem_lucro": "30.00",
  "periodo_analise": 30
}
```

#### Obter Produto (Detalhado)
```http
GET /api/produtos/{id}/
```

**Resposta:**
```json
{
  "id": 1,
  "usuario": 1,
  "nome": "Bolo de Chocolate",
  "descricao": "Bolo úmido de chocolate com cobertura",
  "tempo_preparo": 90,
  "margem_lucro": "25.50",
  "periodo_analise": 30,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "usuario_nome": "Padaria Central",
  "margem_lucro_formatada": "25.50%",
  "tempo_preparo_formatado": "1h 30min",
  "ingredientes": [
    {
      "id": 1,
      "ingrediente": 1,
      "quantidade": "500.000",
      "ingrediente_nome": "Farinha de Trigo",
      "ingrediente_preco": "5.50",
      "ingrediente_unidade": "kg",
      "custo_total": "2.75"
    }
  ],
  "despesas_fixas": [
    {
      "id": 1,
      "despesa_fixa": 1,
      "despesa_nome": "Aluguel",
      "despesa_valor": "1500.00"
    }
  ],
  "despesas_variaveis": [
    {
      "id": 1,
      "despesa_variavel": 1,
      "quantidade": "0.050",
      "despesa_nome": "Energia Elétrica",
      "despesa_valor_unitario": "0.75",
      "despesa_unidade": "kwh",
      "custo_total": "0.0375"
    }
  ]
}
```

#### Atualizar Produto
```http
PUT /api/produtos/{id}/
PATCH /api/produtos/{id}/
```

#### Deletar Produto
```http
DELETE /api/produtos/{id}/
```

### 2. Endpoints Especiais

#### Buscar Produtos
```http
GET /api/produtos/search/?q=chocolate
```

#### Estatísticas de Produtos
```http
GET /api/produtos/stats/
```

**Resposta:**
```json
{
  "total_produtos": 5,
  "tempo_preparo_medio": 75.5,
  "margem_lucro_media": 28.5,
  "periodo_analise_medio": 35.2,
  "produto_mais_complexo": {
    "id": 3,
    "nome": "Torta Alemã",
    "tempo_preparo": 180
  },
  "produto_maior_margem": {
    "id": 2,
    "nome": "Brigadeiro Gourmet",
    "margem_lucro": "45.00"
  }
}
```

#### Duplicar Produto
```http
POST /api/produtos/{id}/duplicar/
```

**Resposta:**
```json
{
  "message": "Produto duplicado com sucesso",
  "produto": {
    // Dados do produto duplicado
  }
}
```

#### Calcular Custos e Análise Financeira
```http
GET /api/produtos/{id}/calcular/
```

**Resposta:**
```json
{
  "produto_id": 1,
  "produto_nome": "Bolo de Chocolate",
  "periodo_analise": 30,
  "margem_lucro": "25.50",
  "custos": {
    "ingredientes": 15.75,
    "despesas_fixas": 50.00,
    "despesas_variaveis": 3.25,
    "total_producao": 69.00
  },
  "precificacao": {
    "preco_venda_sugerido": 86.60,
    "margem_lucro_percentual": 25.50,
    "margem_lucro_valor": 17.60
  },
  "projecoes_periodo": {
    "quantidade_estimada": 30,
    "faturamento_previsto": 2598.00,
    "custo_total_periodo": 2070.00,
    "lucro_previsto": 528.00,
    "roi_percentual": 25.50
  },
  "detalhamento_ingredientes": [
    {
      "nome": "Farinha de Trigo",
      "quantidade": 0.5,
      "unidade": "kg",
      "preco_unitario": 5.50,
      "custo_total": 2.75
    }
  ],
  "detalhamento_despesas_fixas": [
    {
      "nome": "Aluguel",
      "valor_mensal": 1500.00,
      "valor_rateado": 50.00
    }
  ],
  "detalhamento_despesas_variaveis": [
    {
      "nome": "Energia Elétrica",
      "quantidade": 0.05,
      "unidade": "kwh",
      "valor_unitario": 0.75,
      "custo_total": 0.0375
    }
  ]
}
```

### 3. Gestão de Relacionamentos

#### Produto-Ingredientes
```http
GET /api/produto-ingredientes/
POST /api/produto-ingredientes/
GET /api/produto-ingredientes/{id}/
PUT /api/produto-ingredientes/{id}/
PATCH /api/produto-ingredientes/{id}/
DELETE /api/produto-ingredientes/{id}/
```

**Exemplo de criação:**
```json
{
  "produto": 1,
  "ingrediente": 1,
  "quantidade": "500.000"
}
```

#### Produto-Despesas Fixas
```http
GET /api/produto-despesas-fixas/
POST /api/produto-despesas-fixas/
GET /api/produto-despesas-fixas/{id}/
PUT /api/produto-despesas-fixas/{id}/
PATCH /api/produto-despesas-fixas/{id}/
DELETE /api/produto-despesas-fixas/{id}/
```

**Exemplo de criação:**
```json
{
  "produto": 1,
  "despesa_fixa": 1
}
```

#### Produto-Despesas Variáveis
```http
GET /api/produto-despesas-variaveis/
POST /api/produto-despesas-variaveis/
GET /api/produto-despesas-variaveis/{id}/
PUT /api/produto-despesas-variaveis/{id}/
PATCH /api/produto-despesas-variaveis/{id}/
DELETE /api/produto-despesas-variaveis/{id}/
```

**Exemplo de criação:**
```json
{
  "produto": 1,
  "despesa_variavel": 1,
  "quantidade": "0.050"
}
```

## Códigos de Status HTTP

- `200 OK`: Sucesso
- `201 Created`: Recurso criado com sucesso
- `204 No Content`: Recurso deletado com sucesso
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Não autenticado
- `403 Forbidden`: Sem permissão
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## Validações

### Produto
- **nome**: Obrigatório, mínimo 2 caracteres, único por usuário
- **tempo_preparo**: Obrigatório, deve ser maior que zero
- **margem_lucro**: Obrigatório, entre 0 e 1000%
- **periodo_analise**: Obrigatório, deve ser maior que zero

### Relacionamentos
- **quantidade**: Deve ser maior que zero (onde aplicável)
- **Integridade**: Ingredientes/despesas devem pertencer ao mesmo usuário do produto

## Autenticação

Todas as requisições devem incluir o header de autorização:
```http
Authorization: Bearer {jwt_token}
```

## Filtros e Ordenação

### Produtos
- **Filtros**: `tempo_preparo`, `periodo_analise`
- **Busca**: `nome`, `descricao`
- **Ordenação**: `nome`, `tempo_preparo`, `margem_lucro`, `created_at`

## Exemplos de Uso

### 1. Fluxo Completo de Criação de Produto

```bash
# 1. Criar o produto
curl -X POST http://localhost:8000/api/produtos/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Pão de Açúcar",
    "descricao": "Pão doce tradicional",
    "tempo_preparo": 45,
    "margem_lucro": "20.00",
    "periodo_analise": 30
  }'

# 2. Adicionar ingredientes
curl -X POST http://localhost:8000/api/produto-ingredientes/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "produto": 1,
    "ingrediente": 1,
    "quantidade": "300.000"
  }'

# 3. Adicionar despesa fixa
curl -X POST http://localhost:8000/api/produto-despesas-fixas/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "produto": 1,
    "despesa_fixa": 1
  }'

# 4. Calcular custos
curl -X GET http://localhost:8000/api/produtos/1/calcular/ \
  -H "Authorization: Bearer {token}"
```
