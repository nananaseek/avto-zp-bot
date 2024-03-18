from src.settings.config import settings


def get_app_list():
    app_list = [
        f'{settings.APPLICATIONS_MODULE}.{src}.models' for src in settings.APPLICATIONS
    ]
    return app_list
