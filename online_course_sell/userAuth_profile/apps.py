from django.apps import AppConfig


class UserauthProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userAuth_profile'
    
    def ready(self):
        import userAuth_profile.signals
