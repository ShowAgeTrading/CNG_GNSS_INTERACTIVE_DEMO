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

from .graphics_manager import GraphicsManager

__version__ = "1.0.0"
__all__ = ["GraphicsManager"]