from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Produto, ProdutoIngrediente, ProdutoDespesaFixa, ProdutoDespesaVariavel

User = get_user_model()


class ProdutoModelTest(TestCase):
    """Testes para o modelo Produto"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Empresa Teste'
        )
    
    def test_criar_produto(self):
        """Teste de criação de produto"""
        produto = Produto.objects.create(
            usuario=self.user,
            nome='Produto Teste',
            descricao='Descrição do produto teste',
            tempo_preparo=30,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        
        self.assertEqual(produto.nome, 'Produto Teste')
        self.assertEqual(produto.usuario, self.user)
        self.assertEqual(produto.tempo_preparo, 30)
        self.assertEqual(produto.margem_lucro, Decimal('25.50'))
        self.assertEqual(produto.periodo_analise, 30)
    
    def test_str_produto(self):
        """Teste do método __str__ do produto"""
        produto = Produto.objects.create(
            usuario=self.user,
            nome='Produto Teste',
            tempo_preparo=30,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        
        expected_str = f"Produto Teste - {self.user.nome_comercial}"
        self.assertEqual(str(produto), expected_str)
    
    def test_margem_lucro_formatada(self):
        """Teste da propriedade margem_lucro_formatada"""
        produto = Produto.objects.create(
            usuario=self.user,
            nome='Produto Teste',
            tempo_preparo=30,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        
        self.assertEqual(produto.margem_lucro_formatada, "25.50%")
    
    def test_tempo_preparo_formatado(self):
        """Teste da propriedade tempo_preparo_formatado"""
        # Teste com minutos apenas
        produto1 = Produto.objects.create(
            usuario=self.user,
            nome='Produto 1',
            tempo_preparo=45,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        self.assertEqual(produto1.tempo_preparo_formatado, "45min")
        
        # Teste com horas e minutos
        produto2 = Produto.objects.create(
            usuario=self.user,
            nome='Produto 2',
            tempo_preparo=90,  # 1h 30min
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        self.assertEqual(produto2.tempo_preparo_formatado, "1h 30min")
        
        # Teste com horas exatas
        produto3 = Produto.objects.create(
            usuario=self.user,
            nome='Produto 3',
            tempo_preparo=120,  # 2h
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        self.assertEqual(produto3.tempo_preparo_formatado, "2h")


class ProdutoAPITest(APITestCase):
    """Testes para a API de produtos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Empresa Teste'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_listar_produtos(self):
        """Teste de listagem de produtos"""
        # Criar alguns produtos
        Produto.objects.create(
            usuario=self.user,
            nome='Produto 1',
            tempo_preparo=30,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        Produto.objects.create(
            usuario=self.user,
            nome='Produto 2',
            tempo_preparo=45,
            margem_lucro=Decimal('30.00'),
            periodo_analise=60
        )
        
        url = '/api/produtos/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_criar_produto(self):
        """Teste de criação de produto via API"""
        data = {
            'nome': 'Novo Produto',
            'descricao': 'Descrição do novo produto',
            'tempo_preparo': 60,
            'margem_lucro': '20.00',
            'periodo_analise': 30
        }
        
        url = '/api/produtos/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 1)
        
        produto = Produto.objects.first()
        self.assertEqual(produto.nome, 'Novo Produto')
        self.assertEqual(produto.usuario, self.user)
    
    def test_obter_produto(self):
        """Teste de obtenção de produto específico"""
        produto = Produto.objects.create(
            usuario=self.user,
            nome='Produto Teste',
            tempo_preparo=30,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        
        url = f'/api/produtos/{produto.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Produto Teste')
    
    def test_atualizar_produto(self):
        """Teste de atualização de produto"""
        produto = Produto.objects.create(
            usuario=self.user,
            nome='Produto Original',
            tempo_preparo=30,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        
        data = {
            'nome': 'Produto Atualizado',
            'tempo_preparo': 45,
            'margem_lucro': '30.00',
            'periodo_analise': 60
        }
        
        url = f'/api/produtos/{produto.id}/'
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        produto.refresh_from_db()
        self.assertEqual(produto.nome, 'Produto Atualizado')
        self.assertEqual(produto.tempo_preparo, 45)
    
    def test_deletar_produto(self):
        """Teste de deleção de produto"""
        produto = Produto.objects.create(
            usuario=self.user,
            nome='Produto para Deletar',
            tempo_preparo=30,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        
        url = f'/api/produtos/{produto.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Produto.objects.count(), 0)
    
    def test_buscar_produtos(self):
        """Teste de busca de produtos"""
        Produto.objects.create(
            usuario=self.user,
            nome='Bolo de Chocolate',
            tempo_preparo=60,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        Produto.objects.create(
            usuario=self.user,
            nome='Torta de Limão',
            tempo_preparo=90,
            margem_lucro=Decimal('30.00'),
            periodo_analise=30
        )
        
        url = '/api/produtos/search/?q=chocolate'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['nome'], 'Bolo de Chocolate')
    
    def test_estatisticas_produtos(self):
        """Teste de endpoint de estatísticas"""
        Produto.objects.create(
            usuario=self.user,
            nome='Produto 1',
            tempo_preparo=30,
            margem_lucro=Decimal('20.00'),
            periodo_analise=30
        )
        Produto.objects.create(
            usuario=self.user,
            nome='Produto 2',
            tempo_preparo=60,
            margem_lucro=Decimal('30.00'),
            periodo_analise=60
        )
        
        url = '/api/produtos/stats/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_produtos'], 2)
        self.assertEqual(response.data['tempo_preparo_medio'], 45.0)
        self.assertEqual(response.data['margem_lucro_media'], 25.0)
    
    def test_produto_nome_unico_por_usuario(self):
        """Teste de validação de nome único por usuário"""
        # Criar primeiro produto
        Produto.objects.create(
            usuario=self.user,
            nome='Produto Único',
            tempo_preparo=30,
            margem_lucro=Decimal('25.50'),
            periodo_analise=30
        )
        
        # Tentar criar segundo produto com mesmo nome
        data = {
            'nome': 'Produto Único',
            'tempo_preparo': 45,
            'margem_lucro': '20.00',
            'periodo_analise': 60
        }
        
        url = '/api/produtos/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nome', response.data)
    
    def test_validacao_campos_obrigatorios(self):
        """Teste de validação de campos obrigatórios"""
        data = {}  # Dados vazios
        
        url = '/api/produtos/'
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nome', response.data)
        self.assertIn('tempo_preparo', response.data)
        self.assertIn('margem_lucro', response.data)
        self.assertIn('periodo_analise', response.data)
