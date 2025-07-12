import logging
from src.common.configs.settings import settings

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with consistent formatting and configuration.
    
    Args:
        name: The name of the logger (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
        
        # Create formatter
        formatter = logging.Formatter(settings.LOG_FORMAT)
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger 