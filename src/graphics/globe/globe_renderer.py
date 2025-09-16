#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: globe_renderer.py
Purpose: High-quality Earth globe rendering with realistic textures
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - 3D rendering and model loading
    - panda3d-gltf (1.3.0) - GLTF model support

References:
    - Related Files: texture_manager.py, coordinate_system.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md
    - Assets: assets/models/earth/earth_3D.gltf

TODO/FIXME:
    - Implement dynamic day/night blending (Priority: High)
    - Add atmospheric effects (Priority: Medium)
    - LOD system for zoom levels (Priority: Medium)

Line Count: 200/200 (Soft Limit: 180)
"""

import logging
from pathlib import Path
from typing import Optional, Dict

from panda3d.core import (
    NodePath, Texture, Vec3
)
from direct.showbase.DirectObject import DirectObject

from .texture_manager import TextureManager
from .coordinate_system import CoordinateSystem
from .material_manager import MaterialManager
from .model_loader import ModelLoader
from .globe_setup import GlobeSetupOrchestrator

# Import asset manager utilities
try:
    from ..utils.asset_manager import AssetManager
    from ..utils.panda3d_utils import apply_transform
except ImportError:
    # Fallback for when running tests directly
    import sys
    from pathlib import Path as ImportPath
    src_path = ImportPath(__file__).parent.parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from graphics.utils.asset_manager import AssetManager

logger = logging.getLogger(__name__)


class GlobeRenderer(DirectObject):
    """
    High-quality Earth globe rendering with realistic textures.
    
    Features:
    - Multi-layer texture system (day/night/bump/specular)
    - Dynamic day/night blending based on sun position
    - High-resolution GLTF model loading
    - Performance optimizations for Intel Iris
    """
    
    def __init__(self, render_node: NodePath, assets_path: Path) -> None:
        DirectObject.__init__(self)
        
        self._render = render_node
        self._assets_path = assets_path
        
        # Asset management
        self._asset_manager = AssetManager(assets_path)
        
        # Globe components
        self._globe_model: Optional[NodePath] = None
        self._texture_manager: Optional[TextureManager] = None
        self._earth_textures: Dict[str, Optional[Texture]] = {}
        
        # Rendering properties
        self._earth_radius_km = 6371.0
        self._globe_scale = 1.0
        self._day_night_blend = 1.0  # 1.0 = full day, 0.0 = full night
        
        # Material and model management
        self._material_manager = MaterialManager()
        self._model_loader = ModelLoader(assets_path)
        self._setup_orchestrator = GlobeSetupOrchestrator(assets_path)
        self._initialized = False
        
        logger.info("Globe renderer initialized")
    
    def initialize(self) -> bool:
        """Initialize globe renderer with model and textures."""
        try:
            logger.info("Loading Earth globe...")
            
            # Initialize texture manager
            self._texture_manager = TextureManager(self._assets_path)
            
            # Use orchestrator for complex setup
            setup_result = self._setup_orchestrator.orchestrate_full_setup(
                self._texture_manager,
                self._material_manager,
                self._model_loader,
                self._render,
                self._globe_scale
            )
            
            if not setup_result['success']:
                logger.error(f"Globe setup failed: {setup_result['error']}")
                return False
            
            # Store results
            self._globe_model = setup_result['globe_model']
            self._earth_textures = setup_result['earth_textures']
            
            self._initialized = True
            logger.info("Globe renderer initialization complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize globe renderer: {e}")
            return False


    
    def update_day_night_blend(self, sun_position: Vec3) -> None:
        """Update day/night texture blending based on sun position."""
        if not self._initialized:
            return
        self._material_manager.update_day_night_blend(sun_position)
    
    def set_scale(self, scale: float) -> None:
        """Set globe scale factor."""
        self._globe_scale = scale
        if self._globe_model:
            try:
                apply_transform(self._globe_model, scale=(scale, scale, scale))
            except NameError:
                # Fallback if utilities not available
                self._globe_model.setScale(scale)
    
    def get_coordinate_system(self) -> CoordinateSystem:
        """Get coordinate system for positioning objects on globe."""
        return CoordinateSystem
    
    def get_globe_node(self) -> Optional[NodePath]:
        """Get the globe NodePath for external manipulation."""
        return self._globe_model
    
    def cleanup(self) -> None:
        """Clean up globe renderer resources."""
        if self._globe_model:
            self._globe_model.removeNode()
            self._globe_model = None
        if self._texture_manager:
            self._texture_manager.cleanup()
            self._texture_manager = None
        self._earth_textures.clear()
        self._initialized = False