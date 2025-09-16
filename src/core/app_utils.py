#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: app_utils.py
Purpose: Application framework utilities and helper functions
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - time - Performance monitoring
    - typing - Type hints

References:
    - Related Files: app_framework.py
    - Design Docs: planning/phases/PHASE_02_CORE_ARCHITECTURE.md

Line Count: 45/200 (Soft Limit: 180)
"""

import time
from typing import Tuple

class PerformanceMonitor:
    """Helper class for application performance monitoring."""
    
    def __init__(self) -> None:
        """Initialize performance monitor."""
        self._frame_count = 0
        self._fps_start_time = time.perf_counter()
        self._current_fps = 0.0
    
    def update_stats(self) -> None:
        """Update performance statistics."""
        self._frame_count += 1
        
        # Calculate FPS every second
        current_time = time.perf_counter()
        if current_time - self._fps_start_time >= 1.0:
            time_elapsed = current_time - self._fps_start_time
            self._current_fps = self._frame_count / time_elapsed
            self._frame_count = 0
            self._fps_start_time = current_time
    
    def get_fps(self) -> float:
        """Get current frames per second."""
        return self._current_fps
    
    def get_frame_count(self) -> int:
        """Get total frame count since last reset."""
        return self._frame_count
    
    def reset(self) -> None:
        """Reset performance counters."""
        self._frame_count = 0
        self._fps_start_time = time.perf_counter()
        self._current_fps = 0.0