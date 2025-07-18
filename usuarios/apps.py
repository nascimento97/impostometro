from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    verbose_name = 'Usuários'
    
    def ready(self):
        """
        Método chamado quando o app está pronto.
        Aqui você pode importar signals ou fazer outras configurações.
        """
        pass
