import logging
from ..configs.settings import get_settings

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    settings = get_settings()
    logger.setLevel(getattr(logging, settings.log_level))
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(settings.log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger 