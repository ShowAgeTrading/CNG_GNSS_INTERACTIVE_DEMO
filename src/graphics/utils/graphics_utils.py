"""
Graphics utilities for performance monitoring and logging.

This module contains utilities extracted from graphics_manager.py to reduce file size
and provide reusable performance monitoring across graphics components.
"""

import time
import logging
import gc
from typing import Optional, Dict, Any

# Optional imports
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Performance monitoring utilities for graphics operations."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self._frame_start_time: Optional[float] = None
        self._frame_times: list = []
        self._max_frame_history = 60  # Keep last 60 frames for averaging
        
        self._stats = {
            'frame_time': 0.0,
            'fps': 0.0,
            'memory_usage': 0.0,
            'texture_memory': 0.0,
            'gc_collections': 0
        }
    
    def start_frame(self) -> None:
        """Start frame timing."""
        self._frame_start_time = time.perf_counter()
    
    def end_frame(self) -> None:
        """End frame timing and update statistics."""
        if self._frame_start_time is None:
            return
            
        frame_time = time.perf_counter() - self._frame_start_time
        self._frame_times.append(frame_time)
        
        # Keep only recent frame times
        if len(self._frame_times) > self._max_frame_history:
            self._frame_times.pop(0)
        
        # Update statistics
        self._update_frame_stats()
        self._update_memory_stats()
        
        self._frame_start_time = None
    
    def _update_frame_stats(self) -> None:
        """Update frame timing statistics."""
        if not self._frame_times:
            return
            
        # Use recent average for smoother FPS
        recent_times = self._frame_times[-10:] if len(self._frame_times) >= 10 else self._frame_times
        avg_frame_time = sum(recent_times) / len(recent_times)
        
        self._stats['frame_time'] = avg_frame_time
        self._stats['fps'] = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    def _update_memory_stats(self) -> None:
        """Update memory usage statistics."""
        if not PSUTIL_AVAILABLE:
            return
            
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            self._stats['memory_usage'] = memory_info.rss / (1024 * 1024)  # MB
            
            # Count garbage collections
            self._stats['gc_collections'] = sum(gc.get_stats()[i]['collections'] 
                                               for i in range(len(gc.get_stats())))
        except Exception as e:
            logger.debug(f"Could not update memory stats: {e}")
    
    def update_performance_stats(self, delta_time: float) -> None:
        """Update performance statistics with delta time (legacy compatibility)."""
        self._stats['frame_time'] = delta_time
        self._stats['fps'] = 1.0 / delta_time if delta_time > 0 else 0.0
    
    def get_fps(self) -> float:
        """Get current FPS."""
        return self._stats['fps']
    
    def get_frame_time(self) -> float:
        """Get current frame time in seconds."""
        return self._stats['frame_time']
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            'usage_mb': self._stats['memory_usage'],
            'gc_collections': self._stats['gc_collections']
        }
    
    def get_all_stats(self) -> Dict[str, float]:
        """Get all performance statistics."""
        return self._stats.copy()
    
    def reset_stats(self) -> None:
        """Reset performance statistics."""
        self._frame_times.clear()
        self._stats = {
            'frame_time': 0.0,
            'fps': 0.0,
            'memory_usage': 0.0,
            'texture_memory': 0.0,
            'gc_collections': 0
        }