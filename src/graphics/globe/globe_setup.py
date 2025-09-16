#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: globe_setup.py
Purpose: Globe initialization orchestrator for complex setup sequences
Author: GitHub Copilot
Created: 2025-09-16
Version: 1.0.0

Line Count: Target <120 lines
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from panda3d.core import NodePath, Texture

logger = logging.getLogger(__name__)


class GlobeSetupOrchestrator:
    """Orchestrates the complex globe initialization sequence."""
    
    def __init__(self, assets_path: Path):
        self._assets_path = assets_path
        self._setup_steps = []
        self._rollback_actions = []
        
    def orchestrate_full_setup(self, 
                              texture_manager, 
                              material_manager,
                              model_loader,
                              render_node: NodePath,
                              globe_scale: float) -> Dict[str, any]:
        """
        Orchestrate the full globe setup sequence.
        
        Returns:
            Dictionary with setup results including model and textures
        """
        setup_result = {
            'globe_model': None,
            'earth_textures': {},
            'success': False,
            'error': None
        }
        
        try:
            # Step 1: Load Earth model
            globe_model = self._setup_earth_model(model_loader, render_node, globe_scale)
            if not globe_model:
                setup_result['error'] = "Failed to load Earth model"
                return setup_result
            setup_result['globe_model'] = globe_model
            
            # Step 2: Load textures
            earth_textures = self._setup_earth_textures(texture_manager)
            if not earth_textures:
                setup_result['error'] = "Failed to load Earth textures"
                return setup_result
            setup_result['earth_textures'] = earth_textures
            
            # Step 3: Setup materials and textures
            if not self._setup_materials_and_textures(material_manager, globe_model, earth_textures):
                setup_result['error'] = "Failed to setup materials and textures"
                return setup_result
            
            setup_result['success'] = True
            logger.info("Globe setup orchestration completed successfully")
            return setup_result
            
        except Exception as e:
            setup_result['error'] = f"Setup orchestration failed: {e}"
            logger.error(setup_result['error'])
            self._rollback_setup()
            return setup_result
    
    def _setup_earth_model(self, model_loader, render_node: NodePath, scale: float) -> Optional[NodePath]:
        """Load and configure Earth model."""
        globe_model = model_loader.load_earth_model(render_node, scale)
        if globe_model:
            self._rollback_actions.append(lambda: globe_model.removeNode())
        return globe_model
    
    def _setup_earth_textures(self, texture_manager) -> Optional[Dict[str, Texture]]:
        """Load all Earth texture layers."""
        earth_textures = texture_manager.load_earth_textures()
        if not earth_textures.get('day'):
            logger.error("Failed to load day texture - critical for rendering")
            return None
        
        total_memory = texture_manager.get_total_memory_usage()
        logger.info(f"Loaded Earth textures, total memory: {total_memory/1024/1024:.1f} MB")
        return earth_textures
    
    def _setup_materials_and_textures(self, material_manager, globe_model: NodePath, earth_textures: Dict) -> bool:
        """Setup materials and apply textures."""
        # Create and apply material
        earth_material = material_manager.create_earth_material()
        if not earth_material:
            return False
        
        if not material_manager.apply_material_to_globe(globe_model, earth_material):
            return False
        
        # Apply texture layers
        if not material_manager.apply_texture_layers(globe_model, earth_textures):
            return False
        
        # Configure rendering properties  
        material_manager.configure_rendering_properties(globe_model)
        return True
    
    def _rollback_setup(self) -> None:
        """Rollback setup actions in reverse order."""
        for action in reversed(self._rollback_actions):
            try:
                action()
            except Exception as e:
                logger.error(f"Rollback action failed: {e}")
        self._rollback_actions.clear()