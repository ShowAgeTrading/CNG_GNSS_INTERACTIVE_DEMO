#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: model_loader.py
Purpose: GLTF model loading and initialization for Earth globe
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - NodePath and model handling
    - panda3d-gltf (1.3.0) - GLTF model loading

References:
    - Related Files: globe_renderer.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md

TODO/FIXME:
    - Add LOD system for different zoom levels (Priority: Medium)
    - Implement model caching (Priority: Low)

Line Count: 60/200 (Target: Under 80 for extraction)
"""

import logging
from pathlib import Path
from typing import Optional

from panda3d.core import NodePath
from gltf import load_model
from ..utils.panda3d_utils import setup_node, apply_transform

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Handles GLTF model loading and initialization for Earth globe.
    
    Extracted from globe_renderer.py to maintain file size compliance.
    Manages model loading, validation, and initial setup.
    """
    
    def __init__(self, assets_path: Path) -> None:
        self._assets_path = assets_path
    
    def load_earth_model(self, render_node: NodePath, scale: float = 1.0) -> Optional[NodePath]:
        """Load Earth GLTF model and attach to render tree."""
        try:
            model_path = self._assets_path / "models" / "earth" / "earth_3D.gltf"
            
            if not model_path.exists():
                logger.error(f"Earth model not found: {model_path}")
                return None
            
            logger.info(f"Loading Earth model from {model_path}")
            
            # Load GLTF model
            globe_model = load_model(str(model_path))
            
            if not globe_model:
                logger.error("Failed to load GLTF model")
                return None
            
            # Parent and configure using utilities
            globe_model.reparentTo(render_node)
            apply_transform(globe_model, position=(0, 0, 0), scale=(scale, scale, scale))
            
            logger.info("Earth model loaded successfully")
            return globe_model
            
        except Exception as e:
            logger.error(f"Error loading Earth model: {e}")
            return None
    
    def validate_model(self, model: NodePath) -> bool:
        """Validate that model was loaded correctly."""
        if not model:
            return False
            
        # Basic validation - check if model has geometry
        try:
            # Check if model has children (geometry nodes)
            if model.getNumChildren() == 0:
                logger.warning("Model has no children - may be empty")
                return False
                
            logger.info(f"Model validation passed: {model.getNumChildren()} child nodes")
            return True
            
        except Exception as e:
            logger.error(f"Error validating model: {e}")
            return False


# Line count: 75/200