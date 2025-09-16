#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: graphics_manager.py
Purpose: Main graphics system coordinator integrating with core framework
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - 3D graphics engine
    - panda3d-gltf (1.3.0) - GLTF model loading support

References:
    - Related Files: core/component_interface.py, globe/globe_renderer.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md
    - Assets: assets/models/earth/earth_3D.gltf

TODO/FIXME:
    - Add viewport manager support (Priority: Medium)
    - Performance optimization for Intel Iris (Priority: High)
"""

import sys
import logging
from typing import Optional, Dict, Any
from pathlib import Path

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import (
    WindowProperties, FrameBufferProperties,
    PythonTask
)

try:
    from ..core.component_interface import ComponentInterface
    from ..core.event_bus import Event
except ImportError:
    # Fallback for when running tests directly
    import sys
    from pathlib import Path
    src_path = Path(__file__).parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from core.component_interface import ComponentInterface
    from core.event_bus import Event
from .subsystem_factory import SubsystemFactory
from .panda3d_initializer import Panda3DInitializer
from .utils.graphics_utils import PerformanceMonitor

logger = logging.getLogger(__name__)


class GraphicsManager(ComponentInterface, DirectObject):
    """
    Main graphics system coordinator integrating with core framework.
    
    Responsibilities:
    - Panda3D engine initialization and configuration  
    - Component lifecycle management for graphics subsystems
    - Event handling for graphics-related events
    """
    
    def __init__(self) -> None:
        ComponentInterface.__init__(self)
        DirectObject.__init__(self)
        
        # Core Panda3D components
        self._panda_app: Optional[ShowBase] = None
        self._render_task: Optional[PythonTask] = None
        
        # Performance monitoring
        self._performance_monitor = PerformanceMonitor()
        
        # Graphics subsystem components
        self._globe_renderer = None
        self._camera_controller = None
        self._viewport_manager = None
        self._material_manager = None
        self._lighting_system = None
        
        # Factory for creating subsystems
        self._subsystem_factory = None
        self._panda_initializer = None
        
        # Configuration
        self._window_title = "CNG GNSS Interactive Demo"
        self._window_size = (1920, 1080)
        self._target_fps = 60.0
        self._initialized = False
    
    @property
    def name(self) -> str:
        """Component name for identification."""
        return "GraphicsManager"
    
    def initialize(self, app) -> bool:
        """Initialize Panda3D and all graphics subsystems."""
        try:
            logger.info("Initializing graphics manager...")
            
            # Initialize Panda3D engine using initializer
            self._panda_initializer = Panda3DInitializer(self._window_title, self._window_size)
            self._panda_app = self._panda_initializer.initialize_panda3d()
            if not self._panda_app:
                logger.error("Failed to initialize Panda3D")
                return False
            
            # Initialize subsystem factory
            assets_path = app.config.get('assets_path', Path.cwd() / 'assets')
            self._subsystem_factory = SubsystemFactory(assets_path, self._panda_app)
            
            # Initialize graphics subsystems using factory
            if not self._initialize_graphics_subsystems():
                logger.error("Failed to initialize graphics subsystems")
                return False
            
            # Subscribe to core events
            self._subscribe_to_events(app)
            
            # Set up render loop task
            self._setup_render_task()
            
            self._initialized = True
            logger.info("Graphics manager initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize graphics manager: {e}")
            return False

    def _initialize_graphics_subsystems(self) -> bool:
        """Initialize all graphics subsystems using factory."""
        try:
            # Initialize globe renderer
            self._globe_renderer = self._subsystem_factory.create_globe_renderer()
            if not self._globe_renderer:
                logger.error("Failed to create globe renderer")
                return False
                
            # Initialize camera controller  
            self._camera_controller = self._subsystem_factory.create_camera_controller()
            if not self._camera_controller:
                logger.error("Failed to create camera controller")
                return False
                
            logger.info("Graphics subsystems initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing graphics subsystems: {e}")
            return False

    def _subscribe_to_events(self, app) -> None:
        """Subscribe to relevant events from the event bus."""
        if hasattr(app, 'event_bus'):
            app.event_bus.subscribe("time.changed", self.handle_event)
            app.event_bus.subscribe("config.graphics.*", self.handle_event)
            app.event_bus.subscribe("user.input.*", self.handle_event)
    
    def _setup_render_task(self) -> None:
        """Set up the main render loop task."""
        if self._panda_app and self._panda_app.taskMgr:
            self._render_task = self._panda_app.taskMgr.add(self._render_frame_task, "graphics_render_task")
    
    def _render_frame_task(self, task) -> int:
        """Main render frame task - called every frame."""
        try:
            dt = task.time - task.last if hasattr(task, 'last') else 0.0
            self._performance_monitor.update_performance_stats(dt)
            task.last = task.time
            return task.cont
        except Exception as e:
            logger.error(f"Error in render task: {e}")
            return task.done
    
    def update(self, delta_time: float) -> None:
        """Update graphics system each frame."""
        if not self._initialized:
            return
    
    def handle_event(self, event: Event) -> None:
        """Process graphics-related events."""
        if not self._initialized:
            return
        
        # Parse event type (format: "category.action" or "category.action.detail")
        event_parts = event.event_type.split('.')
        if len(event_parts) < 2:
            return
            
        category = event_parts[0]
        action = event_parts[1]
        
        if category == "time":
            pass  # Handle time-based updates
        elif category == "config" and action == "graphics":
            self._handle_config_change(event.data)
        elif category == "user" and action == "input":
            pass  # Handle user input for camera
    
    def _handle_config_change(self, config_data: Dict[str, Any]) -> None:
        """Handle graphics configuration changes."""
        pass  # Implementation for dynamic config updates
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get current performance statistics."""
        return self._performance_monitor.get_all_stats()
    
    def shutdown(self) -> None:
        """Cleanup graphics resources."""
        if self._render_task and self._panda_app:
            self._panda_app.taskMgr.remove(self._render_task)
        if self._panda_app:
            self._panda_app.destroy()
            self._panda_app = None
        self._initialized = False