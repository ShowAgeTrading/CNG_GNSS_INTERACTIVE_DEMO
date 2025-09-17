"""
Globe rendering subsystem for the GNSS Interactive Demo.

This module provides Earth globe visualization with coordinate systems,
textures, materials, and model loading capabilities.
"""

# Core globe functionality
from .globe_renderer import GlobeRenderer
from .coordinate_system import CoordinateSystem
from .coordinate_validation import CoordinateValidator

# Asset management
from .model_loader import ModelLoader
from .texture_manager import TextureManager
from .material_manager import MaterialManager

# Setup orchestration
from .globe_setup import GlobeSetupOrchestrator

__all__ = [
    # Core components
    'GlobeRenderer',
    'CoordinateSystem', 
    'CoordinateValidator',
    
    # Asset management
    'ModelLoader',
    'TextureManager',
    'MaterialManager',
    
    # Setup
    'GlobeSetupOrchestrator',
]