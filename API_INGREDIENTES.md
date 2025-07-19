# API Ingredientes - Documentação

## Visão Geral
A API de Ingredientes permite gerenciar matérias-primas e insumos utilizados na produção de produtos. Cada ingrediente possui informações sobre preço, unidade de medida e fornecedor.

## Modelo de Dados

### Ingrediente
```python
{
    "id": 1,
    "usuario": 1,
    "nome": "Farinha de Trigo",
    "preco_por_unidade": "5.50",
    "unidade_medida": "kg",
    "fornecedor": "Atacadão",
    "created_at": "2025-07-18T10:00:00Z",
    "updated_at": "2025-07-18T10:00:00Z",
    "usuario_nome": "usuario_teste",
    "custo_formatado": "R$ 5,50 por kg",
    "info_completa": "Farinha de Trigo (R$ 5,50 por kg) - Atacadão"
}
```

## Endpoints

### 1. Listar Ingredientes
**GET** `/api/ingredientes/`

Lista todos os ingredientes do usuário autenticado.

**Parâmetros de Query:**
- `unidade_medida` (string): Filtrar por unidade de medida
- `fornecedor` (string): Filtrar por fornecedor
- `search` (string): Buscar por nome ou fornecedor
- `ordering` (string): Ordenar por campos (nome, preco_por_unidade, created_at)

