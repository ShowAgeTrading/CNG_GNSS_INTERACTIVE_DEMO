#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: globe.py
Purpose: Legacy globe wrapper - redirects to globe/globe_renderer.py
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - .globe.globe_renderer - New modular globe renderer

References:
    - Related Files: globe/globe_renderer.py, globe/texture_manager.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md

TODO/FIXME:
    - Remove this file once direct imports are updated (Priority: Low)

Line Count: 42/200 (Soft Limit: 180)
"""

import numpy as np
from typing import Optional, Tuple

# Import from new modular structure
from .globe.globe_renderer import GlobeRenderer
from .globe.coordinate_system import CoordinateSystem


class Globe:
    """3D Earth globe with textures and coordinate systems - LEGACY WRAPPER."""
    
    def __init__(self, radius: float = 6371.0) -> None:
        """Initialize globe with Earth radius in kilometers - DEPRECATED."""
        # This is now handled by GlobeRenderer
        self._radius = radius
    
    def load_textures(self, day_texture: str, night_texture: str) -> None:
        """Load day and night textures for the globe - DEPRECATED."""
        # This is now handled by TextureManager within GlobeRenderer
        pass
    
    def lat_lon_to_xyz(self, lat: float, lon: float) -> Tuple[float, float, float]:
        """Convert latitude/longitude to 3D cartesian coordinates."""
        # Delegate to CoordinateSystem
        vec3 = CoordinateSystem.lat_lon_to_cartesian(lat, lon)
        return (float(vec3.x), float(vec3.y), float(vec3.z))