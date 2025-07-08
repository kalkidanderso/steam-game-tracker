"""
Configuration Management Module
==============================

Handles application configuration with professional defaults and validation.
"""

import json
import os
from typing import Optional, Dict, Any


class Config:
    """Configuration manager for Steam Game Tracker application."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration with professional defaults."""
        # Default configuration
        self.game_name: str = "Cyberpunk 2077"
        self.steam_app_id: int = 1091500
        self.tracking_days: int = 30
        
        # API Configuration
        self.reddit_client_id: str = os.getenv('REDDIT_CLIENT_ID', '')
        self.reddit_client_secret: str = os.getenv('REDDIT_CLIENT_SECRET', '')
        self.reddit_user_agent: str = os.getenv('REDDIT_USER_AGENT', 'SteamGameTracker/1.0')
        
        # Output settings
        self.output_dir: str = 'data'
        self.log_level: str = 'INFO'
        self.enable_caching: bool = True
        self.cache_duration: int = 3600  # 1 hour
        
        # Rate limiting
        self.rate_limit_delay: float = 1.0  # seconds between requests
        self.max_retries: int = 3
        
        # Load from file if provided
        if config_path:
            self.load_from_file(config_path)
    
    def load_from_file(self, config_path: str) -> None:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
                self._update_from_dict(config_data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading configuration file: {e}")
    
    def _update_from_dict(self, config_data: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        for key, value in config_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'game_name': self.game_name,
            'steam_app_id': self.steam_app_id,
            'tracking_days': self.tracking_days,
            'output_dir': self.output_dir,
            'log_level': self.log_level,
            'enable_caching': self.enable_caching,
            'cache_duration': self.cache_duration,
            'rate_limit_delay': self.rate_limit_delay,
            'max_retries': self.max_retries
        }
    
    def save_to_file(self, config_path: str) -> None:
        """Save configuration to JSON file."""
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(self.to_dict(), file, indent=2)

