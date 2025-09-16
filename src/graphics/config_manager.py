#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: config_manager.py (Graphics)
Purpose: Graphics-specific configuration management and validation
Author: GitHub Copilot
Created: 2025-09-16
Version: 1.0.0

"""

from pathlib import Path
from typing import Tuple


class GraphicsConfigManager:
    """Manages graphics-specific configuration and initialization parameters."""
    
    def __init__(self):
        self._window_title = "CNG GNSS Interactive Demo"
        self._window_size = (1920, 1080)
        self._target_fps = 60.0
        self._vsync_enabled = True
        self._anti_aliasing = 4
        
    def get_window_config(self) -> Tuple[str, Tuple[int, int]]:
        """Get window configuration."""
        return self._window_title, self._window_size
    
    def get_performance_config(self) -> Tuple[float, bool, int]:
        """Get performance configuration."""
        return self._target_fps, self._vsync_enabled, self._anti_aliasing
    
    def set_window_title(self, title: str) -> None:
        """Set window title."""
        self._window_title = title
    
    def set_window_size(self, width: int, height: int) -> None:
        """Set window size."""
        self._window_size = (width, height)
    
    def set_target_fps(self, fps: float) -> None:
        """Set target FPS."""
        self._target_fps = max(30.0, min(144.0, fps))
    
    def enable_vsync(self, enabled: bool) -> None:
        """Enable/disable vsync."""
        self._vsync_enabled = enabled
    
    def set_anti_aliasing(self, samples: int) -> None:
        """Set anti-aliasing samples."""
        valid_samples = [0, 2, 4, 8, 16]
        self._anti_aliasing = samples if samples in valid_samples else 4
    
    def apply_config_from_app(self, app_config) -> None:
        """Apply configuration from main app config."""
        if hasattr(app_config, 'get'):
            self._target_fps = app_config.get('graphics.target_fps', self._target_fps)
            self._vsync_enabled = app_config.get('graphics.vsync', self._vsync_enabled)
            self._anti_aliasing = app_config.get('graphics.anti_aliasing', self._anti_aliasing)
            
            # Window configuration
            title = app_config.get('app.title', self._window_title)
            if title:
                self._window_title = title