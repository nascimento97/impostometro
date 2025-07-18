# API Despesa Variável

## Visão Geral
A API de Despesas Variáveis permite gerenciar despesas que variam conforme a produção dos produtos. Essas despesas são calculadas por unidade e incluem itens como embalagens, combustível, etc.

## Modelo de Dados

### DespesaVariavel
```python
{
    "id": 1,
    "usuario": 1,
    "nome": "Embalagem plástica",
    "valor_por_unidade": "1.50",
    "unidade_medida": "unidade",
    "descricao": "Embalagem plástica para produto",
    "ativa": true,
    "created_at": "2023-07-18T10:00:00Z",
    "updated_at": "2023-07-18T10:00:00Z",
    "valor_formatado": "R$ 1,50",
    "status_text": "Ativa",
    "info_completa": "Embalagem plástica - R$ 1,50/unidade",
    "usuario_nome": "usuario_teste"
}
```

## Endpoints

### 1. Listar Despesas Variáveis
**GET** `/api/despesas-variaveis/`

Lista todas as despesas variáveis do usuário autenticado.

**Parâmetros de Query:**
- `ativa` (boolean): Filtrar por status ativo/inativo
- `unidade_medida` (string): Filtrar por unidade de medida
- `search` (string): Buscar por nome, descrição ou unidade
- `ordering` (string): Ordenar por campos (nome, valor_por_unidade, created_at)

**Exemplo de Resposta:**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "nome": "Embalagem plástica",
            "valor_por_unidade": "1.50",
            "unidade_medida": "unidade",
            "ativa": true,
            "created_at": "2023-07-18T10:00:00Z",
            "valor_formatado": "R$ 1,50",
            "status_text": "Ativa",
            "info_completa": "Embalagem plástica - R$ 1,50/unidade"
        }
    ]
}
```

### 2. Criar Despesa Variável
**POST** `/api/despesas-variaveis/`

Cria uma nova despesa variável.

**Corpo da Requisição:**
```json
{
    "nome": "Combustível",
    "valor_por_unidade": "5.50",
    "unidade_medida": "litro",
    "descricao": "Combustível para entrega",
    "ativa": true
}
```

### 3. Obter Despesa Variável
**GET** `/api/despesas-variaveis/{id}/`

Obtém detalhes de uma despesa variável específica.

### 4. Atualizar Despesa Variável
**PUT** `/api/despesas-variaveis/{id}/`
**PATCH** `/api/despesas-variaveis/{id}/`

Atualiza uma despesa variável existente.

### 5. Remover Despesa Variável
**DELETE** `/api/despesas-variaveis/{id}/`

Remove uma despesa variável.

## Endpoints Especiais

### 6. Listar Apenas Ativas
**GET** `/api/despesas-variaveis/ativas/`

Lista apenas as despesas variáveis ativas.

### 7. Alternar Status
**POST** `/api/despesas-variaveis/{id}/toggle-status/`

Alterna o status ativo/inativo de uma despesa variável.

### 8. Agrupar por Unidade
**GET** `/api/despesas-variaveis/por-unidade/`

Retorna despesas agrupadas por unidade de medida.

**Exemplo de Resposta:**
```json
{
    "unidades_medida": {
        "unidade": [
            {
                "id": 1,
                "nome": "Embalagem plástica",
                "valor_por_unidade": "1.50",
                "valor_formatado": "R$ 1,50",
                "descricao": "Embalagem plástica para produto"
            }
        ],
        "litro": [
            {
                "id": 2,
                "nome": "Combustível",
                "valor_por_unidade": "5.50",
                "valor_formatado": "R$ 5,50",
                "descricao": "Combustível para entrega"
            }
        ]
    },
    "total_unidades": 2
}
```

### 9. Estatísticas
**GET** `/api/despesas-variaveis/estatisticas/`

Retorna estatísticas das despesas variáveis.

**Exemplo de Resposta:**
```json
{
    "total_despesas": 5,
    "despesas_ativas": 4,
    "despesas_inativas": 1,
    "unidades_medida_diferentes": 3,
    "valor_medio_por_unidade": 2.75,
    "valor_minimo": 0.50,
    "valor_maximo": 5.50,
    "unidades_mais_utilizadas": [
        {"unidade": "unidade", "quantidade": 3},
        {"unidade": "kg", "quantidade": 2},
        {"unidade": "litro", "quantidade": 1}
    ]
}
```

## Validações

### Campos Obrigatórios
- `nome`: Mínimo 3 caracteres
- `valor_por_unidade`: Deve ser positivo e menor que 999999.99
- `unidade_medida`: Mínimo 1 caractere

### Regras de Negócio
- Nome deve ser único por usuário
- Valor por unidade não pode ser negativo
- Apenas o proprietário pode editar/excluir suas despesas

## Códigos de Status

- `200 OK`: Operação realizada com sucesso
- `201 Created`: Despesa variável criada com sucesso
- `400 Bad Request`: Dados inválidos na requisição
- `401 Unauthorized`: Usuário não autenticado
- `403 Forbidden`: Usuário não autorizado para esta operação
- `404 Not Found`: Despesa variável não encontrada
- `409 Conflict`: Nome já existe para este usuário

## Autenticação

Todas as rotas requerem autenticação via JWT Token.

**Header necessário:**
```
Authorization: Bearer <seu_jwt_token>
```
