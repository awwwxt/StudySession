from config import logger

class StudySessionError(Exception):
    """Базовый класс для всех ошибок"""

class NoParams(StudySessionError):
    """Не переданы все параметры"""

class BadParams(StudySessionError):
    """Когда один из параметров не такой как надо"""