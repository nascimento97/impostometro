from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import DespesaVariavel

User = get_user_model()


class DespesaVariavelModelTest(TestCase):
    """
    Tests para o modelo DespesaVariavel.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_despesa_variavel(self):
        """Testa a criação de uma despesa variável"""
        despesa = DespesaVariavel.objects.create(
            usuario=self.user,
            nome='Embalagem',
            valor_por_unidade=Decimal('1.50'),
            unidade_medida='unidade',
            descricao='Embalagem para produto'
        )
        
        self.assertEqual(str(despesa), f'Embalagem - {self.user.username}')
        self.assertEqual(despesa.valor_formatado, 'R$ 1,50')
        self.assertEqual(despesa.status_text, 'Ativa')
        self.assertTrue(despesa.ativa)
    
    def test_unique_constraint(self):
        """Testa a constraint de nome único por usuário"""
        DespesaVariavel.objects.create(
            usuario=self.user,
            nome='Embalagem',
            valor_por_unidade=Decimal('1.50'),
            unidade_medida='unidade'
        )
        
        # Tentar criar outra com o mesmo nome deve falhar
        with self.assertRaises(Exception):
            DespesaVariavel.objects.create(
                usuario=self.user,
                nome='Embalagem',
                valor_por_unidade=Decimal('2.00'),
                unidade_medida='unidade'
            )


class DespesaVariavelAPITest(APITestCase):
    """
    Tests para a API de DespesaVariavel.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.despesa_data = {
            'nome': 'Combustível',
            'valor_por_unidade': '5.50',
            'unidade_medida': 'litro',
            'descricao': 'Combustível para entrega',
            'ativa': True
        }
    
    def test_create_despesa_variavel_authenticated(self):
        """Testa criação de despesa variável com usuário autenticado"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/despesas-variaveis/', self.despesa_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DespesaVariavel.objects.count(), 1)
        self.assertEqual(DespesaVariavel.objects.first().usuario, self.user)
    
    def test_create_despesa_variavel_unauthenticated(self):
        """Testa criação de despesa variável sem autenticação"""
        response = self.client.post('/api/despesas-variaveis/', self.despesa_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_despesas_variaveis(self):
        """Testa listagem de despesas variáveis"""
        DespesaVariavel.objects.create(
            usuario=self.user,
            **self.despesa_data
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/despesas-variaveis/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
