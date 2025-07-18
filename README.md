# ImpostoMetro - Calculadora de Precificação

## 📋 Sobre o Projeto

O **ImpostoMetro** é uma API REST desenvolvida em Django que oferece uma solução completa para cálculo de precificação de produtos. A plataforma permite que comerciantes façam login, cadastrem seus produtos com ingredientes detalhados, definam despesas fixas e variáveis, e obtenham análises precisas de custo de produção, faturamento e lucro.

## 🎯 Objetivos

- Facilitar o cálculo preciso de custos de produção
- Automatizar a análise de viabilidade financeira de produtos
- Proporcionar visibilidade sobre margens de lucro
- Auxiliar na tomada de decisões de precificação

## 🚀 Funcionalidades

### Autenticação e Usuários
- ✅ Sistema de login com autenticação JWT
- ✅ Gestão de perfis de comerciantes

### Gestão de Despesas
- 📊 Cadastro e listagem de despesas fixas
- 📊 Cadastro e listagem de despesas variáveis
- 🔗 Vinculação de despesas específicas por produto

### Gestão de Produtos
- 🛍️ Criação e gerenciamento de produtos
- 📝 Especificação detalhada de ingredientes
- ⚖️ Controle de quantidades e custos
- ⏱️ Definição de tempo de preparo

### Análise Financeira
- 💰 Cálculo automático de custo de produção
- 📈 Definição de margem de lucro pretendida
- 📊 Previsão de faturamento e lucro
- 📄 Exportação de relatórios financeiros

## 🏗️ Arquitetura do Sistema

### Modelos de Dados (Models)

#### 1. Usuario (User)
```python
- id: Primary Key
- username: String (único)
- email: Email (único)
- password: String (hash)
- nome_comercial: String
- created_at: DateTime
- updated_at: DateTime
```

#### 2. DespesaFixa
```python
- id: Primary Key
- usuario: ForeignKey(Usuario)
- nome: String
- valor: Decimal
- descricao: Text (opcional)
- ativa: Boolean
- created_at: DateTime
```

#### 3. DespesaVariavel
```python
- id: Primary Key
- usuario: ForeignKey(Usuario)
- nome: String
- valor_por_unidade: Decimal
- unidade_medida: String
- descricao: Text (opcional)
- ativa: Boolean
- created_at: DateTime
```

#### 4. Ingrediente
```python
- id: Primary Key
- usuario: ForeignKey(Usuario)
- nome: String
- preco_por_unidade: Decimal
- unidade_medida: String
- fornecedor: String (opcional)
- created_at: DateTime
```

#### 5. Produto
```python
- id: Primary Key
- usuario: ForeignKey(Usuario)
- nome: String
- descricao: Text
- tempo_preparo: Integer (minutos)
- margem_lucro: Decimal (percentual)
- periodo_analise: Integer (dias)
- created_at: DateTime
- updated_at: DateTime
```

#### 6. ProdutoIngrediente
```python
- id: Primary Key
- produto: ForeignKey(Produto)
- ingrediente: ForeignKey(Ingrediente)
- quantidade: Decimal
- created_at: DateTime
```

#### 7. ProdutoDespesaFixa
```python
- id: Primary Key
- produto: ForeignKey(Produto)
- despesa_fixa: ForeignKey(DespesaFixa)
- created_at: DateTime
```

#### 8. ProdutoDespesaVariavel
```python
- id: Primary Key
- produto: ForeignKey(Produto)
- despesa_variavel: ForeignKey(DespesaVariavel)
- quantidade: Decimal
- created_at: DateTime
```

#### 9. AnaliseFinanceira
```python
- id: Primary Key
- produto: ForeignKey(Produto)
- custo_ingredientes: Decimal
- custo_despesas_fixas: Decimal
- custo_despesas_variaveis: Decimal
- custo_total_producao: Decimal
- preco_venda_sugerido: Decimal
- faturamento_previsto: Decimal
- lucro_previsto: Decimal
- created_at: DateTime
```

## 🔄 Pipeline de Ações do Usuário

### Fluxo Principal
1. **Autenticação**
   - Login com credenciais
   - Recebimento do token JWT

2. **Configuração Inicial**
   - Listar despesas fixas existentes
   - Listar despesas variáveis existentes
   - Cadastrar novas despesas se necessário

3. **Criação do Produto**
   - Definir informações básicas do produto
   - Especificar tempo de preparo

4. **Composição do Produto**
   - Listar ingredientes disponíveis
   - Adicionar ingredientes com quantidades
   - Definir custos por ingrediente

5. **Vinculação de Despesas**
   - Selecionar despesas fixas aplicáveis
   - Selecionar despesas variáveis aplicáveis
   - Definir quantidades para despesas variáveis

6. **Análise Financeira**
   - Definir margem de lucro pretendida
   - Especificar período de análise
   - Gerar cálculos automáticos

7. **Resultados**
   - Visualizar dados de previsão
   - Exportar relatórios
   - Salvar análise para consultas futuras

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.4
- **API**: Django REST Framework 3.16.0
- **Autenticação**: JWT (JSON Web Tokens)
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Documentação**: Swagger/OpenAPI
- **Filtros**: django-filter 25.1

## 📚 Endpoints da API

### Autenticação
- `POST /api/auth/login/` - Login do usuário
- `POST /api/auth/refresh/` - Refresh do token
- `POST /api/auth/logout/` - Logout do usuário

### Despesas
- `GET /api/despesas-fixas/` - Listar despesas fixas
- `POST /api/despesas-fixas/` - Criar despesa fixa
- `GET /api/despesas-variaveis/` - Listar despesas variáveis
- `POST /api/despesas-variaveis/` - Criar despesa variável

### Ingredientes
- `GET /api/ingredientes/` - Listar ingredientes
- `POST /api/ingredientes/` - Criar ingrediente
- `PUT /api/ingredientes/{id}/` - Atualizar ingrediente
- `DELETE /api/ingredientes/{id}/` - Deletar ingrediente

### Produtos
- `GET /api/produtos/` - Listar produtos
- `POST /api/produtos/` - Criar produto
- `GET /api/produtos/{id}/` - Detalhes do produto
- `PUT /api/produtos/{id}/` - Atualizar produto
- `DELETE /api/produtos/{id}/` - Deletar produto

### Análises
- `POST /api/produtos/{id}/calcular/` - Calcular custos e lucros
- `GET /api/produtos/{id}/analise/` - Obter análise financeira
- `GET /api/produtos/{id}/exportar/` - Exportar relatório

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- pip
- virtualenv (recomendado)

### Instalação
```bash
# Clonar o repositório
git clone https://github.com/nascimento97/impostometro.git
cd impostometro

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

### Acesso
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Documentação: http://localhost:8000/api/docs/

## 📋 TODO / Roadmap

- [ ] Implementar autenticação JWT
- [ ] Criar models e migrações
- [ ] Desenvolver endpoints de CRUD
- [ ] Implementar lógica de cálculos
- [ ] Adicionar testes unitários
- [ ] Configurar documentação Swagger
- [ ] Implementar exportação de relatórios
- [ ] Otimizar consultas de banco
- [ ] Adicionar validações de dados
- [ ] Implementar logs de auditoria

## 🤝 Contribuição

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Matheus Nascimento**
- GitHub: [@nascimento97](https://github.com/nascimento97)

---

⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!