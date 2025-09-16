#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: reload_utils.py
Purpose: Utilities for hot-reload functionality
Author: GitHub Copilot
Created: 2025-09-15
"""

import os
import sys
import time
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ModuleInfo:
    """Information about a tracked module."""
    name: str
    path: str
    last_modified: float
    reload_count: int = 0
    state: Optional[Dict[str, Any]] = None
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class ModuleStateManager:
    """Manages state preservation for hot-reloaded modules."""
    
    def __init__(self):
        self._persistent_state: Dict[str, Any] = {}
        
    def preserve_state(self, module_name: str, state: Dict[str, Any]) -> None:
        """Store state before module reload."""
        self._persistent_state[module_name] = state.copy()
        
    def restore_state(self, module_name: str) -> Dict[str, Any]:
        """Restore state after module reload."""
        return self._persistent_state.get(module_name, {})
        
    def preserve_module_state(self, module_name: str, module: Any) -> None:
        """Preserve module state using __persistent_state__ marker."""
        try:
            if hasattr(module, '__persistent_state__'):
                state = {}
                for attr_name in module.__persistent_state__:
                    if hasattr(module, attr_name):
                        state[attr_name] = getattr(module, attr_name)
                        
                if state:
                    self.preserve_state(module_name, state)
                    
        except Exception as e:
            print(f"Error preserving state for {module_name}: {e}")
    
    def restore_module_state(self, module_name: str, module: Any) -> None:
        """Restore module state using __persistent_state__ marker."""
        try:
            state = self.restore_state(module_name)
            if state and hasattr(module, '__persistent_state__'):
                for attr_name, value in state.items():
                    if attr_name in module.__persistent_state__:
                        setattr(module, attr_name, value)
                        
        except Exception as e:
            print(f"Error restoring state for {module_name}: {e}")


class ModulePathResolver:
    """Resolves file paths to Python module names."""
    
    @staticmethod
    def path_to_module_name(file_path: str) -> Optional[str]:
        """Convert file path to Python module name."""
        try:
            # Normalize path
            path = Path(file_path).resolve()
            
            # Find the src directory
            parts = path.parts
            if 'src' not in parts:
                return None
                
            src_index = parts.index('src')
            module_parts = parts[src_index + 1:]
            
            # Remove .py extension
            if module_parts[-1].endswith('.py'):
                module_parts = module_parts[:-1] + (module_parts[-1][:-3],)
                
            # Convert to dot notation
            return '.'.join(module_parts)
            
        except Exception as e:
            print(f"Error converting path to module name: {e}")
            return None


class ReloadQueue:
    """Debounced queue for processing file reload requests."""
    
    def __init__(self, debounce_delay: float = 0.1):
        self._queue: List[str] = []
        self._lock = threading.Lock()
        self._debounce_delay = debounce_delay
        
    def queue_reload(self, file_path: str, callback: callable) -> None:
        """Queue a file for reload with debouncing."""
        with self._lock:
            if file_path not in self._queue:
                self._queue.append(file_path)
                
                def process_reload():
                    time.sleep(self._debounce_delay)
                    with self._lock:
                        if file_path in self._queue:
                            self._queue.remove(file_path)
                            callback(file_path)
                
                threading.Timer(self._debounce_delay, process_reload).start()