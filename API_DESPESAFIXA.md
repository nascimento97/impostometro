# API DespesaFixa - Documentação

## Endpoints Disponíveis

### Autenticação
Todos os endpoints requerem autenticação JWT. Incluir o token no header:
```
Authorization: Bearer {seu_token_jwt}
```

### Despesas Fixas

#### 1. Listar Despesas Fixas
```http
GET /api/despesas-fixas/
```

**Parâmetros de consulta opcionais:**
- `search`: Busca por nome ou descrição
- `ativa`: Filtrar por status (true/false)
- `ordering`: Ordenar por campo (nome, valor, created_at, updated_at)

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "nome": "Aluguel",
    "valor": "1500.00",
    "valor_formatado": "R$ 1.500,00",
    "ativa": true,
    "status_text": "Ativa",
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

#### 2. Criar Despesa Fixa
```http
POST /api/despesas-fixas/
```

**Corpo da requisição:**
```json
{
  "nome": "Energia Elétrica",
  "valor": 350.50,
  "descricao": "Conta de energia elétrica mensal",
  "ativa": true
}
```

#### 3. Detalhar Despesa Fixa
```http
GET /api/despesas-fixas/{id}/
```

#### 4. Atualizar Despesa Fixa
```http
PUT /api/despesas-fixas/{id}/
PATCH /api/despesas-fixas/{id}/
```

#### 5. Deletar Despesa Fixa
```http
DELETE /api/despesas-fixas/{id}/
```

#### 6. Listar Apenas Despesas Ativas
```http
GET /api/despesas-fixas/ativas/
```

#### 7. Alternar Status (Ativar/Desativar)
```http
POST /api/despesas-fixas/{id}/toggle-status/
```

#### 8. Total das Despesas Fixas Ativas
```http
GET /api/despesas-fixas/total/
```

**Resposta:**
```json
{
  "total_despesas_fixas": 2500.50,
  "total_formatado": "R$ 2.500,50",
  "quantidade_despesas": 5
}
```

#### 9. Estatísticas das Despesas
```http
GET /api/despesas-fixas/estatisticas/
```

**Resposta:**
```json
{
  "total": {
    "quantidade": 10,
    "valor": 3000.00,
    "valor_formatado": "R$ 3.000,00"
  },
  "ativas": {
    "quantidade": 8,
    "valor": 2500.50,
    "valor_formatado": "R$ 2.500,50"
  },
  "inativas": {
    "quantidade": 2,
    "valor": 499.50,
    "valor_formatado": "R$ 499,50"
  }
}
```

## Validações

### Campos Obrigatórios
- `nome`: Mínimo 3 caracteres
- `valor`: Maior que 0, máximo 999.999,99

### Regras de Negócio
- Não é possível ter duas despesas fixas com o mesmo nome para o mesmo usuário
- Valores não podem ser negativos
- Apenas o proprietário da despesa pode visualizar/editar/excluir

## Códigos de Status HTTP

- `200 OK`: Sucesso
- `201 Created`: Criado com sucesso
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Não autenticado
- `403 Forbidden`: Sem permissão
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor
