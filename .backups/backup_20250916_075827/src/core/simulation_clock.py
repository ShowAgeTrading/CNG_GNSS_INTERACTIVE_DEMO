#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: simulation_clock.py
Purpose: Precise simulation time control with variable speed and event publishing
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - datetime - Time handling and calculations
    - threading - Timer functionality and thread safety
    - time - Performance timing
    - typing - Type hints

References:
    - Related Files: event_bus.py, app_framework.py
    - Design Docs: planning/phases/PHASE_02_CORE_ARCHITECTURE.md
    - Test File: tests/unit/test_simulation_clock.py

TODO/FIXME:
    - Add session save/load for time persistence (Priority: Medium)

Line Count: 170/200 (Soft Limit: 180)
"""

from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING
import threading
import time

if TYPE_CHECKING:
    from .event_bus import EventBus

class SimulationClock:
    """Manages simulation time with precise control and synchronization."""
    
    def __init__(self, event_bus: 'EventBus', start_time: Optional[datetime] = None) -> None:
        """Initialize simulation clock with event bus integration."""
        self._event_bus = event_bus
        self._current_time = start_time or datetime.utcnow()
        self._real_start_time = time.perf_counter()
        
        self._is_playing = False
        self._speed_multiplier = 1.0
        self._step_size = timedelta(seconds=1)
        self._last_update_time = time.perf_counter()
        
        # Thread safety
        self._lock = threading.RLock()
        self._update_timer: Optional[threading.Timer] = None
        self._update_interval = 1.0 / 60  # 60 FPS
    
    @property
    def current_time(self) -> datetime:
        """Get current simulation time."""
        with self._lock:
            if self._is_playing:
                self._update_time_internal()
            return self._current_time
    
    @property
    def is_playing(self) -> bool:
        """Check if time simulation is running."""
        return self._is_playing
    
    @property
    def speed_multiplier(self) -> float:
        """Get current playback speed."""
        return self._speed_multiplier
    
    def play(self) -> None:
        """Start time simulation."""
        with self._lock:
            if not self._is_playing:
                self._is_playing = True
                self._last_update_time = time.perf_counter()
                self._start_update_loop()
                self._publish_event("time.play")
    
    def pause(self) -> None:
        """Pause time simulation."""
        with self._lock:
            if self._is_playing:
                self._is_playing = False
                self._stop_update_loop()
                self._publish_event("time.pause")
    
    def step_forward(self, steps: int = 1) -> None:
        """Advance time by specified steps."""
        with self._lock:
            delta = self._step_size * steps
            self._current_time += delta
            self._publish_event("time.step")
            self._publish_time_changed()
    
    def step_backward(self, steps: int = 1) -> None:
        """Reverse time by specified steps."""
        with self._lock:
            delta = self._step_size * steps
            self._current_time -= delta
            self._publish_event("time.step")
            self._publish_time_changed()
    
    def set_speed(self, multiplier: float) -> None:
        """Set playback speed (0.1x to 100x)."""
        if not (0.1 <= multiplier <= 100.0):
            raise ValueError("Speed multiplier must be between 0.1 and 100.0")
        
        with self._lock:
            self._speed_multiplier = multiplier
            if self._is_playing:
                self._last_update_time = time.perf_counter()
            self._publish_event("time.speed_changed")
    
    def set_time(self, new_time: datetime) -> None:
        """Jump to specific time."""
        with self._lock:
            self._current_time = new_time
            if self._is_playing:
                self._last_update_time = time.perf_counter()
            self._publish_event("time.jump")
            self._publish_time_changed()
    
    def set_step_size(self, step_size: timedelta) -> None:
        """Set the size of manual time steps."""
        with self._lock:
            self._step_size = step_size
    
    def get_elapsed_real_time(self) -> float:
        """Get elapsed real-world time since clock creation."""
        return time.perf_counter() - self._real_start_time
    
    def _update_time_internal(self) -> None:
        """Internal time update method (called within lock)."""
        if not self._is_playing:
            return
        
        current_real_time = time.perf_counter()
        real_delta = current_real_time - self._last_update_time
        self._last_update_time = current_real_time
        
        # Apply speed multiplier to real time delta
        simulation_delta = timedelta(seconds=real_delta * self._speed_multiplier)
        self._current_time += simulation_delta
        
        # Publish time changed event
        self._publish_time_changed()
    
    def _publish_time_changed(self) -> None:
        """Publish time changed event."""
        self._event_bus.publish("time.changed", {
            "time": self._current_time,
            "speed": self._speed_multiplier,
            "is_playing": self._is_playing
        }, "SimulationClock")
    
    def _publish_event(self, event_type: str) -> None:
        """Publish time-related event."""
        self._event_bus.publish(event_type, {
            "time": self._current_time,
            "speed": self._speed_multiplier
        }, "SimulationClock")
    
    def _start_update_loop(self) -> None:
        """Start the time update loop."""
        if self._update_timer is not None:
            self._update_timer.cancel()
        
        def update_loop():
            with self._lock:
                if self._is_playing:
                    self._update_time_internal()
                    self._update_timer = threading.Timer(self._update_interval, update_loop)
                    self._update_timer.start()
        
        update_loop()
    
    def _stop_update_loop(self) -> None:
        """Stop the time update loop."""
        if self._update_timer is not None:
            self._update_timer.cancel()
            self._update_timer = None