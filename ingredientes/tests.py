from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Ingrediente
from .serializers import IngredienteSerializer, IngredienteCreateSerializer

User = get_user_model()


class IngredienteModelTest(TestCase):
    """
    Testes para o modelo Ingrediente.
    """
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Teste Comercial'
        )
    
    def test_create_ingrediente(self):
        """Testa a criação de um ingrediente."""
        ingrediente = Ingrediente.objects.create(
            usuario=self.user,
            nome='Farinha de Trigo',
            preco_por_unidade=Decimal('5.50'),
            unidade_medida='kg',
            fornecedor='Atacadão'
        )
        
        self.assertEqual(ingrediente.nome, 'Farinha de Trigo')
        self.assertEqual(ingrediente.preco_por_unidade, Decimal('5.50'))
        self.assertEqual(ingrediente.unidade_medida, 'kg')
        self.assertEqual(ingrediente.fornecedor, 'Atacadão')
        self.assertEqual(str(ingrediente), 'Farinha de Trigo - R$ 5.50/kg')
    
    def test_ingrediente_unique_together(self):
        """Testa a restrição de nome único por usuário."""
        Ingrediente.objects.create(
            usuario=self.user,
            nome='Açúcar',
            preco_por_unidade=Decimal('3.00'),
            unidade_medida='kg'
        )
        
        # Tentar criar outro ingrediente com o mesmo nome deve gerar erro
        with self.assertRaises(Exception):
            Ingrediente.objects.create(
                usuario=self.user,
                nome='Açúcar',
                preco_por_unidade=Decimal('3.50'),
                unidade_medida='kg'
            )
    
    def test_preco_negative_validation(self):
        """Testa validação de preço negativo."""
        ingrediente = Ingrediente(
            usuario=self.user,
            nome='Teste',
            preco_por_unidade=Decimal('-1.00'),
            unidade_medida='kg'
        )
        
        with self.assertRaises(ValidationError):
            ingrediente.clean()
    
    def test_preco_too_high_validation(self):
        """Testa validação de preço muito alto."""
        ingrediente = Ingrediente(
            usuario=self.user,
            nome='Teste',
            preco_por_unidade=Decimal('1000000.00'),
            unidade_medida='kg'
        )
        
        with self.assertRaises(ValidationError):
            ingrediente.clean()
    
    def test_properties(self):
        """Testa as propriedades do modelo."""
        ingrediente = Ingrediente.objects.create(
            usuario=self.user,
            nome='Leite',
            preco_por_unidade=Decimal('4.50'),
            unidade_medida='litro',
            fornecedor='Laticínios ABC'
        )
        
        self.assertEqual(ingrediente.custo_formatado, 'R$ 4.50 por litro')
        self.assertEqual(
            ingrediente.info_completa, 
            'Leite (R$ 4.50 por litro) - Laticínios ABC'
        )


class IngredienteAPITest(APITestCase):
    """
    Testes para a API de ingredientes.
    """
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Teste Comercial'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_ingrediente_api(self):
        """Testa a criação de ingrediente via API."""
        data = {
            'nome': 'Farinha de Trigo',
            'preco_por_unidade': '5.50',
            'unidade_medida': 'kg',
            'fornecedor': 'Atacadão'
        }
        
        response = self.client.post('/api/ingredientes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingrediente.objects.count(), 1)
        
        ingrediente = Ingrediente.objects.first()
        self.assertEqual(ingrediente.usuario, self.user)
        self.assertEqual(ingrediente.nome, 'Farinha de Trigo')
    
    def test_list_ingredientes_api(self):
        """Testa a listagem de ingredientes via API."""
        Ingrediente.objects.create(
            usuario=self.user,
            nome='Açúcar',
            preco_por_unidade=Decimal('3.00'),
            unidade_medida='kg'
        )
        
        response = self.client.get('/api/ingredientes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_update_ingrediente_api(self):
        """Testa a atualização de ingrediente via API."""
        ingrediente = Ingrediente.objects.create(
            usuario=self.user,
            nome='Leite',
            preco_por_unidade=Decimal('4.00'),
            unidade_medida='litro'
        )
        
        data = {
            'nome': 'Leite Integral',
            'preco_por_unidade': '4.50',
            'unidade_medida': 'litro',
            'fornecedor': 'Laticínios XYZ'
        }
        
        response = self.client.put(f'/api/ingredientes/{ingrediente.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        ingrediente.refresh_from_db()
        self.assertEqual(ingrediente.nome, 'Leite Integral')
        self.assertEqual(ingrediente.preco_por_unidade, Decimal('4.50'))
    
    def test_delete_ingrediente_api(self):
        """Testa a exclusão de ingrediente via API."""
        ingrediente = Ingrediente.objects.create(
            usuario=self.user,
            nome='Ovos',
            preco_por_unidade=Decimal('0.50'),
            unidade_medida='unidade'
        )
        
        response = self.client.delete(f'/api/ingredientes/{ingrediente.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ingrediente.objects.count(), 0)
    
    def test_search_ingredientes_api(self):
        """Testa a busca de ingredientes via API."""
        Ingrediente.objects.create(
            usuario=self.user,
            nome='Farinha de Trigo',
            preco_por_unidade=Decimal('5.50'),
            unidade_medida='kg'
        )
        
        response = self.client.get('/api/ingredientes/search/?q=farinha')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_stats_ingredientes_api(self):
        """Testa as estatísticas de ingredientes via API."""
        Ingrediente.objects.create(
            usuario=self.user,
            nome='Açúcar',
            preco_por_unidade=Decimal('3.00'),
            unidade_medida='kg'
        )
        Ingrediente.objects.create(
            usuario=self.user,
            nome='Farinha',
            preco_por_unidade=Decimal('5.00'),
            unidade_medida='kg'
        )
        
        response = self.client.get('/api/ingredientes/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_ingredientes'], 2)
        self.assertEqual(response.data['precos']['medio'], 4.0)


class IngredienteSerializerTest(TestCase):
    """
    Testes para os serializers de ingredientes.
    """
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Teste Comercial'
        )
    
    def test_ingrediente_serializer_validation(self):
        """Testa validações do serializer."""
        data = {
            'nome': 'A',  # Nome muito curto
            'preco_por_unidade': '-1.00',  # Preço negativo
            'unidade_medida': '',  # Unidade vazia
        }
        
        serializer = IngredienteCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        
        self.assertIn('nome', serializer.errors)
        self.assertIn('preco_por_unidade', serializer.errors)
        self.assertIn('unidade_medida', serializer.errors)
    
    def test_ingrediente_serializer_valid_data(self):
        """Testa serializer com dados válidos."""
        data = {
            'nome': 'Farinha de Trigo',
            'preco_por_unidade': '5.50',
            'unidade_medida': 'kg',
            'fornecedor': 'Atacadão'
        }
        
        serializer = IngredienteCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
