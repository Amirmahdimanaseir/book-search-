"""
Logging configuration for the Book Database System
"""

import logging
import logging.handlers
from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def setup_logger(name: str, level: str = LOG_LEVEL) -> logging.Logger:
    """
    Setup and configure logger with file and console handlers.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT
    )
    file_handler.setLevel(getattr(logging, level))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Module-level logger
logger = setup_logger(__name__)
