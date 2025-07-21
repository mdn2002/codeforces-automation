import json
import os
from typing import Dict, Any, Optional

class ConfigParser:
    """Handles loading and validation of configuration settings"""
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            if not os.path.exists(self.config_path):
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate required fields
            self.validate_config(config)
            return config
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise Exception(f"Failed to load configuration: {e}")
    
    def validate_config(self, config: Dict[str, Any]) -> None:
        """Validate that all required configuration fields are present"""
        required_fields = [
            'output_directory',
            'template_directory',
            'default_language',
            'file_naming',
            'editor',
            'keyboard_shortcut'
        ]
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required configuration field: {field}")
        
        # Validate file naming configuration
        file_naming = config.get('file_naming', {})
        required_file_fields = ['solution_file', 'input_prefix', 'output_prefix']
        for field in required_file_fields:
            if field not in file_naming:
                raise ValueError(f"Missing required file naming field: {field}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_file_naming(self) -> Dict[str, str]:
        """Get file naming configuration"""
        return self.config.get('file_naming', {})
    
    def get_editor_config(self) -> Dict[str, Any]:
        """Get editor configuration"""
        return self.config.get('editor', {})
    
    def get_keyboard_shortcut(self) -> Dict[str, Any]:
        """Get keyboard shortcut configuration"""
        return self.config.get('keyboard_shortcut', {})
    
    def reload(self) -> None:
        """Reload configuration from file"""
        self.config = self.load_config()
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to save configuration: {e}") 