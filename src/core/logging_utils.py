#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: logging_utils.py
Purpose: Utilities for logging system
Author: GitHub Copilot
Created: 2025-09-15
"""

import logging
import threading
from typing import Dict, Any, Optional, List
from datetime import datetime

from .event_bus import EventBus


class UILogHandler(logging.Handler):
    """Custom log handler that publishes to event bus for UI display."""
    
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        
    def emit(self, record):
        """Emit log record to event bus."""
        try:
            msg = self.format(record)
            self.event_bus.publish('log.entry', {
                'level': record.levelname,
                'message': msg,
                'timestamp': datetime.fromtimestamp(record.created),
                'module': record.name
            })
        except Exception:
            self.handleError(record)


class PerformanceLogger:
    """Tracks and logs performance metrics."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._metrics: Dict[str, List[float]] = {}
        self._lock = threading.Lock()
        
    def log_operation(self, operation: str, duration: float) -> None:
        """Log performance metric for an operation."""
        with self._lock:
            if operation not in self._metrics:
                self._metrics[operation] = []
            self._metrics[operation].append(duration)
            
            # Keep only recent metrics (last 100)
            if len(self._metrics[operation]) > 100:
                self._metrics[operation] = self._metrics[operation][-100:]
        
        # Log if duration is concerning
        if duration > 0.1:  # 100ms threshold
            self.logger.warning(f"Slow operation: {operation} took {duration:.3f}s")
            
    def get_stats(self, operation: str) -> Optional[Dict[str, float]]:
        """Get performance statistics for an operation."""
        with self._lock:
            if operation not in self._metrics or not self._metrics[operation]:
                return None
                
            durations = self._metrics[operation]
            return {
                'count': len(durations),
                'avg': sum(durations) / len(durations),
                'min': min(durations),
                'max': max(durations),
                'recent': durations[-1] if durations else 0
            }


class ErrorAggregator:
    """Aggregates and tracks error patterns."""
    
    def __init__(self):
        self._error_counts: Dict[str, int] = {}
        self._error_details: Dict[str, List[Dict[str, Any]]] = {}
        self._lock = threading.Lock()
        
    def record_error(self, error_type: str, details: str) -> None:
        """Record an error occurrence."""
        with self._lock:
            self._error_counts[error_type] = self._error_counts.get(error_type, 0) + 1
            
            if error_type not in self._error_details:
                self._error_details[error_type] = []
            self._error_details[error_type].append({
                'timestamp': datetime.now(),
                'details': details
            })
            
            # Keep only recent errors (last 50 per type)
            if len(self._error_details[error_type]) > 50:
                self._error_details[error_type] = self._error_details[error_type][-50:]
                
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors."""
        with self._lock:
            return {
                'total_errors': sum(self._error_counts.values()),
                'error_types': dict(self._error_counts),
                'recent_errors': {
                    error_type: details[-5:] if len(details) >= 5 else details
                    for error_type, details in self._error_details.items()
                }
            }