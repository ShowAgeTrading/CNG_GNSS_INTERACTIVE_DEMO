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

# Import asset manager utilities
try:
    from ..utils.asset_manager import AssetManager
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
        self._initialized = False
        
        logger.info("Globe renderer initialized")
    
    def initialize(self) -> bool:
        """Initialize globe renderer with model and textures."""
        try:
            logger.info("Loading Earth globe...")
            
            # Initialize texture manager
            self._texture_manager = TextureManager(self._assets_path)
            
            # Load Earth model using model loader
            self._globe_model = self._model_loader.load_earth_model(self._render, self._globe_scale)
            if not self._globe_model:
                logger.error("Failed to load Earth model")
                return False
            
            # Load textures
            if not self._load_earth_textures():
                logger.error("Failed to load Earth textures")
                return False
            
            # Apply materials and textures using material manager
            if not self._setup_materials_and_textures():
                logger.error("Failed to setup Earth materials and textures")
                return False
            
            self._initialized = True
            logger.info("Globe renderer initialization complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize globe renderer: {e}")
            return False

    def _load_earth_textures(self) -> bool:
        """Load all Earth texture layers."""
        try:
            if not self._texture_manager:
                logger.error("Texture manager not initialized")
                return False
            
            # Load all texture layers
            self._earth_textures = self._texture_manager.load_earth_textures()
            
            # Check if critical textures loaded
            if not self._earth_textures.get('day'):
                logger.error("Failed to load day texture - critical for rendering")
                return False
            
            # Log texture loading results
            total_memory = self._texture_manager.get_total_memory_usage()
            logger.info(f"Loaded Earth textures, total memory: {total_memory/1024/1024:.1f} MB")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading Earth textures: {e}")
            return False
    
    def _setup_materials_and_textures(self) -> bool:
        """Setup materials and textures using MaterialManager."""
        try:
            if not self._globe_model:
                logger.error("Globe model not loaded")
                return False
            
            # Create and apply material
            earth_material = self._material_manager.create_earth_material()
            if not earth_material:
                return False
            
            if not self._material_manager.apply_material_to_globe(self._globe_model, earth_material):
                return False
            
            # Apply texture layers
            if not self._material_manager.apply_texture_layers(self._globe_model, self._earth_textures):
                return False
            
            # Configure rendering properties  
            self._material_manager.configure_rendering_properties(self._globe_model)
            
            logger.info("Materials and textures setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up materials and textures: {e}")
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
            self._globe_model.setScale(scale)
    
    def get_coordinate_system(self) -> CoordinateSystem:
        """Get coordinate system for positioning objects on globe."""
        return CoordinateSystem
    
    def get_globe_node(self) -> Optional[NodePath]:
        """Get the globe NodePath for external manipulation."""
        return self._globe_model
    
    def get_performance_info(self) -> Dict[str, any]:
        """Get performance information for monitoring."""
        info = {
            'initialized': self._initialized,
            'model_loaded': self._globe_model is not None,
            'textures_loaded': len([t for t in self._earth_textures.values() if t])
        }
        if self._texture_manager:
            info['texture_memory_mb'] = self._texture_manager.get_total_memory_usage() / (1024*1024)
        return info
    
    def cleanup(self) -> None:
        """Clean up globe renderer resources."""
        logger.info("Cleaning up globe renderer...")
        if self._globe_model:
            self._globe_model.removeNode()
            self._globe_model = None
        if self._texture_manager:
            self._texture_manager.cleanup()
            self._texture_manager = None
        self._earth_textures.clear()
        self._initialized = False
        logger.info("Globe renderer cleanup complete")


# Line count: 227/229