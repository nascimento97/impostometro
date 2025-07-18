# API de Usuários - ImpostoMetro

## Visão Geral

A API de usuários do ImpostoMetro fornece endpoints completos para gerenciamento de comerciantes, incluindo criação, autenticação, atualização e listagem de usuários.

## Base URL

```
http://localhost:8000/api/
```

## Autenticação

A API utiliza autenticação JWT (JSON Web Tokens). Após o login, inclua o token de acesso no header das requisições:

```
Authorization: Bearer <seu_access_token>
```

## Endpoints

### 1. Criar Usuário

**POST** `/api/usuarios/`

Cria um novo usuário no sistema.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "username": "comerciante1",
    "email": "comerciante@exemplo.com",
    "password": "senha123@",
    "confirm_password": "senha123@",
    "nome_comercial": "Loja do João",
    "first_name": "João",
    "last_name": "Silva",
    "telefone": "11999999999",
    "cnpj": "12345678000195",
    "endereco": "Rua das Flores, 123, São Paulo - SP"
}
```

**Resposta (201):**
```json
{
    "message": "Usuário criado com sucesso!",
    "usuario": {
        "id": 1,
        "username": "comerciante1",
        "email": "comerciante@exemplo.com",
        "first_name": "João",
        "last_name": "Silva",
        "nome_comercial": "Loja do João",
        "telefone": "11999999999",
        "cnpj": "12.345.678/0001-95",
        "endereco": "Rua das Flores, 123, São Paulo - SP",
        "is_active": true,
        "date_joined": "2025-07-18T20:00:00Z",
        "created_at": "2025-07-18T20:00:00Z",
        "updated_at": "2025-07-18T20:00:00Z",
        "nome_completo": "João Silva"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

### 2. Login

**POST** `/api/usuarios/login/`

Autentica um usuário e retorna tokens JWT.

**Body:**
```json
{
    "username": "comerciante1",  // ou email
    "password": "senha123@"
}
```

**Resposta (200):**
```json
{
    "message": "Login realizado com sucesso!",
    "usuario": {
        "id": 1,
        "username": "comerciante1",
        "email": "comerciante@exemplo.com",
        "nome_comercial": "Loja do João",
        // ... outros campos
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

### 3. Logout

**POST** `/api/usuarios/logout/`

Invalida o refresh token do usuário.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Resposta (205):**
```json
{
    "message": "Logout realizado com sucesso!"
}
```

### 4. Dados do Usuário Autenticado

**GET** `/api/usuarios/me/`

Retorna os dados do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta (200):**
```json
{
    "id": 1,
    "username": "comerciante1",
    "email": "comerciante@exemplo.com",
    "first_name": "João",
    "last_name": "Silva",
    "nome_comercial": "Loja do João",
    "telefone": "11999999999",
    "cnpj": "12.345.678/0001-95",
    "endereco": "Rua das Flores, 123, São Paulo - SP",
    "is_active": true,
    "date_joined": "2025-07-18T20:00:00Z",
    "created_at": "2025-07-18T20:00:00Z",
    "updated_at": "2025-07-18T20:00:00Z",
    "nome_completo": "João Silva"
}
```

### 5. Atualizar Dados do Usuário Autenticado

**PUT/PATCH** `/api/usuarios/me/`

Atualiza os dados do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body (PATCH - campos opcionais):**
```json
{
    "nome_comercial": "Nova Loja do João",
    "telefone": "11888888888",
    "endereco": "Nova Rua, 456, São Paulo - SP"
}
```

**Resposta (200):**
```json
{
    "message": "Dados atualizados com sucesso!",
    "usuario": {
        // dados atualizados do usuário
    }
}
```

### 6. Listar Usuários

**GET** `/api/usuarios/`

Lista todos os usuários (requer autenticação).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search`: Busca por username, email, nome_comercial, first_name ou last_name
- `is_active`: Filtra por status ativo (true/false)
- `page`: Número da página para paginação
- `page_size`: Tamanho da página (padrão: 20)

**Exemplo:**
```
GET /api/usuarios/?search=joão&is_active=true&page=1
```

**Resposta (200):**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/usuarios/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "comerciante1",
            "email": "comerciante@exemplo.com",
            "nome_completo": "João Silva",
            "nome_comercial": "Loja do João",
            "is_active": true,
            "created_at": "2025-07-18T20:00:00Z"
        },
        // ... mais usuários
    ]
}
```

### 7. Detalhes de um Usuário

**GET** `/api/usuarios/{id}/`

Retorna os detalhes de um usuário específico.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta (200):**
```json
{
    "id": 1,
    "username": "comerciante1",
    "email": "comerciante@exemplo.com",
    // ... todos os campos do usuário
}
```

### 8. Atualizar Usuário

**PUT/PATCH** `/api/usuarios/{id}/`

Atualiza um usuário específico.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body:** Similar ao endpoint de criação, mas com campos opcionais para PATCH.

### 9. Desativar Usuário

**DELETE** `/api/usuarios/{id}/`

Desativa um usuário (soft delete).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta (204):**
```json
{
    "message": "Usuário desativado com sucesso!"
}
```

## Códigos de Status HTTP

- **200**: OK - Requisição bem-sucedida
- **201**: Created - Recurso criado com sucesso
- **204**: No Content - Recurso deletado/atualizado sem retorno de conteúdo
- **205**: Reset Content - Logout realizado com sucesso
- **400**: Bad Request - Dados inválidos na requisição
- **401**: Unauthorized - Token de acesso inválido ou ausente
- **403**: Forbidden - Sem permissão para acessar o recurso
- **404**: Not Found - Recurso não encontrado
- **415**: Unsupported Media Type - Content-Type incorreto

## Validações

### Campos Obrigatórios (Criação)
- `username`: Único, 150 caracteres máximo
- `email`: Único, formato de email válido
- `password`: Mínimo 8 caracteres, seguindo validadores do Django
- `confirm_password`: Deve ser igual ao password
- `nome_comercial`: 255 caracteres máximo

### Validações Específicas
- **CNPJ**: Deve ter 14 dígitos, formatado automaticamente
- **Telefone**: Entre 10 e 11 dígitos
- **Email**: Deve ser único no sistema
- **Username**: Deve ser único no sistema

## Exemplos de Uso

### Criar usuário e fazer login
```bash
# 1. Criar usuário
curl -X POST http://localhost:8000/api/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste",
    "email": "teste@exemplo.com",
    "password": "senha123@",
    "confirm_password": "senha123@",
    "nome_comercial": "Loja Teste"
  }'

# 2. Fazer login
curl -X POST http://localhost:8000/api/usuarios/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teste",
    "password": "senha123@"
  }'

# 3. Usar o token para acessar dados
curl -X GET http://localhost:8000/api/usuarios/me/ \
  -H "Authorization: Bearer <seu_access_token>"
```

## Erros Comuns

### 400 - Dados Inválidos
```json
{
    "email": ["Este email já está em uso."],
    "password": ["Esta senha é muito comum."],
    "confirm_password": ["As senhas não coincidem."]
}
```

### 401 - Token Inválido
```json
{
    "detail": "Token inválido.",
    "code": "token_not_valid"
}
```

### 415 - Content-Type Incorreto
Certifique-se de usar `Content-Type: application/json` nas requisições POST/PUT/PATCH.
