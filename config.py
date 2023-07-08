class Config:
    """Класс с параметрами запуска. Заполняется при старте проекта conftest.py:pytest_configure"""
    log_level = 'INFO'

    class Api:
        url: str = ''
