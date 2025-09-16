#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: camera_controller.py
Purpose: Basic camera controls for 3D globe navigation
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - Camera and input handling

References:
    - Related Files: ../graphics_manager.py, ../globe/globe_renderer.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md

TODO/FIXME:
    - Implement orbit mode controls (Priority: High)
    - Add smooth camera movement (Priority: Medium)
    - Mouse input handling (Priority: High)

Line Count: 85/200 (Soft Limit: 180)
"""

import logging
from typing import Optional

from panda3d.core import Vec3, Camera
from direct.showbase.DirectObject import DirectObject

try:
    from ..utils.panda3d_utils import apply_transform
except ImportError:
    apply_transform = None

logger = logging.getLogger(__name__)


class CameraController(DirectObject):
    """
    Basic camera controls for 3D globe navigation.
    
    Initial implementation provides:
    - Fixed positioning around Earth
    - Basic zoom capabilities
    - Event-based control structure for future expansion
    """
    
    def __init__(self, panda_app) -> None:
        DirectObject.__init__(self)
        
        self._panda_app = panda_app
        self._camera = panda_app.camera
        self._initialized = False
        
        # Camera positioning
        self._distance = 15000.0  # km from Earth center
        self._azimuth = 0.0       # horizontal angle
        self._elevation = 0.0     # vertical angle
        
        logger.info("Camera controller initialized")
    
    def initialize(self) -> bool:
        """Initialize camera controller with default position."""
        try:
            # Set initial camera position (view Earth from space)
            if not self._update_camera_position():
                return False
            
            # Enable mouse controls (basic implementation)
            self._setup_basic_controls()
            
            self._initialized = True
            logger.info("Camera controller setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize camera controller: {e}")
            return False
    
    def _setup_basic_controls(self) -> None:
        """Setup basic keyboard controls."""
        # Accept input events
        self.accept('wheel_up', self._zoom_in)
        self.accept('wheel_down', self._zoom_out)
        
        # Basic keyboard controls for testing
        self.accept('arrow_left', self._rotate_left)
        self.accept('arrow_right', self._rotate_right)
        self.accept('arrow_up', self._rotate_up)
        self.accept('arrow_down', self._rotate_down)
    
    def _update_camera_position(self) -> bool:
        """Update camera position based on spherical coordinates."""
        import math
        
        try:
            # Convert spherical to cartesian coordinates
            x = self._distance * math.cos(math.radians(self._elevation)) * math.cos(math.radians(self._azimuth))
            y = self._distance * math.cos(math.radians(self._elevation)) * math.sin(math.radians(self._azimuth))
            z = self._distance * math.sin(math.radians(self._elevation))
            
            if apply_transform:
                success = apply_transform(self._camera, position=(x, y, z))
                if not success:
                    return False
            else:
                self._camera.setPos(x, y, z)
            
            self._camera.lookAt(0, 0, 0)
            return True
            
        except Exception as e:
            logger.error(f"Failed to update camera position: {e}")
            return False
    
    def _zoom_in(self) -> None:
        """Zoom camera closer to Earth."""
        self._distance = max(7000.0, self._distance * 0.9)
        self._update_camera_position()
    
    def _zoom_out(self) -> None:
        """Zoom camera away from Earth."""
        self._distance = min(50000.0, self._distance * 1.1)
        self._update_camera_position()
    
    def _rotate_left(self) -> None:
        """Rotate camera left around Earth."""
        self._azimuth -= 5.0
        self._update_camera_position()
    
    def _rotate_right(self) -> None:
        """Rotate camera right around Earth."""
        self._azimuth += 5.0
        self._update_camera_position()
    
    def _rotate_up(self) -> None:
        """Rotate camera up around Earth."""
        self._elevation = min(80.0, self._elevation + 5.0)
        self._update_camera_position()
    
    def _rotate_down(self) -> None:
        """Rotate camera down around Earth."""
        self._elevation = max(-80.0, self._elevation - 5.0)
        self._update_camera_position()


# Line count: 85/200