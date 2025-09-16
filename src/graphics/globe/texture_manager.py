#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: texture_manager.py
Purpose: Efficient texture loading and management for Earth globe
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - Texture loading and management
    - pathlib - Path handling
References:
    - Related Files: globe_renderer.py, ../graphics_manager.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md
    - Assets: assets/textures/earth/*/10k.jpg
TODO/FIXME:
    - Add async texture loading (Priority: Medium)
    - Implement texture compression (Priority: Low)
"""

import logging
from pathlib import Path
from typing import Dict, Optional, List

from panda3d.core import Texture, TexturePool, PNMImage
from direct.task import Task

# Import asset manager utilities
try:
    from ..utils.asset_manager import AssetManager
except ImportError:
    # Fallback for when running tests directly
    import sys
    from pathlib import Path
    src_path = Path(__file__).parent.parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from graphics.utils.asset_manager import AssetManager

logger = logging.getLogger(__name__)


class TextureManager:
    """
    Efficient texture loading and management for Earth globe.
    
    Manages 4 texture layers for realistic Earth rendering:
    - Day texture: Composite Earth surface colors
    - Night texture: City lights and illumination  
    - Bump map: Elevation data for surface relief
    - Specular map: Ocean reflectance and ice data
    """
    
    def __init__(self, assets_path: Path) -> None:
        # Initialize asset manager for all asset operations
        self._asset_manager = AssetManager(assets_path)
        
        # Earth texture paths (10K variants for high quality)
        self._earth_textures = {
            'day': 'composite_earth__skins/8081_earthmap10k.jpg',
            'night': 'night_lights_skin/8081_earthlights10k.jpg',
            'bump': 'landmass_elevations_skins/8081_earthbump10k.jpg',
            'specular': 'oceans_specularity_reflections_skin/8081_earthspec10k.jpg'
        }
        
        logger.info("Texture manager initialized")
    
    def load_earth_textures(self) -> Dict[str, Optional[Texture]]:
        """
        Load all Earth texture layers synchronously.
        Returns:
            Dict containing loaded textures or None for failed loads
        """
        textures = {}
        
        for texture_name, relative_path in self._earth_textures.items():
            texture_path = self._asset_manager.resolve_texture_path("earth", relative_path)
            
            logger.info(f"Loading {texture_name} texture from {texture_path}")
            texture = self._load_texture(str(texture_path), texture_name)
            
            if texture:
                textures[texture_name] = texture
                logger.info(f"Successfully loaded {texture_name} texture "
                          f"({texture.getXSize()}x{texture.getYSize()})")
            else:
                textures[texture_name] = None
                logger.error(f"Failed to load {texture_name} texture")
        
        return textures
    
    def _load_texture(self, path: str, name: str) -> Optional[Texture]:
        """Load a single texture using AssetManager for caching and validation."""
        try:
            # Use AssetManager for all caching operations
            if self._asset_manager.is_asset_cached(name):
                return self._asset_manager.get_cached_asset(name)
            
            # Validate asset exists using AssetManager
            if not self._asset_manager.validate_asset(Path(path)):
                return None
            
            # Load and configure texture
            texture = TexturePool.loadTexture(path)
            if texture:
                self._configure_texture(texture, name)
                self._asset_manager.cache_asset(name, texture)
                return texture
                
        except Exception as e:
            logger.error(f"Error loading texture {name}: {e}")
        return None
    
    def _configure_texture(self, texture: Texture, name: str) -> None:
        """Configure texture settings for optimal performance."""
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        texture.setAnisotropicDegree(4)
        texture.setWrapU(Texture.WMRepeat)
        texture.setWrapV(Texture.WMRepeat)
        texture.generateMipmaps()
        
        # Quality based on texture type
        quality_map = {
            'night': Texture.QLNormal,
            'bump': Texture.QLFastest,
            'specular': Texture.QLFastest
        }
        texture.setQualityLevel(quality_map.get(name, Texture.QLBest))
    
    def get_texture(self, name: str) -> Optional[Texture]:
        """Get cached texture by name."""
        return self._asset_manager.get_cached_asset(name)
    
    def get_texture_info(self, name: str) -> Dict[str, any]:
        """Get texture information."""
        texture = self.get_texture(name)
        if texture:
            return {
                'name': name,
                'width': texture.getXSize(), 
                'height': texture.getYSize(),
                'memory_usage': texture.estimateTextureMemory()
            }
        return {'name': name, 'loaded': False}
    
    def cleanup(self) -> None:
        """Clean up texture resources."""
        self._asset_manager.clear_cache()
        logger.info("Texture manager cleanup complete")