from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo customizado de usuário para comerciantes.
    Estende AbstractUser para incluir campos específicos do negócio.
    """
    nome_comercial = models.CharField(
        max_length=255,
        verbose_name="Nome Comercial",
        help_text="Nome da empresa ou estabelecimento comercial"
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone",
        help_text="Telefone para contato"
    )
    cnpj = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        unique=True,
        verbose_name="CNPJ",
        help_text="CNPJ do estabelecimento (formato: XX.XXX.XXX/XXXX-XX)"
    )
    endereco = models.TextField(
        blank=True,
        null=True,
        verbose_name="Endereço",
        help_text="Endereço completo do estabelecimento"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} - {self.nome_comercial}"

    @property
    def nome_completo(self):
        """Retorna o nome completo do usuário"""
        return f"{self.first_name} {self.last_name}".strip()

    def clean(self):
        """Validações customizadas"""
        super().clean()
        if self.cnpj:
            # Remove caracteres não numéricos do CNPJ
            self.cnpj = ''.join(filter(str.isdigit, self.cnpj))
            # Formata o CNPJ
            if len(self.cnpj) == 14:
                self.cnpj = f"{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:]}"
