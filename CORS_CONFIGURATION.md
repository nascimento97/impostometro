# Configuração do CORS (Cross-Origin Resource Sharing)

## Sobre

O `django-cors-headers` foi configurado para permitir que páginas estáticas hospedadas no GitHub Pages possam fazer requisições HTTPS para esta API Django.

## Configurações Aplicadas

### 1. Instalação
- Adicionado `django-cors-headers==4.6.0` ao `requirements.txt`
- Instalado no ambiente virtual do projeto

### 2. Settings.py

#### Apps Instalados
```python
THIRD_PARTY_APPS = [
    'corsheaders',  # Adicionado
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_yasg',
]
```

#### Middleware
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Adicionado no topo
    'django.middleware.security.SecurityMiddleware',
    # ... outros middlewares
]
```

#### Configurações CORS
```python
# Permite requisições de páginas estáticas do GitHub Pages
CORS_ALLOWED_ORIGINS = [
    "https://nascimento97.github.io",
]

# Permite todos os métodos HTTP (GET, POST, PUT, DELETE, PATCH, OPTIONS)
CORS_ALLOW_ALL_METHODS = True

# Headers permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Permite credenciais (cookies, headers de autorização)
CORS_ALLOW_CREDENTIALS = True

# Configurações adicionais para HTTPS
CORS_ALLOW_PRIVATE_NETWORK = True
```

## Funcionalidades Habilitadas

- ✅ Requisições HTTPS do GitHub Pages (`https://nascimento97.github.io`)
- ✅ Todos os métodos HTTP (GET, POST, PUT, DELETE, PATCH, OPTIONS)
- ✅ Headers de autorização (Bearer tokens)
- ✅ Credenciais de autenticação
- ✅ Suporte para redes privadas

## Como Usar

1. Suas páginas estáticas no GitHub Pages (`https://nascimento97.github.io`) podem agora fazer requisições para a API
2. Certifique-se de incluir o header `Authorization: Bearer <token>` nas requisições autenticadas
3. Use os métodos HTTP apropriados para cada endpoint da API

## Segurança

- A configuração permite apenas o domínio específico do GitHub Pages
- Mantém a autenticação JWT obrigatória para endpoints protegidos
- Headers são restringidos aos necessários para operação

## Testando

Para testar se o CORS está funcionando:

```bash
# Execute o servidor de desenvolvimento
python manage.py runserver

# Em outro terminal, teste com curl:
curl -H "Origin: https://nascimento97.github.io" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: authorization" \
     -X OPTIONS \
     http://localhost:8000/api/usuarios/
```

Se configurado corretamente, você deve ver headers `Access-Control-Allow-*` na resposta.
