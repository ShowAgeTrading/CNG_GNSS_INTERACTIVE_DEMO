#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: app_framework.py
Purpose: Main application framework with component lifecycle management
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - typing - Type hints
    - abc - Abstract base class for component interface
    - time - Performance monitoring
    - threading - Thread safety

References:
    - Related Files: event_bus.py, simulation_clock.py, config_manager.py, app_utils.py
    - Design Docs: planning/phases/PHASE_02_CORE_ARCHITECTURE.md
    - Test File: tests/unit/test_app_framework.py

TODO/FIXME:
    - Add component dependency ordering (Priority: Medium)
    - Add graceful component failure recovery (Priority: Medium)

Line Count: 170/200 (Soft Limit: 180)
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, TYPE_CHECKING
import time
import threading
from .app_utils import PerformanceMonitor
from .component_interface import ComponentInterface

if TYPE_CHECKING:
    from .event_bus import EventBus
    from .simulation_clock import SimulationClock
    from .config_manager import ConfigManager

class Application:
    """Main application framework managing lifecycle and components."""
    
    def __init__(self, config_path: str = "config/app_config.json") -> None:
        """Initialize application framework."""
        # Import here to avoid circular imports
        from .event_bus import EventBus
        from .simulation_clock import SimulationClock
        from .config_manager import ConfigManager
        
        self.event_bus = EventBus()
        self.clock = SimulationClock(self.event_bus)
        self.config = ConfigManager(config_path)
        
        self._components: Dict[str, ComponentInterface] = {}
        self._shutdown_requested = False
        self._running = False
        self._last_frame_time = time.perf_counter()
        self._target_fps = self.config.get("graphics.target_fps", 60)
        self._frame_time = 1.0 / self._target_fps
        
        # Performance monitoring
        self._perf_monitor = PerformanceMonitor()
        
        # Thread safety
        self._lock = threading.RLock()
    
    def register_component(self, name: str, component: ComponentInterface) -> None:
        """Register component for lifecycle management."""
        with self._lock:
            if name in self._components:
                raise ValueError(f"Component '{name}' is already registered")
            
            self._components[name] = component
    
    def unregister_component(self, name: str) -> bool:
        """Unregister component by name."""
        with self._lock:
            if name in self._components:
                component = self._components[name]
                try:
                    component.shutdown()
                except Exception as e:
                    print(f"Error shutting down component '{name}': {e}")
                
                del self._components[name]
                return True
            return False
    
    def get_component(self, name: str) -> Optional[ComponentInterface]:
        """Get component by name."""
        return self._components.get(name)
    
    def startup(self) -> bool:
        """Initialize all components and prepare for main loop."""
        try:
            # Publish startup event
            self.event_bus.publish("app.startup", {
                "components": list(self._components.keys())
            }, "Application")
            
            # Initialize components
            failed_components = []
            for name, component in self._components.items():
                try:
                    if not component.initialize(self):
                        failed_components.append(name)
                        print(f"Component '{name}' failed to initialize")
                except Exception as e:
                    failed_components.append(name)
                    print(f"Error initializing component '{name}': {e}")
            
            # Remove failed components
            for name in failed_components:
                self.unregister_component(name)
            
            return len(failed_components) == 0
            
        except Exception as e:
            print(f"Startup failed: {e}")
            return False
    
    def run(self) -> None:
        """Main application loop."""
        if self._running:
            return
        
        self._running = True
        self._last_frame_time = time.perf_counter()
        
        try:
            while self._running and not self._shutdown_requested:
                current_time = time.perf_counter()
                delta_time = current_time - self._last_frame_time
                
                # Update components
                self._update_components(delta_time)
                
                # Update performance stats
                self._perf_monitor.update_stats()
                
                # Frame rate limiting
                elapsed = time.perf_counter() - current_time
                sleep_time = max(0, self._frame_time - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
                self._last_frame_time = time.perf_counter()
        
        except KeyboardInterrupt:
            print("Application interrupted by user")
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            self._running = False
    
    def shutdown(self) -> None:
        """Graceful shutdown of all components."""
        self._shutdown_requested = True
        
        # Publish shutdown event
        self.event_bus.publish("app.shutdown", {
            "reason": "requested"
        }, "Application")
        
        # Shutdown components in reverse order
        component_names = list(self._components.keys())
        for name in reversed(component_names):
            self.unregister_component(name)
        
        # Stop clock
        if self.clock.is_playing:
            self.clock.pause()
        
        self._running = False
    
    def is_running(self) -> bool:
        """Check if application is currently running."""
        return self._running
    
    def request_shutdown(self) -> None:
        """Request application shutdown."""
        self._shutdown_requested = True
    
    def get_fps(self) -> float:
        """Get current frames per second."""
        return self._perf_monitor.get_fps()
    
    def get_frame_count(self) -> int:
        """Get total frame count."""
        return self._perf_monitor.get_frame_count()
    
    def _update_components(self, delta_time: float) -> None:
        """Update all registered components."""
        failed_components = []
        
        for name, component in self._components.items():
            try:
                component.update(delta_time)
            except Exception as e:
                print(f"Error updating component '{name}': {e}")
                failed_components.append(name)
        
        # Remove failed components
        for name in failed_components:
            self.unregister_component(name)