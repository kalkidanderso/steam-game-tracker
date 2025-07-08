"""
Utility Functions Module
========================

Professional utilities for logging, validation, and common operations.
"""

import logging
import sys
from datetime import datetime, timedelta
from typing import Any, Optional
import re
import time
from pathlib import Path

from .config import Config


def setup_logging(level: str = 'INFO') -> logging.Logger:
    """
    Set up professional logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('steam_tracker.log', mode='a')
        ]
    )
    
    logger = logging.getLogger('SteamGameTracker')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Suppress noisy third-party loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    return logger


def validate_config(config: Config) -> bool:
    """
    Validate configuration parameters.
    
    Args:
        config: Configuration object to validate
    
    Returns:
        True if configuration is valid, False otherwise
    """
    logger = logging.getLogger('SteamGameTracker')
    
    # Validate game name
    if not config.game_name or not isinstance(config.game_name, str):
        logger.error("Game name must be a non-empty string")
        return False
    
    # Validate Steam App ID
    if not isinstance(config.steam_app_id, int) or config.steam_app_id <= 0:
        logger.error("Steam App ID must be a positive integer")
        return False
    
    # Validate tracking days
    if not isinstance(config.tracking_days, int) or config.tracking_days <= 0:
        logger.error("Tracking days must be a positive integer")
        return False
    
    if config.tracking_days > 365:
        logger.warning("Tracking period exceeds 365 days, this may take a long time")
    
    logger.info("Configuration validation passed")
    return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for cross-platform compatibility.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure filename is not too long
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized


def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger = logging.getLogger('SteamGameTracker')
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        logger.error(f"All retry attempts failed for {func.__name__}: {e}")
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            
        return wrapper
    return decorator


def get_date_range(days: int) -> tuple[datetime, datetime]:
    """
    Get date range for the specified number of days.
    
    Args:
        days: Number of days to go back
    
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def format_number(number: int) -> str:
    """
    Format large numbers with appropriate suffixes.
    
    Args:
        number: Number to format
    
    Returns:
        Formatted number string
    """
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)


def ensure_directory(path: str) -> Path:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path
    
    Returns:
        Path object
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def calculate_correlation(x_values: list, y_values: list) -> float:
    """
    Calculate Pearson correlation coefficient.
    
    Args:
        x_values: First set of values
        y_values: Second set of values
    
    Returns:
        Correlation coefficient (-1 to 1)
    """
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return 0.0
    
    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x * x for x in x_values)
    sum_y2 = sum(y * y for y in y_values)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator

