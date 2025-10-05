"""
Configuration Manager
Handles loading and saving application configuration
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / 'config' / 'default_config.json'
    USER_CONFIG_PATH = Path(__file__).parent.parent.parent / 'config' / 'user_config.json'
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from files.
        User config overrides default config.
        
        Returns:
            Dict[str, Any]: Merged configuration dictionary
        """
        try:
            # Load default config
            with open(self.DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self.logger.info("Default configuration loaded")
            
            # Load user config if exists and merge
            if self.USER_CONFIG_PATH.exists():
                with open(self.USER_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                self.config = self._merge_configs(self.config, user_config)
                self.logger.info("User configuration loaded and merged")
            
            return self.config
            
        except FileNotFoundError as e:
            self.logger.error(f"Configuration file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            raise
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save user configuration to file.
        
        Args:
            config: Configuration dictionary to save. If None, saves current config.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            config_to_save = config if config is not None else self.config
            
            with open(self.USER_CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2)
            
            self.logger.info("User configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key using dot notation.
        
        Args:
            key: Configuration key (e.g., 'network.default_timeout')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by key using dot notation.
        
        Args:
            key: Configuration key (e.g., 'network.default_timeout')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.logger.debug(f"Configuration updated: {key} = {value}")
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """
        Recursively merge user config into default config.
        
        Args:
            default: Default configuration
            user: User configuration
            
        Returns:
            Merged configuration
        """
        merged = default.copy()
        
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def reset_to_default(self) -> Dict[str, Any]:
        """
        Reset configuration to default values.
        
        Returns:
            Default configuration dictionary
        """
        with open(self.DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.logger.info("Configuration reset to default")
        return self.config
