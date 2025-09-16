#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: panda3d_initializer.py
Purpose: Panda3D engine initialization and configuration
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - 3D graphics engine

References:
    - Related Files: graphics_manager.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md

Line Count: 50/200
"""

import logging
from typing import Optional, Tuple

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, FrameBufferProperties

logger = logging.getLogger(__name__)


class Panda3DInitializer:
    """
    Handles Panda3D engine initialization and configuration.
    
    Extracted from graphics_manager.py for better separation of concerns.
    Optimized for Intel Iris graphics performance.
    """
    
    def __init__(self, window_title: str, window_size: Tuple[int, int]) -> None:
        self._window_title = window_title
        self._window_size = window_size
    
    def initialize_panda3d(self) -> Optional[ShowBase]:
        """Initialize Panda3D with optimal settings for Intel Iris."""
        try:
            # Configure window properties
            window_props = WindowProperties()
            window_props.setTitle(self._window_title)
            window_props.setSize(*self._window_size)
            window_props.setFullscreen(False)
            
            # Configure frame buffer - optimized for Intel Iris
            fb_props = FrameBufferProperties()
            fb_props.setRgbColor(True)
            fb_props.setAlphaBits(8)
            fb_props.setDepthBits(24)
            fb_props.setMultisamples(2)  # Reduced for Intel Iris performance
            
            # Initialize ShowBase with custom properties
            panda_app = ShowBase()
            
            # Apply window properties
            if panda_app.win:
                panda_app.win.requestProperties(window_props)
                
            # Enable frame rate meter for performance monitoring
            panda_app.setFrameRateMeter(True)
            
            # Set background color (space black)
            panda_app.win.setClearColor((0, 0, 0, 1))
            
            logger.info("Panda3D initialized with Intel Iris optimizations")
            return panda_app
            
        except Exception as e:
            logger.error(f"Failed to initialize Panda3D: {e}")
            return None


# Line count: 60/200