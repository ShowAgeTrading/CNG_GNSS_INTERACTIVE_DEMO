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
        self._assets_path = assets_path
        self._texture_cache: Dict[str, Texture] = {}
        self._loading_queue: List[str] = []
        
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
            texture_path = self._assets_path / "textures" / "earth" / relative_path
            
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
        """
        Load a single texture with optimizations for Intel Iris.
        Args:
            path: Full path to texture file
            name: Texture identifier for caching
            
        Returns:
            Loaded texture or None if failed
        """
        try:
            # Check cache first
            if name in self._texture_cache:
                logger.debug(f"Using cached texture: {name}")
                return self._texture_cache[name]
            
            # Check if file exists
            if not Path(path).exists():
                logger.error(f"Texture file not found: {path}")
                return None
            
            # Load texture through TexturePool for automatic management
            texture = TexturePool.loadTexture(path)
            
            if texture:
                # Configure texture settings for performance
                self._configure_texture(texture, name)
                
                # Cache the texture
                self._texture_cache[name] = texture
                
                return texture
            else:
                logger.error(f"Failed to load texture from {path}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading texture {name}: {e}")
            return None
    
    def _configure_texture(self, texture: Texture, name: str) -> None:
        """
        Configure texture settings for optimal performance on Intel Iris.
        
        Args:
            texture: The loaded texture to configure
            name: Texture identifier for specific settings
        """
        # Enable mipmapping for better performance at distance
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        
        # Configure anisotropic filtering (reduced for Intel Iris)
        texture.setAnisotropicDegree(4)  # Conservative setting
        
        # Set wrap modes
        texture.setWrapU(Texture.WMRepeat)
        texture.setWrapV(Texture.WMRepeat)
        
        # Generate mipmaps for performance
        texture.generateMipmaps()
        
        # Texture-specific optimizations
        if name == 'night':
            # Night textures can use slightly lower quality
            texture.setQualityLevel(Texture.QLNormal)
        elif name in ['bump', 'specular']:
            # Detail textures can be more compressed
            texture.setQualityLevel(Texture.QLFastest)
        else:
            # Day texture uses highest quality
            texture.setQualityLevel(Texture.QLBest)
    
    def get_texture(self, name: str) -> Optional[Texture]:
        """
        Get cached texture by name.
        Args:
            name: Texture identifier ('day', 'night', 'bump', 'specular')
            
        Returns:
            Cached texture or None if not found
        """
        return self._texture_cache.get(name)
    
    def preload_textures(self, texture_names: List[str]) -> None:
        """
        Preload specified textures (currently unused - for future async loading).
        
        Args:
            texture_names: List of texture names to preload
        """
        for name in texture_names:
            if name in self._earth_textures and name not in self._texture_cache:
                self._loading_queue.append(name)
    
    def get_texture_info(self, name: str) -> Dict[str, any]:
        """
        Get detailed information about a loaded texture.
        
        Args:
            name: Texture identifier
            
        Returns:
            Dictionary with texture details
        """
        texture = self.get_texture(name)
        
        if texture:
            return {
                'name': name,
                'width': texture.getXSize(),
                'height': texture.getYSize(),
                'format': texture.getFormat(),
                'has_mipmaps': texture.getNumMipmapPages() > 1,
                'memory_usage': texture.estimateTextureMemory()
            }
        else:
            return {'name': name, 'loaded': False}
    
    def get_total_memory_usage(self) -> int:
        """
        Calculate total memory usage of all loaded textures.
        
        Returns:
            Total memory usage in bytes
        """
        total_memory = 0
        
        for texture in self._texture_cache.values():
            if texture:
                total_memory += texture.estimateTextureMemory()
        
        return total_memory
    
    def cleanup(self) -> None:
        """Clean up texture resources."""
        logger.info("Cleaning up texture manager...")
        
        for name, texture in self._texture_cache.items():
            if texture:
                logger.debug(f"Releasing texture: {name}")
                # TexturePool handles cleanup automatically
        
        self._texture_cache.clear()
        self._loading_queue.clear()
        
        logger.info("Texture manager cleanup complete")