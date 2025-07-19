# Configuração de Variáveis de Ambiente com Django-Environ

Este projeto agora utiliza o `django-environ` para gerenciar variáveis de ambiente de forma segura e organizada.

## Arquivos Criados/Modificados

### 1. `.env` (Arquivo de configuração local)
Contém as variáveis de ambiente para desenvolvimento local. **NUNCA deve ser commitado no git**.

### 2. `.env.example` (Template de variáveis)
Template que mostra quais variáveis são necessárias. Este arquivo deve ser commitado.

### 3. `settings.py` (Configurações atualizadas)
O arquivo de configurações do Django foi atualizado para usar as variáveis de ambiente.

## Variáveis de Ambiente Configuradas

- **SECRET_KEY**: Chave secreta do Django
- **DEBUG**: Modo debug (True/False)
- **ALLOWED_HOSTS**: Hosts permitidos (separados por vírgula)
- **DATABASE_URL**: URL de conexão com o banco de dados
- **CORS_ALLOWED_ORIGINS**: Origens permitidas para CORS (separadas por vírgula)

## Como Usar

### Desenvolvimento Local
1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edite o arquivo `.env` com suas configurações locais

3. Execute o projeto normalmente:
   ```bash
   python manage.py runserver
   ```

### Produção
1. Configure as variáveis de ambiente diretamente no servidor ou no serviço de hospedagem
2. Gere uma nova `SECRET_KEY` para produção
3. Configure `DEBUG=False`
4. Configure os `ALLOWED_HOSTS` com seu domínio

## Comandos de Teste

Para verificar se a configuração está funcionando:
```bash
python manage.py check
```

## Benefícios

1. **Segurança**: Senhas e chaves secretas não ficam no código
2. **Flexibilidade**: Diferentes configurações para desenvolvimento/produção
3. **Simplicidade**: Gerenciamento centralizado de configurações
4. **Boas Práticas**: Segue as recomendações do 12-factor app

## Importante

- O arquivo `.env` está no `.gitignore` e não será commitado
- Sempre use o arquivo `.env.example` como referência
- Para produção, gere uma nova SECRET_KEY segura
