#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: subsystem_manager.py
Purpose: Manages graphics subsystem initialization and lifecycle
Author: GitHub Copilot
Created: 2025-09-16
Version: 1.0.0

Line Count: Target <100 lines
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class GraphicsSubsystemManager:
    """Manages graphics subsystem components and their lifecycle."""
    
    def __init__(self, subsystem_factory):
        self._factory = subsystem_factory
        
        # Graphics subsystem components
        self._globe_renderer = None
        self._camera_controller = None
        self._viewport_manager = None
        self._material_manager = None
        self._lighting_system = None
        
    def initialize_all_subsystems(self) -> bool:
        """Initialize all graphics subsystems using factory."""
        try:
            if not self._initialize_globe_renderer():
                return False
            if not self._initialize_camera_controller():
                return False
                
            logger.info("Graphics subsystems initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing graphics subsystems: {e}")
            return False
    
    def _initialize_globe_renderer(self) -> bool:
        """Initialize globe renderer subsystem."""
        self._globe_renderer = self._factory.create_globe_renderer()
        if not self._globe_renderer:
            logger.error("Failed to create globe renderer")
            return False
        return True
        
    def _initialize_camera_controller(self) -> bool:
        """Initialize camera controller subsystem."""
        self._camera_controller = self._factory.create_camera_controller()
        if not self._camera_controller:
            logger.error("Failed to create camera controller")
            return False
        return True
    
    def get_globe_renderer(self):
        """Get the globe renderer instance."""
        return self._globe_renderer
    
    def get_camera_controller(self):
        """Get the camera controller instance."""
        return self._camera_controller
    
    def shutdown_all(self) -> None:
        """Shutdown all subsystems."""
        if self._globe_renderer:
            self._globe_renderer.cleanup()
            self._globe_renderer = None
        if self._camera_controller:
            self._camera_controller.cleanup()
            self._camera_controller = None
        
        logger.info("All graphics subsystems shut down")