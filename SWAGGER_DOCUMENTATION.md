# Documentação Swagger - Impostômetro API

## 📚 Sobre

Este projeto agora inclui documentação automática da API usando Swagger/OpenAPI 3.0. A documentação é gerada automaticamente a partir do código e fornece uma interface interativa para testar todos os endpoints.

## 🔗 URLs da Documentação

Com o servidor rodando (`python manage.py runserver`), você pode acessar:

### Swagger UI (Interface Principal)
```
http://127.0.0.1:8000/swagger/
```
- Interface interativa e moderna
- Permite testar endpoints diretamente
- Suporte completo a autenticação JWT
- Visualização de schemas e modelos

### ReDoc (Interface Alternativa)
```
http://127.0.0.1:8000/redoc/
```
- Interface mais focada em documentação
- Melhor para leitura e referência
- Layout mais limpo e organizado

### Schema JSON
```
http://127.0.0.1:8000/swagger.json
http://127.0.0.1:8000/api/schema/
```
- Schema OpenAPI em formato JSON
- Útil para integração com outras ferramentas
- Pode ser importado em clientes API

## 🔐 Autenticação no Swagger

A API utiliza autenticação JWT. Para testar endpoints protegidos no Swagger:

### 1. Obter Token de Acesso

**Opção A: Usar endpoint de login customizado**
```bash
POST /usuarios/login/
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Opção B: Usar endpoint JWT padrão**
```bash
POST /api/auth/token/
{
    "username": "seu_usuario", 
    "password": "sua_senha"
}
```

### 2. Configurar Autenticação no Swagger

1. Clique no botão **"Authorize"** no topo da página do Swagger
2. No campo **"Bearer"**, digite: `Bearer seu_token_aqui`
3. Clique em **"Authorize"**
4. Agora todos os endpoints protegidos podem ser testados

### Exemplo de Token:
```
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY...
```

## 📋 Estrutura da API

### Apps Documentadas

1. **👥 Usuários** (`/usuarios/`)
   - CRUD completo de usuários
   - Login/Logout
   - Perfil do usuário autenticado

2. **💰 Despesas Fixas** (`/despesas-fixas/`)
   - Gerenciamento de despesas fixas mensais

3. **📊 Despesas Variáveis** (`/despesas-variaveis/`)
   - Controle de despesas variáveis

4. **🥕 Ingredientes** (`/ingredientes/`)
   - Cadastro e gerenciamento de ingredientes

5. **📦 Produtos** (`/produtos/`)
   - Cadastro e gerenciamento de produtos

6. **📈 Análise Financeira** (`/analise-financeira/`)
   - Relatórios e análises financeiras

## 🛠️ Funcionalidades do Swagger

### ✅ Recursos Implementados

- **Documentação automática** de todos os endpoints
- **Schemas detalhados** para request/response
- **Autenticação JWT** integrada
- **Testes interativos** diretamente na interface
- **Filtros e parâmetros** documentados
- **Códigos de resposta** com exemplos
- **Modelos de dados** com descrições

### 📝 Informações Incluídas

Para cada endpoint você encontrará:

- **Método HTTP** (GET, POST, PUT, PATCH, DELETE)
- **URL** completa
- **Parâmetros** obrigatórios e opcionais
- **Body** da requisição com exemplo
- **Respostas possíveis** com códigos HTTP
- **Autenticação** necessária
- **Filtros** disponíveis

## 🔧 Configuração Técnica

### Dependências Adicionadas

```bash
# requirements.txt
drf-yasg==1.21.8
```

### Settings Configurados

```python
# core/settings.py
INSTALLED_APPS = [
    # ...
    'drf_yasg',
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    # ... outras configurações
}
```

### URLs Configuradas

```python
# core/urls.py
# URLs do Swagger - apenas em desenvolvimento
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0)),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0)),
    ]
```

## 🚀 Como Usar

### 1. Iniciar o Servidor
```bash
python manage.py runserver
```

### 2. Acessar o Swagger
Abra o navegador em: `http://127.0.0.1:8000/swagger/`

### 3. Fazer Login
- Use o endpoint `/usuarios/login/` para obter um token
- Configure a autenticação clicando em "Authorize"

### 4. Testar Endpoints
- Navegue pelos diferentes apps/tags
- Clique em qualquer endpoint para ver detalhes
- Use "Try it out" para fazer requisições reais

## 📚 Melhorias Futuras

### Possíveis Implementações

- **Versionamento da API** (v1, v2, etc.)
- **Documentação de erros** mais detalhada
- **Exemplos de uso** em diferentes linguagens
- **Rate limiting** documentado
- **Webhooks** se houver
- **Upload de arquivos** se necessário

### Como Melhorar a Documentação

Para adicionar mais detalhes a qualquer endpoint:

```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    operation_summary="Título do endpoint",
    operation_description="Descrição detalhada...",
    request_body=SerializerClass,
    responses={
        200: SerializerClass,
        400: 'Erro de validação',
        404: 'Não encontrado'
    }
)
def meu_endpoint(self, request):
    # implementação
```

## 🐛 Solução de Problemas

### Problemas Comuns

1. **Swagger não carrega**
   - Verifique se `DEBUG=True`
   - Confirme se `drf_yasg` está em `INSTALLED_APPS`

2. **Autenticação não funciona**
   - Verifique se o token está no formato `Bearer TOKEN`
   - Confirme se o token não expirou

3. **Endpoints não aparecem**
   - Verifique se as URLs estão corretamente configuradas
   - Confirme se as views têm as permissões adequadas

### Logs Úteis

Para debug, adicione no settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'drf_yasg': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

**Desenvolvido para o projeto Impostômetro** 📊
*Documentação automática que facilita o desenvolvimento e integração da API*
