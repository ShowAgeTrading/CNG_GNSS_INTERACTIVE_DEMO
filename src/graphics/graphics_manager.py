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

try:
    from direct.showbase.ShowBase import ShowBase
    from direct.showbase.DirectObject import DirectObject
    from panda3d.core import (
        WindowProperties, FrameBufferProperties,
        PythonTask
    )
    PANDA3D_AVAILABLE = True
except ImportError:
    # Mock classes for when Panda3D is not available (testing)
    PANDA3D_AVAILABLE = False
    class ShowBase:
        def __init__(self):
            pass
    class DirectObject:
        def __init__(self):
            pass
    class WindowProperties:
        pass
    class FrameBufferProperties:
        pass
    class PythonTask:
        pass

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
from .event_handler import GraphicsEventHandler
from .subsystem_manager import GraphicsSubsystemManager
from .config_manager import GraphicsConfigManager

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
        
        # Core components
        self._performance_monitor = PerformanceMonitor()
        self._event_handler = GraphicsEventHandler()
        self._config_manager = GraphicsConfigManager()
        self._subsystem_manager = None
        
        # Panda3D components
        self._panda_initializer = None
        self._subsystem_factory = None
        self._initialized = False
    
    @property
    def name(self) -> str:
        """Component name for identification."""
        return "GraphicsManager"
    
    def initialize(self, app) -> bool:
        """Initialize Panda3D and all graphics subsystems."""
        try:
            logger.info("Initializing graphics manager...")
            
            if not self._initialize_panda3d():
                return False
            if not self._initialize_factory(app):
                return False
            if not self._initialize_graphics_subsystems():
                logger.error("Failed to initialize graphics subsystems")
                return False
            
            self._subscribe_to_events(app)
            self._setup_render_task()
            
            self._initialized = True
            logger.info("Graphics manager initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize graphics manager: {e}")
            return False

    def _initialize_panda3d(self) -> bool:
        """Initialize Panda3D engine."""
        window_title, window_size = self._config_manager.get_window_config()
        self._panda_initializer = Panda3DInitializer(window_title, window_size)
        self._panda_app = self._panda_initializer.initialize_panda3d()
        if not self._panda_app:
            logger.error("Failed to initialize Panda3D")
            return False
        return True

    def _initialize_factory(self, app) -> bool:
        """Initialize subsystem factory."""
        assets_path = app.config.get('assets_path', Path.cwd() / 'assets')
        self._subsystem_factory = SubsystemFactory(assets_path, self._panda_app)
        
        # Initialize subsystem manager
        self._subsystem_manager = GraphicsSubsystemManager(self._subsystem_factory)
        return True

    def _initialize_graphics_subsystems(self) -> bool:
        """Initialize all graphics subsystems using subsystem manager."""
        return self._subsystem_manager.initialize_all_subsystems()

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
        self._event_handler.handle_graphics_event(event)
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get current performance statistics."""
        return self._performance_monitor.get_all_stats()
    
    def get_globe_renderer(self):
        """Get globe renderer instance."""
        return self._subsystem_manager.get_globe_renderer() if self._subsystem_manager else None
    
    def get_camera_controller(self):
        """Get camera controller instance.""" 
        return self._subsystem_manager.get_camera_controller() if self._subsystem_manager else None
    
    def shutdown(self) -> None:
        """Cleanup graphics resources."""
        if self._subsystem_manager:
            self._subsystem_manager.shutdown_all()
        if self._render_task and self._panda_app:
            self._panda_app.taskMgr.remove(self._render_task)
        if self._panda_app:
            self._panda_app.destroy()
            self._panda_app = None
        self._initialized = False