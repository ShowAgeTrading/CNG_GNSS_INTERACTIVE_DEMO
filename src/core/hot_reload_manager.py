#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: hot_reload_manager.py
Purpose: Hot-reload system for modules and plugins with state preservation
Author: GitHub Copilot
Created: 2025-09-15
"""

import os
import sys
import time
import threading
import importlib
from typing import Dict, List, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from .event_bus import EventBus
from .reload_utils import ModuleInfo, ModuleStateManager, ModulePathResolver, ReloadQueue


class ReloadFileHandler(FileSystemEventHandler):
    """File system event handler for hot-reload monitoring."""
    
    def __init__(self, reload_manager: 'HotReloadManager'):
        self.reload_manager = reload_manager
        
    def on_modified(self, event):
        """Handle file modification events."""
        if isinstance(event, FileModifiedEvent) and event.src_path.endswith('.py'):
            self.reload_manager._queue_reload(event.src_path)


class HotReloadManager:
    """
    Hot-reload manager with:
    - File system watching
    - Module reloading with state preservation
    - Dependency tracking
    - Error recovery
    """
    
    def __init__(self, event_bus: Optional['EventBus'] = None):
        if event_bus is None:
            from .event_bus import EventBus
            event_bus = EventBus()
        
        self._event_bus = event_bus
        self._watchers: Dict[str, Any] = {}
        self._loaded_modules: Dict[str, ModuleInfo] = {}
        self._reload_lock = threading.Lock()
        self._enabled = True
        
        # Utility components
        self._state_manager = ModuleStateManager()
        self._path_resolver = ModulePathResolver()
        self._reload_queue = ReloadQueue()
        
        # Subscribe to app events
        self._event_bus.subscribe('app.shutdown', self._on_app_shutdown)
        
    def watch_directory(self, path: str, patterns: List[str] = None) -> None:
        """Watch directory for file changes."""
        if not os.path.exists(path):
            print(f"Warning: Path {path} does not exist, skipping watch")
            return
            
        if patterns is None:
            patterns = ['*.py']
            
        observer = Observer()
        handler = ReloadFileHandler(self)
        observer.schedule(handler, path, recursive=True)
        observer.start()
        
        self._watchers[path] = observer
        print(f"Watching {path} for changes (patterns: {patterns})")
        
    def stop_watching(self, path: str) -> None:
        """Stop watching a directory."""
        if path in self._watchers:
            self._watchers[path].stop()
            self._watchers[path].join()
            del self._watchers[path]
            print(f"Stopped watching {path}")
    
    def reload_module(self, module_path: str) -> bool:
        """Reload specific module with state preservation."""
        if not self._enabled:
            return False
            
        try:
            # Convert file path to module name
            module_name = self._path_resolver.path_to_module_name(module_path)
            if not module_name:
                return False
                
            # Check if module is already loaded
            if module_name not in sys.modules:
                print(f"Module {module_name} not loaded, skipping reload")
                return False
                
            # Get module reference
            module = sys.modules[module_name]
            
            # Preserve state if module supports it
            self._state_manager.preserve_module_state(module_name, module)
            
            # Perform reload
            print(f"Reloading module: {module_name}")
            importlib.reload(module)
            
            # Update tracking info
            module_info = self._loaded_modules.get(module_name, 
                ModuleInfo(module_name, module_path, time.time()))
            module_info.reload_count += 1
            module_info.last_modified = time.time()
            self._loaded_modules[module_name] = module_info
            
            # Restore state
            self._state_manager.restore_module_state(module_name, module)
            
            # Notify of successful reload
            self._event_bus.publish('plugin.reloaded', {
                'module': module_name,
                'path': module_path,
                'reload_count': module_info.reload_count
            })
            
            return True
            
        except Exception as e:
            print(f"Error reloading {module_path}: {e}")
            self._event_bus.publish('error.occurred', {
                'type': 'hot_reload_failed',
                'module': module_path,
                'error': str(e)
            })
            return False
    
    def preserve_state(self, module_name: str, state: Dict[str, Any]) -> None:
        """Store state before module reload."""
        self._state_manager.preserve_state(module_name, state)
        
    def restore_state(self, module_name: str) -> Dict[str, Any]:
        """Restore state after module reload."""
        return self._state_manager.restore_state(module_name)
        
    def enable_hot_reload(self, enabled: bool = True) -> None:
        """Enable or disable hot-reload functionality."""
        self._enabled = enabled
        status = "enabled" if enabled else "disabled"
        print(f"Hot-reload {status}")
        
        self._event_bus.publish('hot_reload.toggled', {
            'enabled': enabled
        })
    
    def get_module_info(self, module_name: str) -> Optional[ModuleInfo]:
        """Get information about a tracked module."""
        return self._loaded_modules.get(module_name)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get hot-reload statistics."""
        total_reloads = sum(info.reload_count for info in self._loaded_modules.values())
        
        return {
            'enabled': self._enabled,
            'watched_paths': list(self._watchers.keys()),
            'tracked_modules': len(self._loaded_modules),
            'total_reloads': total_reloads,
            'persistent_state_count': len(self._state_manager._persistent_state)
        }
    
    def _queue_reload(self, file_path: str) -> None:
        """Queue a file for reload (debounced)."""
        self._reload_queue.queue_reload(file_path, self.reload_module)
    
    def _on_app_shutdown(self, event) -> None:
        """Handle application shutdown."""
        print("Shutting down hot-reload manager...")
        
        # Stop all watchers
        for path in list(self._watchers.keys()):
            self.stop_watching(path)
            
        self._enabled = False
        
    def __del__(self):
        """Cleanup on destruction."""
        try:
            for observer in self._watchers.values():
                observer.stop()
                observer.join()
        except:
            pass