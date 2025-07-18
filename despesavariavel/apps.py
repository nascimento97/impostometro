from django.apps import AppConfig


class DespesavariavelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'despesavariavel'
    verbose_name = 'Despesas Variáveis'
    
    def ready(self):
        """
        Método executado quando o app é carregado.
        Usado para registrar signals ou outras configurações.
        """
        pass
