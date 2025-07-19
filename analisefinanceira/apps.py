from django.apps import AppConfig


class AnalisefinanceiraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analisefinanceira'
    verbose_name = 'Análises Financeiras'
    
    def ready(self):
        """
        Configurações executadas quando o app é carregado.
        """
        pass
