"""
Test Config Module
=================

Professional unit tests for the configuration module.
"""

import pytest
import json
import tempfile
from pathlib import Path

from src.config import Config


class TestConfig:
    """Test cases for Config class."""
    
    def test_default_initialization(self):
        """Test default configuration initialization."""
        config = Config()
        
        assert config.game_name == "Cyberpunk 2077"
        assert config.steam_app_id == 1091500
        assert config.tracking_days == 30
        assert config.output_dir == "data"
        assert config.rate_limit_delay == 1.0
    
    def test_config_from_dict(self):
        """Test configuration update from dictionary."""
        config = Config()
        
        test_data = {
            "game_name": "Test Game",
            "steam_app_id": 999999,
            "tracking_days": 14
        }
        
        config._update_from_dict(test_data)
        
        assert config.game_name == "Test Game"
        assert config.steam_app_id == 999999
        assert config.tracking_days == 14
    
    def test_config_to_dict(self):
        """Test configuration serialization to dictionary."""
        config = Config()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "game_name" in config_dict
        assert "steam_app_id" in config_dict
        assert "tracking_days" in config_dict
    
    def test_load_from_file(self):
        """Test loading configuration from file."""
        test_config = {
            "game_name": "Test Game",
            "steam_app_id": 123456,
            "tracking_days": 7
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            temp_path = f.name
        
        try:
            config = Config(temp_path)
            
            assert config.game_name == "Test Game"
            assert config.steam_app_id == 123456
            assert config.tracking_days == 7
        finally:
            Path(temp_path).unlink()
    
    def test_save_to_file(self):
        """Test saving configuration to file."""
        config = Config()
        config.game_name = "Save Test Game"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            config.save_to_file(temp_path)
            
            with open(temp_path, 'r') as f:
                saved_config = json.load(f)
            
            assert saved_config["game_name"] == "Save Test Game"
        finally:
            Path(temp_path).unlink()
    
    def test_invalid_config_file(self):
        """Test error handling for invalid config file."""
        with pytest.raises(ValueError):
            Config("nonexistent_file.json")

