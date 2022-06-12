from django.apps import AppConfig


class DeepcomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deepcom'
    videos_path = 'C:/Users/migue/Documents/U/4to/TFG/Videos'
    allowed_extensions = ('.mp4')
