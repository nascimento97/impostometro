from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import DespesaFixa

User = get_user_model()


class DespesaFixaModelTest(TestCase):
    """Testes para o modelo DespesaFixa"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Teste Comercial'
        )
    
    def test_create_despesa_fixa(self):
        """Teste de criação de despesa fixa"""
        despesa = DespesaFixa.objects.create(
            usuario=self.user,
            nome='Aluguel',
            valor=Decimal('1500.00'),
            descricao='Aluguel mensal do estabelecimento'
        )
        
        self.assertEqual(despesa.nome, 'Aluguel')
        self.assertEqual(despesa.valor, Decimal('1500.00'))
        self.assertEqual(despesa.usuario, self.user)
        self.assertTrue(despesa.ativa)
        self.assertIsNotNone(despesa.created_at)
        self.assertIsNotNone(despesa.updated_at)
    
    def test_str_representation(self):
        """Teste da representação string do modelo"""
        despesa = DespesaFixa.objects.create(
            usuario=self.user,
            nome='Energia',
            valor=Decimal('300.00')
        )
        
        expected = f"Energia - R$ 300.00 ({self.user.username})"
        self.assertEqual(str(despesa), expected)
    
    def test_valor_formatado_property(self):
        """Teste da propriedade valor_formatado"""
        despesa = DespesaFixa.objects.create(
            usuario=self.user,
            nome='Internet',
            valor=Decimal('150.50')
        )
        
        self.assertEqual(despesa.valor_formatado, 'R$ 150,50')
    
    def test_status_text_property(self):
        """Teste da propriedade status_text"""
        despesa_ativa = DespesaFixa.objects.create(
            usuario=self.user,
            nome='Água',
            valor=Decimal('80.00'),
            ativa=True
        )
        
        despesa_inativa = DespesaFixa.objects.create(
            usuario=self.user,
            nome='Telefone',
            valor=Decimal('50.00'),
            ativa=False
        )
        
        self.assertEqual(despesa_ativa.status_text, 'Ativa')
        self.assertEqual(despesa_inativa.status_text, 'Inativa')
    
    def test_unique_together_constraint(self):
        """Teste da constraint unique_together para usuario e nome"""
        DespesaFixa.objects.create(
            usuario=self.user,
            nome='Segurança',
            valor=Decimal('200.00')
        )
        
        # Tentativa de criar outra despesa com o mesmo nome para o mesmo usuário
        with self.assertRaises(Exception):  # IntegrityError será levantado
            DespesaFixa.objects.create(
                usuario=self.user,
                nome='Segurança',
                valor=Decimal('250.00')
            )
    
    def test_clean_validation_negative_value(self):
        """Teste da validação de valor negativo"""
        despesa = DespesaFixa(
            usuario=self.user,
            nome='Teste',
            valor=Decimal('-100.00')
        )
        
        with self.assertRaises(ValidationError):
            despesa.clean()


class DespesaFixaViewTest(TestCase):
    """Testes para as views de DespesaFixa"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Teste Comercial'
        )
        
        self.despesa = DespesaFixa.objects.create(
            usuario=self.user,
            nome='Aluguel',
            valor=Decimal('1500.00')
        )
    
    def test_queryset_filters_by_user(self):
        """Teste se o queryset filtra por usuário"""
        # Criar outro usuário com despesa
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123',
            nome_comercial='Outro Comercial'
        )
        
        DespesaFixa.objects.create(
            usuario=other_user,
            nome='Energia',
            valor=Decimal('200.00')
        )
        
        # Verificar que cada usuário vê apenas suas despesas
        user_despesas = DespesaFixa.objects.filter(usuario=self.user)
        other_user_despesas = DespesaFixa.objects.filter(usuario=other_user)
        
        self.assertEqual(user_despesas.count(), 1)
        self.assertEqual(other_user_despesas.count(), 1)
        self.assertEqual(user_despesas.first().nome, 'Aluguel')
        self.assertEqual(other_user_despesas.first().nome, 'Energia')
