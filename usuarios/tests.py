from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

Usuario = get_user_model()


class UsuarioModelTest(TestCase):
    """Testes para o modelo Usuario"""

    def setUp(self):
        self.usuario_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'nome_comercial': 'Loja Teste',
            'first_name': 'João',
            'last_name': 'Silva'
        }

    def test_create_usuario(self):
        """Testa a criação de um usuário"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        
        self.assertEqual(usuario.username, 'testuser')
        self.assertEqual(usuario.email, 'test@example.com')
        self.assertEqual(usuario.nome_comercial, 'Loja Teste')
        self.assertTrue(usuario.check_password('testpass123'))
        self.assertTrue(usuario.is_active)
        self.assertFalse(usuario.is_staff)

    def test_usuario_str_method(self):
        """Testa o método __str__ do usuário"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        expected_str = f"{usuario.username} - {usuario.nome_comercial}"
        self.assertEqual(str(usuario), expected_str)

    def test_nome_completo_property(self):
        """Testa a propriedade nome_completo"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        expected_nome = f"{usuario.first_name} {usuario.last_name}"
        self.assertEqual(usuario.nome_completo, expected_nome)

    def test_cnpj_formatting(self):
        """Testa a formatação do CNPJ"""
        self.usuario_data['cnpj'] = '12345678000195'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        usuario.clean()
        self.assertEqual(usuario.cnpj, '12.345.678/0001-95')


class UsuarioAPITest(APITestCase):
    """Testes para a API de usuários"""

    def setUp(self):
        self.usuario_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'nome_comercial': 'Loja Teste',
            'first_name': 'João',
            'last_name': 'Silva'
        }

        self.login_url = reverse('usuario-login')
        self.usuarios_url = reverse('usuario-list')

    def test_create_usuario_api(self):
        """Testa a criação de usuário via API"""
        response = self.client.post(
            self.usuarios_url, 
            self.usuario_data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('usuario', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(Usuario.objects.count(), 1)

    def test_create_usuario_password_mismatch(self):
        """Testa criação com senhas diferentes"""
        data = self.usuario_data.copy()
        data['confirm_password'] = 'different_password'
        
        response = self.client.post(
            self.usuarios_url, 
            data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Usuario.objects.count(), 0)

    def test_create_usuario_email_duplicate(self):
        """Testa criação com email duplicado"""
        # Cria primeiro usuário
        Usuario.objects.create_user(
            username='user1',
            email='test@example.com',
            password='pass123',
            nome_comercial='Loja 1'
        )
        
        # Tenta criar segundo usuário com mesmo email
        response = self.client.post(
            self.usuarios_url, 
            self.usuario_data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Usuario.objects.count(), 1)

    def test_login_success(self):
        """Testa login com sucesso"""
        # Cria usuário
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Loja Teste'
        )
        
        # Testa login com username
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('usuario', response.data)

    def test_login_with_email(self):
        """Testa login usando email"""
        # Cria usuário
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Loja Teste'
        )
        
        # Testa login com email
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'testpass123'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        response = self.client.post(self.login_url, {
            'username': 'invaliduser',
            'password': 'invalidpass'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_endpoint_authenticated(self):
        """Testa endpoint /me/ autenticado"""
        # Cria usuário
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Loja Teste'
        )
        
        # Gera token
        refresh = RefreshToken.for_user(usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Testa endpoint
        response = self.client.get(reverse('usuario-me'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_me_endpoint_unauthenticated(self):
        """Testa endpoint /me/ sem autenticação"""
        response = self.client.get(reverse('usuario-me'))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_usuarios_authenticated(self):
        """Testa listagem de usuários autenticado"""
        # Cria usuário
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Loja Teste'
        )
        
        # Gera token
        refresh = RefreshToken.for_user(usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Testa listagem
        response = self.client.get(self.usuarios_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_me_endpoint(self):
        """Testa atualização de dados do usuário"""
        # Cria usuário
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            nome_comercial='Loja Teste'
        )
        
        # Gera token
        refresh = RefreshToken.for_user(usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Atualiza dados
        update_data = {
            'nome_comercial': 'Nova Loja',
            'telefone': '11999999999'
        }
        
        response = self.client.patch(
            reverse('usuario-update-me'), 
            update_data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica se foi atualizado
        usuario.refresh_from_db()
        self.assertEqual(usuario.nome_comercial, 'Nova Loja')
        self.assertEqual(usuario.telefone, '11999999999')
