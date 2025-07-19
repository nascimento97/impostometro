from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from produtos.models import Produto
from .models import AnaliseFinanceira

User = get_user_model()


class AnaliseFinanceiraModelTest(TestCase):
    """
    Testes para o modelo AnaliseFinanceira.
    """
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Empresa Teste'
        )
        
        self.produto = Produto.objects.create(
            usuario=self.user,
            nome='Produto Teste',
            descricao='Descrição do produto teste',
            tempo_preparo=30,
            margem_lucro=Decimal('50.00'),
            periodo_analise=30
        )
    
    def test_criacao_analise_financeira(self):
        """Testa a criação de uma análise financeira"""
        analise = AnaliseFinanceira.objects.create(
            produto=self.produto,
            custo_ingredientes=Decimal('10.00'),
            custo_despesas_fixas=Decimal('5.00'),
            custo_despesas_variaveis=Decimal('3.00'),
            preco_venda_sugerido=Decimal('25.00'),
            faturamento_previsto=Decimal('750.00'),
            lucro_previsto=Decimal('210.00')
        )
        
        self.assertEqual(analise.produto, self.produto)
        self.assertEqual(analise.custo_total_producao, Decimal('18.00'))
        self.assertIn('Produto Teste', str(analise))
    
    def test_margem_lucro_real(self):
        """Testa o cálculo da margem de lucro real"""
        analise = AnaliseFinanceira.objects.create(
            produto=self.produto,
            custo_ingredientes=Decimal('10.00'),
            custo_despesas_fixas=Decimal('5.00'),
            custo_despesas_variaveis=Decimal('5.00'),
            preco_venda_sugerido=Decimal('30.00'),
            faturamento_previsto=Decimal('900.00'),
            lucro_previsto=Decimal('300.00')
        )
        
        # Margem esperada: ((30 - 20) / 20) * 100 = 50%
        self.assertEqual(analise.margem_lucro_real, Decimal('50.00'))
    
    def test_formatacao_valores(self):
        """Testa a formatação dos valores monetários"""
        analise = AnaliseFinanceira.objects.create(
            produto=self.produto,
            custo_ingredientes=Decimal('10.50'),
            custo_despesas_fixas=Decimal('5.25'),
            custo_despesas_variaveis=Decimal('2.75'),
            preco_venda_sugerido=Decimal('27.75'),
            faturamento_previsto=Decimal('832.50'),
            lucro_previsto=Decimal('277.50')
        )
        
        self.assertEqual(analise.custo_total_formatado, 'R$ 18.50')
        self.assertEqual(analise.preco_venda_formatado, 'R$ 27.75')
        self.assertEqual(analise.lucro_formatado, 'R$ 277.50')


class AnaliseFinanceiraAPITest(APITestCase):
    """
    Testes para a API de análises financeiras.
    """
    
    def setUp(self):
        """Configuração inicial para os testes da API"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Empresa Teste'
        )
        
        self.produto = Produto.objects.create(
            usuario=self.user,
            nome='Produto API Teste',
            descricao='Descrição do produto para teste da API',
            tempo_preparo=45,
            margem_lucro=Decimal('40.00'),
            periodo_analise=30
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_criar_analise_financeira(self):
        """Testa a criação de análise via API"""
        url = reverse('analise-financeira-list')
        data = {
            'produto': self.produto.id,
            'custo_ingredientes': '15.00',
            'custo_despesas_fixas': '8.00',
            'custo_despesas_variaveis': '4.00',
            'preco_venda_sugerido': '35.00',
            'faturamento_previsto': '1050.00',
            'lucro_previsto': '240.00'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AnaliseFinanceira.objects.count(), 1)
    
    def test_listar_analises_financeiras(self):
        """Testa a listagem de análises via API"""
        # Cria algumas análises
        AnaliseFinanceira.objects.create(
            produto=self.produto,
            custo_ingredientes=Decimal('10.00'),
            custo_despesas_fixas=Decimal('5.00'),
            custo_despesas_variaveis=Decimal('3.00'),
            preco_venda_sugerido=Decimal('25.00'),
            faturamento_previsto=Decimal('750.00'),
            lucro_previsto=Decimal('210.00')
        )
        
        url = reverse('analise-financeira-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_validacao_preco_venda(self):
        """Testa validação do preço de venda menor que custo total"""
        url = reverse('analise-financeira-list')
        data = {
            'produto': self.produto.id,
            'custo_ingredientes': '15.00',
            'custo_despesas_fixas': '8.00',
            'custo_despesas_variaveis': '4.00',
            'preco_venda_sugerido': '20.00',  # Menor que custo total (27.00)
            'faturamento_previsto': '600.00',
            'lucro_previsto': '-210.00'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('preco_venda_sugerido', response.data)
    
    def test_stats_analises(self):
        """Testa o endpoint de estatísticas"""
        # Cria análises para estatísticas
        AnaliseFinanceira.objects.create(
            produto=self.produto,
            custo_ingredientes=Decimal('10.00'),
            custo_despesas_fixas=Decimal('5.00'),
            custo_despesas_variaveis=Decimal('3.00'),
            preco_venda_sugerido=Decimal('25.00'),
            faturamento_previsto=Decimal('750.00'),
            lucro_previsto=Decimal('210.00')
        )
        
        url = reverse('analise-financeira-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_analises', response.data)
        self.assertIn('custo_medio', response.data)
        self.assertIn('margem_lucro_media', response.data)