**Exemplo de Resposta:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "nome": "Farinha de Trigo",
            "preco_por_unidade": "5.50",
            "unidade_medida": "kg",
            "fornecedor": "Atacadão",
            "custo_formatado": "R$ 5,50 por kg",
            "created_at": "2025-07-18T10:00:00Z"
        },
        {
            "id": 2,
            "nome": "Açúcar Cristal",
            "preco_por_unidade": "3.20",
            "unidade_medida": "kg",
            "fornecedor": "Supermercado ABC",
            "custo_formatado": "R$ 3,20 por kg",
            "created_at": "2025-07-18T09:30:00Z"
        }
    ]
}
```

### 2. Criar Ingrediente
**POST** `/api/ingredientes/`

Cria um novo ingrediente para o usuário autenticado.

**Headers:**
```
Authorization: Bearer {seu_token_jwt}
Content-Type: application/json
```

**Corpo da Requisição:**
```json
{
    "nome": "Leite Integral",
    "preco_por_unidade": 4.50,
    "unidade_medida": "litro",
    "fornecedor": "Laticínios XYZ"
}
```

**Campos Obrigatórios:**
- `nome`: Nome do ingrediente (mínimo 2 caracteres)
- `preco_por_unidade`: Preço unitário (não negativo, máximo R$ 999.999,99)
- `unidade_medida`: Unidade de medida (máximo 50 caracteres)

**Campos Opcionais:**
- `fornecedor`: Nome do fornecedor ou local de compra

**Exemplo de Resposta (201):**
```json
{
    "id": 3,
    "usuario": 1,
    "nome": "Leite Integral",
    "preco_por_unidade": "4.50",
    "unidade_medida": "litro",
    "fornecedor": "Laticínios XYZ",
    "created_at": "2025-07-18T11:00:00Z",
    "updated_at": "2025-07-18T11:00:00Z",
    "usuario_nome": "comerciante_teste",
    "custo_formatado": "R$ 4,50 por litro",
    "info_completa": "Leite Integral (R$ 4,50 por litro) - Laticínios XYZ"
}
```

### 3. Obter Ingrediente Específico
**GET** `/api/ingredientes/{id}/`

Retorna os detalhes de um ingrediente específico.

**Headers:**
```
Authorization: Bearer {seu_token_jwt}
```

**Exemplo de Resposta (200):**
```json
{
    "id": 1,
    "usuario": 1,
    "nome": "Farinha de Trigo",
    "preco_por_unidade": "5.50",
    "unidade_medida": "kg",
    "fornecedor": "Atacadão",
    "created_at": "2025-07-18T10:00:00Z",
    "updated_at": "2025-07-18T10:00:00Z",
    "usuario_nome": "comerciante_teste",
    "custo_formatado": "R$ 5,50 por kg",
    "info_completa": "Farinha de Trigo (R$ 5,50 por kg) - Atacadão"
}
```

### 4. Atualizar Ingrediente
**PUT** `/api/ingredientes/{id}/` ou **PATCH** `/api/ingredientes/{id}/`

Atualiza um ingrediente existente. PUT requer todos os campos, PATCH permite atualização parcial.

**Headers:**
```
Authorization: Bearer {seu_token_jwt}
Content-Type: application/json
```

**Corpo da Requisição (PUT):**
```json
{
    "nome": "Farinha de Trigo Especial",
    "preco_por_unidade": 6.00,
    "unidade_medida": "kg",
    "fornecedor": "Moinho Premium"
}
```

**Corpo da Requisição (PATCH):**
```json
{
    "preco_por_unidade": 6.00,
    "fornecedor": "Moinho Premium"
}
```

**Exemplo de Resposta (200):**
```json
{
    "id": 1,
    "usuario": 1,
    "nome": "Farinha de Trigo Especial",
    "preco_por_unidade": "6.00",
    "unidade_medida": "kg",
    "fornecedor": "Moinho Premium",
    "created_at": "2025-07-18T10:00:00Z",
    "updated_at": "2025-07-18T11:30:00Z",
    "usuario_nome": "comerciante_teste",
    "custo_formatado": "R$ 6,00 por kg",
    "info_completa": "Farinha de Trigo Especial (R$ 6,00 por kg) - Moinho Premium"
}
```

### 5. Deletar Ingrediente
**DELETE** `/api/ingredientes/{id}/`

Remove um ingrediente específico.

**Headers:**
```
Authorization: Bearer {seu_token_jwt}
```

**Exemplo de Resposta (204):**
```json
{
    "message": "Ingrediente removido com sucesso."
}
```

## Endpoints Especiais

### 6. Buscar Ingredientes
**GET** `/api/ingredientes/search/?q={termo_busca}`

Busca ingredientes por nome ou fornecedor.

**Parâmetros de Query:**
- `q` (obrigatório): Termo de busca

**Exemplo de Requisição:**
```
GET /api/ingredientes/search/?q=farinha
```

**Exemplo de Resposta:**
```json
{
    "count": 2,
    "query": "farinha",
    "results": [
        {
            "id": 1,
            "nome": "Farinha de Trigo",
            "preco_por_unidade": "5.50",
            "unidade_medida": "kg",
            "fornecedor": "Atacadão",
            "custo_formatado": "R$ 5,50 por kg",
            "created_at": "2025-07-18T10:00:00Z"
        },
        {
            "id": 4,
            "nome": "Farinha de Milho",
            "preco_por_unidade": "4.20",
            "unidade_medida": "kg",
            "fornecedor": "Moinho Local",
            "custo_formatado": "R$ 4,20 por kg",
            "created_at": "2025-07-18T09:15:00Z"
        }
    ]
}
```

### 7. Ingredientes por Fornecedor
**GET** `/api/ingredientes/by-fornecedor/?fornecedor={nome_fornecedor}`

Lista ingredientes de um fornecedor específico.

**Parâmetros de Query:**
- `fornecedor` (obrigatório): Nome do fornecedor

**Exemplo de Requisição:**
```
GET /api/ingredientes/by-fornecedor/?fornecedor=Atacadão
```

**Exemplo de Resposta:**
```json
{
    "fornecedor": "Atacadão",
    "count": 3,
    "ingredientes": [
        {
            "id": 1,
            "nome": "Farinha de Trigo",
            "preco_por_unidade": "5.50",
            "unidade_medida": "kg",
            "fornecedor": "Atacadão",
            "custo_formatado": "R$ 5,50 por kg",
            "created_at": "2025-07-18T10:00:00Z"
        },
        {
            "id": 5,
            "nome": "Óleo de Soja",
            "preco_por_unidade": "8.90",
            "unidade_medida": "litro",
            "fornecedor": "Atacadão",
            "custo_formatado": "R$ 8,90 por litro",
            "created_at": "2025-07-18T08:45:00Z"
        }
    ]
}
```

### 8. Estatísticas dos Ingredientes
**GET** `/api/ingredientes/stats/`

Retorna estatísticas dos ingredientes do usuário.

**Headers:**
```
Authorization: Bearer {seu_token_jwt}
```

**Exemplo de Resposta:**
```json
{
    "total_ingredientes": 10,
    "ingredientes_com_fornecedor": 8,
    "percentual_com_fornecedor": 80.0,
    "precos": {
        "medio": 6.75,
        "minimo": 2.50,
        "maximo": 15.00
    },
    "unidades_mais_usadas": [
        ["kg", 6],
        ["litro", 3],
        ["unidade", 1]
    ],
    "fornecedores_mais_usados": [
        ["Atacadão", 4],
        ["Supermercado ABC", 2],
        ["Moinho Local", 2]
    ]
}
```

### 9. Duplicar Ingrediente
**GET** `/api/ingredientes/{id}/duplicar/`

Cria uma cópia de um ingrediente existente.

**Headers:**
```
Authorization: Bearer {seu_token_jwt}
```

**Exemplo de Resposta (201):**
```json
{
    "message": "Ingrediente duplicado com sucesso.",
    "ingrediente_original": 1,
    "novo_ingrediente": {
        "id": 11,
        "usuario": 1,
        "nome": "Farinha de Trigo (Cópia)",
        "preco_por_unidade": "5.50",
        "unidade_medida": "kg",
        "fornecedor": "Atacadão",
        "created_at": "2025-07-18T12:00:00Z",
        "updated_at": "2025-07-18T12:00:00Z",
        "usuario_nome": "comerciante_teste",
        "custo_formatado": "R$ 5,50 por kg",
        "info_completa": "Farinha de Trigo (Cópia) (R$ 5,50 por kg) - Atacadão"
    }
}
```

## Códigos de Erro

### 400 - Bad Request
```json
{
    "nome": ["Este campo é obrigatório."],
    "preco_por_unidade": ["O preço não pode ser negativo."]
}
```

### 401 - Unauthorized
```json
{
    "detail": "As credenciais de autenticação não foram fornecidas."
}
```

### 404 - Not Found
```json
{
    "detail": "Não encontrado."
}
```

### 409 - Conflict
```json
{
    "nome": ["Você já possui um ingrediente com este nome."]
}
```

## Validações

### Nome do Ingrediente
- Obrigatório
- Mínimo de 2 caracteres
- Único por usuário (case insensitive)

### Preço por Unidade
- Obrigatório
- Não pode ser negativo
- Máximo de R$ 999.999,99
- Formato decimal com até 2 casas decimais

### Unidade de Medida
- Obrigatória
- Máximo de 50 caracteres
- Convertida automaticamente para minúsculas

### Fornecedor
- Opcional
- Máximo de 255 caracteres

## Filtros e Ordenação

### Filtros Disponíveis
- `unidade_medida`: Filtrar por unidade de medida específica
- `fornecedor`: Filtrar por fornecedor específico

### Busca
- Busca em `nome` e `fornecedor` (case insensitive)

### Ordenação
- `nome`: Ordenar por nome (crescente/decrescente)
- `preco_por_unidade`: Ordenar por preço (crescente/decrescente)
- `created_at`: Ordenar por data de criação (crescente/decrescente)

**Exemplos:**
```
GET /api/ingredientes/?ordering=nome
GET /api/ingredientes/?ordering=-preco_por_unidade
GET /api/ingredientes/?search=farinha&ordering=created_at
GET /api/ingredientes/?unidade_medida=kg&fornecedor=Atacadão
```

## Autenticação

Todos os endpoints requerem autenticação JWT. Inclua o token no header:

```
Authorization: Bearer {seu_access_token}
```

Para obter o token, use o endpoint de login:
```
POST /api/auth/token/
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

## Notas Importantes

1. **Isolamento de Dados**: Cada usuário vê apenas seus próprios ingredientes
2. **Validação de Duplicatas**: Não é possível criar ingredientes com nomes idênticos para o mesmo usuário
3. **Formatação Automática**: A unidade de medida é automaticamente convertida para minúsculas
4. **Soft Delete**: Os ingredientes são completamente removidos (hard delete)
5. **Performance**: As queries são otimizadas com `select_related` para evitar N+1 queries
