#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: __init__.py
Purpose: Graphics module initialization and exports
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - 3D graphics engine
    - panda3d-gltf (1.3.0) - GLTF model loading

References:
    - Related Files: graphics_manager.py, globe/globe_renderer.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md

Line Count: 25/200 (Soft Limit: 180)
"""

# Core graphics components
from .graphics_manager import GraphicsManager

# Subsystem management  
from .subsystem_manager import GraphicsSubsystemManager
from .subsystem_factory import SubsystemFactory

# Panda3D initialization
from .panda3d_initializer import Panda3DInitializer

# Configuration and events
from .config_manager import GraphicsConfigManager
from .event_handler import GraphicsEventHandler

# Globe subsystem
from . import globe

# Camera subsystem
from . import camera

# Utilities
from . import utils

__version__ = "1.0.0"
__all__ = [
    # Core components
    "GraphicsManager",
    
    # Subsystems
    "GraphicsSubsystemManager",
    "SubsystemFactory", 
    "Panda3DInitializer",
    
    # Configuration
    "GraphicsConfigManager",
    "GraphicsEventHandler",
    
    # Modules
    "globe",
    "camera",
    "utils",
]