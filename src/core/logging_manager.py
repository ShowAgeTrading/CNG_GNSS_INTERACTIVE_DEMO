#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: logging_manager.py
Purpose: Centralized logging system with UI integration and performance monitoring
Author: GitHub Copilot
Created: 2025-09-15
"""

import os
import logging
import logging.handlers
from typing import Dict, Any, Optional
from pathlib import Path

from .event_bus import EventBus
from .logging_utils import UILogHandler, PerformanceLogger, ErrorAggregator


class LoggingManager:
    """
    Centralized logging manager with:
    - Multiple output destinations (file, console, UI)
    - Performance monitoring integration
    - Error aggregation and reporting
    - Dynamic log level control
    """
    
    def __init__(self, event_bus: EventBus, logs_dir: str = "logs"):
        self._event_bus = event_bus
        self._logs_dir = Path(logs_dir)
        self._loggers: Dict[str, logging.Logger] = {}
        self._performance_logger: Optional[PerformanceLogger] = None
        self._error_aggregator = ErrorAggregator()
        self._ui_handler: Optional[UILogHandler] = None
        
        # Create logs directory
        self._logs_dir.mkdir(exist_ok=True)
        
        # Subscribe to events
        self._event_bus.subscribe('app.startup', self._on_app_startup)
        self._event_bus.subscribe('error.occurred', self._on_error_occurred)
        
    def setup_logging(self, level: str = "INFO", console_output: bool = True) -> None:
        """Configure logging system with specified settings."""
        # Convert level string to logging constant
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # Add file handler with rotation
        log_file = self._logs_dir / "app.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5  # 10MB files, 5 backups
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
        # Add console handler if requested
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(simple_formatter)
            root_logger.addHandler(console_handler)
            
        # Add UI handler for event bus integration
        self._ui_handler = UILogHandler(self._event_bus)
        self._ui_handler.setLevel(log_level)
        self._ui_handler.setFormatter(simple_formatter)
        root_logger.addHandler(self._ui_handler)
        
        # Create performance logger
        perf_logger = self.get_logger('performance')
        self._performance_logger = PerformanceLogger(perf_logger)
        
        print(f"Logging initialized - Level: {level}, Directory: {self._logs_dir}")
        
    def get_logger(self, name: str) -> logging.Logger:
        """Get or create logger for specific module."""
        if name not in self._loggers:
            logger = logging.getLogger(name)
            self._loggers[name] = logger
        return self._loggers[name]
        
    def log_performance(self, operation: str, duration: float) -> None:
        """Log performance metrics for operations."""
        if self._performance_logger:
            self._performance_logger.log_operation(operation, duration)
            
    def get_performance_stats(self, operation: str = None) -> Dict[str, Any]:
        """Get performance statistics."""
        if not self._performance_logger:
            return {}
            
        if operation:
            stats = self._performance_logger.get_stats(operation)
            return {operation: stats} if stats else {}
        else:
            # Get stats for all operations
            all_stats = {}
            for op in self._performance_logger._metrics.keys():
                stats = self._performance_logger.get_stats(op)
                if stats:
                    all_stats[op] = stats
            return all_stats
            
    def get_error_summary(self) -> Dict[str, Any]:
        """Get aggregated error information."""
        return self._error_aggregator.get_error_summary()
        
    def set_log_level(self, level: str) -> None:
        """Dynamically change log level."""
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        # Update all handlers
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        for handler in root_logger.handlers:
            handler.setLevel(log_level)
            
        print(f"Log level changed to: {level}")
        
    def _on_app_startup(self, event) -> None:
        """Handle application startup."""
        logger = self.get_logger('app')
        logger.info("Application starting up...")
        
    def _on_error_occurred(self, event) -> None:
        """Handle error events."""
        data = event.get('data', {})
        error_type = data.get('type', 'unknown')
        error_msg = data.get('error', 'No details provided')
        
        # Record in error aggregator
        self._error_aggregator.record_error(error_type, error_msg)
        
        # Log the error
        logger = self.get_logger('error')
        logger.error(f"Error occurred - Type: {error_type}, Details: {error_msg}")