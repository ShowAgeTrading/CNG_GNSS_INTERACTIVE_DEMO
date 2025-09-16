#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: config_manager.py
Purpose: JSON configuration management with schema validation and dot notation
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - json - JSON parsing and serialization
    - jsonschema - Schema validation
    - pathlib - Path handling
    - typing - Type hints
    - os - Environment variable access

References:
    - Related Files: app_framework.py, logging_manager.py
    - Design Docs: planning/phases/PHASE_02_CORE_ARCHITECTURE.md
    - Test File: tests/unit/test_config_manager.py

TODO/FIXME:
    - Add configuration file watching for live updates (Priority: Medium)
    - Add configuration backup mechanism (Priority: Low)

Line Count: 175/200 (Soft Limit: 180)
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Callable
import jsonschema

class ConfigManager:
    """Configuration management with validation and dot notation access."""
    
    def __init__(self, config_path: str) -> None:
        """Initialize configuration manager."""
        self._config_path = Path(config_path)
        self._config_data: Dict[str, Any] = {}
        self._schema: Dict[str, Any] = {}
        self._validators: Dict[str, Callable] = {}
        self._default_config = self._get_default_config()
        
        # Load configuration
        self.load_config()
    
    def load_config(self, schema_path: Optional[str] = None) -> None:
        """Load configuration with optional schema validation."""
        # Load schema if provided
        if schema_path:
            schema_path_obj = Path(schema_path)
            if schema_path_obj.exists():
                with open(schema_path_obj, 'r') as f:
                    self._schema = json.load(f)
        
        # Create config directory if it doesn't exist
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load configuration file or create with defaults
        if self._config_path.exists():
            try:
                with open(self._config_path, 'r') as f:
                    self._config_data = json.load(f)
                
                # Validate against schema if available
                if self._schema:
                    jsonschema.validate(self._config_data, self._schema)
                
            except (json.JSONDecodeError, jsonschema.ValidationError) as e:
                print(f"Configuration error: {e}")
                print("Using default configuration")
                self._config_data = self._default_config.copy()
                self.save()
        else:
            # Create default configuration file
            self._config_data = self._default_config.copy()
            self.save()
        
        # Apply environment variable overrides
        self._apply_env_overrides()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support."""
        keys = key.split('.')
        current = self._config_data
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value with dot notation support."""
        keys = key.split('.')
        current = self._config_data
        
        # Navigate to parent of target key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
        
        # Validate if schema is available
        if self._schema:
            try:
                jsonschema.validate(self._config_data, self._schema)
            except jsonschema.ValidationError as e:
                # Revert the change if validation fails
                del current[keys[-1]]
                raise ValueError(f"Configuration validation failed: {e}")
    
    def save(self) -> None:
        """Save current configuration to file."""
        with open(self._config_path, 'w') as f:
            json.dump(self._config_data, f, indent=2, default=str)
    
    def get_all(self) -> Dict[str, Any]:
        """Get complete configuration dictionary."""
        return self._config_data.copy()
    
    def has_key(self, key: str) -> bool:
        """Check if configuration key exists."""
        return self.get(key) is not None
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration structure."""
        return {
            "app": {
                "title": "CNG GNSS Interactive Demo",
                "version": "1.0.0",
                "log_level": "INFO",
                "performance_monitoring": True
            },
            "graphics": {
                "target_fps": 60,
                "vsync": True,
                "anti_aliasing": 4
            },
            "simulation": {
                "default_time_speed": 1.0,
                "time_step_ms": 16.67,
                "max_satellites": 100
            },
            "plugins": {
                "auto_reload": True,
                "watch_directories": ["src/plugins"],
                "load_on_startup": []
            },
            "logging": {
                "file_level": "INFO",
                "console_level": "INFO",
                "max_file_size": "10MB",
                "backup_count": 5
            }
        }
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # Check for environment variables with GNSS_ prefix
        for key, value in os.environ.items():
            if key.startswith('GNSS_'):
                # Convert GNSS_APP_LOG_LEVEL to app.log_level
                config_key = key[5:].lower().replace('_', '.')
                
                # Try to parse as JSON, fall back to string
                try:
                    parsed_value = json.loads(value)
                except json.JSONDecodeError:
                    parsed_value = value
                
                try:
                    self.set(config_key, parsed_value)
                except ValueError:
                    # Skip invalid overrides
                    pass