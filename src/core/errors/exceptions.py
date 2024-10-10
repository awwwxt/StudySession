from config import logger

class StudySessionError(Exception):
    """Базовый класс для всех ошибок"""
    def __init__(self, message: str, is_warning: bool = False):
        logger.warning(message) if is_warning else logger.error(message)

class NoParams(StudySessionError):
    """Не переданы все параметры"""

class BadParams(StudySessionError):
    """Когда один из параметров не такой как надо"""

class ClientError(StudySessionError):
    """Вызывается при различных ошибках в HTTP клиенте"""
    def __init__(self, status: int = None, url: str = None, error: str = None):
        super().__init__(message = f"received status {status} on {url}" if error is None else f"Caused {error} on {url}")