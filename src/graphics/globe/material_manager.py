#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: material_manager.py
Purpose: Earth globe material and texture layer management
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - Material and texture stage management

References:
    - Related Files: globe_renderer.py, texture_manager.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md

TODO/FIXME:
    - Implement dynamic day/night blending shader (Priority: High)
    - Add atmospheric scattering materials (Priority: Medium)

Line Count: 80/200 (Target: Under 90 for extraction)
"""

import logging
from typing import Optional, Dict

from panda3d.core import (
    NodePath, Material, TextureStage, Texture,
    ShadeModelAttrib, Vec3
)

logger = logging.getLogger(__name__)


class MaterialManager:
    """
    Manages materials and texture layers for Earth globe rendering.
    
    Extracted from globe_renderer.py to maintain file size compliance.
    Handles material creation, texture layer application, and rendering configuration.
    """
    
    def __init__(self) -> None:
        self._earth_material: Optional[Material] = None
        self._day_night_blend: float = 0.5
    
    def create_earth_material(self) -> Optional[Material]:
        """Create and configure Earth surface material."""
        try:
            # Create material for Earth surface
            material = Material("earth_material")
            
            # Configure material properties for realistic appearance
            material.setAmbient((0.2, 0.2, 0.2, 1.0))
            material.setDiffuse((1.0, 1.0, 1.0, 1.0))
            material.setSpecular((0.1, 0.1, 0.1, 1.0))
            material.setShininess(2.0)
            
            self._earth_material = material
            logger.info("Earth material created successfully")
            return material
            
        except Exception as e:
            logger.error(f"Error creating Earth material: {e}")
            return None
    
    def apply_material_to_globe(self, globe_model: NodePath, material: Material) -> bool:
        """Apply material to globe model."""
        try:
            if not globe_model or not material:
                logger.error("Invalid globe model or material")
                return False
            
            globe_model.setMaterial(material)
            logger.info("Material applied to globe successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error applying material to globe: {e}")
            return False
    
    def apply_texture_layers(self, globe_model: NodePath, textures: Dict[str, Texture]) -> bool:
        """Apply multi-layer texture system to globe."""
        try:
            if not globe_model:
                logger.error("Globe model not available")
                return False
            
            # Base day texture
            if textures.get('day'):
                day_stage = TextureStage('day')
                day_stage.setMode(TextureStage.MModulate)
                globe_model.setTexture(day_stage, textures['day'])
                
            # Night lights (will be blended dynamically)
            if textures.get('night'):
                night_stage = TextureStage('night')
                night_stage.setMode(TextureStage.MAdd)
                night_stage.setCombineRgb(TextureStage.CMInterpolate,
                                        TextureStage.CSTexture,
                                        TextureStage.CSPrevious,
                                        TextureStage.CSConstant)
                globe_model.setTexture(night_stage, textures['night'])
                
            # Bump mapping for surface relief
            if textures.get('bump'):
                bump_stage = TextureStage('bump')
                bump_stage.setMode(TextureStage.MNormal)
                globe_model.setTexture(bump_stage, textures['bump'])
                
            # Specular mapping for water reflections
            if textures.get('specular'):
                spec_stage = TextureStage('specular')
                spec_stage.setMode(TextureStage.MGloss)
                globe_model.setTexture(spec_stage, textures['specular'])
            
            logger.info("Texture layers applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error applying texture layers: {e}")
            return False
    
    def configure_rendering_properties(self, globe_model: NodePath) -> None:
        """Configure rendering properties for optimal appearance."""
        try:
            if not globe_model:
                return
                
            # Enable smooth shading
            globe_model.setRenderModeWireframe()
            globe_model.clearRenderMode()
            globe_model.setShadeModel(ShadeModelAttrib.MSmooth)
            
            # Enable depth testing
            globe_model.setDepthTest(True)
            globe_model.setDepthWrite(True)
            
            # Configure backface culling
            globe_model.setTwoSided(False)
            
            logger.info("Rendering properties configured")
            
        except Exception as e:
            logger.error(f"Error configuring rendering properties: {e}")
    
    def update_day_night_blend(self, sun_position: Vec3) -> None:
        """Update day/night texture blending based on sun position."""
        # Calculate blend factor based on sun angle
        # This is a simplified version - full implementation would consider
        # each point on Earth's surface relative to sun position
        
        # For now, use a simple global day/night cycle
        # In a real implementation, this would be per-pixel in a shader
        
        # Update blend factor (placeholder for future shader implementation)
        # self._day_night_blend = calculate_blend_factor(sun_position)
        pass


# Line count: 129/200