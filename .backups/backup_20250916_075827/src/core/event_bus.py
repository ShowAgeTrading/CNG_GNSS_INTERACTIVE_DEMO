#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: event_bus.py
Purpose: Thread-safe event communication system for modular architecture
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - typing - Type hints for better code clarity
    - threading - Thread-safe event handling
    - dataclasses - Event and subscription data structures
    - uuid - Unique subscription IDs
    - asyncio - Asynchronous event publishing
    - time - Performance monitoring

References:
    - Related Files: app_framework.py, simulation_clock.py
    - Design Docs: planning/phases/PHASE_02_CORE_ARCHITECTURE.md
    - Test File: tests/unit/test_event_bus.py

TODO/FIXME:
    - Add event history cleanup mechanism (Priority: Medium)
    - Consider event batching for high-frequency events (Priority: Low)

Line Count: 180/200 (Soft Limit: 180)
"""

from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import threading
import uuid
import asyncio
import time

@dataclass
class Event:
    """Event data structure."""
    event_type: str
    data: Any = None
    source: str = "unknown"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class EventSubscription:
    """Subscription metadata."""
    subscription_id: str
    event_type: str
    callback: Callable
    priority: int = 0
    filter_func: Optional[Callable] = None

class EventBus:
    """Thread-safe event bus for decoupled communication."""
    
    def __init__(self, max_history: int = 1000) -> None:
        """Initialize event bus with configurable history size."""
        self._subscribers: Dict[str, List[EventSubscription]] = {}
        self._lock = threading.RLock()
        self._event_history: List[Event] = []
        self._max_history = max_history
        self._performance_stats: Dict[str, float] = {}
        self._total_events_published = 0
    
    def subscribe(self, event_type: str, callback: Callable, 
                  priority: int = 0, filter_func: Optional[Callable] = None) -> str:
        """Subscribe to event type with priority and optional filtering."""
        subscription_id = str(uuid.uuid4())
        subscription = EventSubscription(
            subscription_id=subscription_id,
            event_type=event_type,
            callback=callback,
            priority=priority,
            filter_func=filter_func
        )
        
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            
            self._subscribers[event_type].append(subscription)
            # Sort by priority (higher numbers = higher priority)
            self._subscribers[event_type].sort(key=lambda s: s.priority, reverse=True)
        
        return subscription_id
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove subscription by ID."""
        with self._lock:
            for event_type, subscriptions in self._subscribers.items():
                for i, sub in enumerate(subscriptions):
                    if sub.subscription_id == subscription_id:
                        subscriptions.pop(i)
                        return True
        return False
    
    def publish(self, event_type: str, data: Any = None, 
                source: str = "unknown") -> None:
        """Publish event to all matching subscribers."""
        start_time = time.perf_counter()
        
        event = Event(
            event_type=event_type,
            data=data,
            source=source
        )
        
        # Store in history
        with self._lock:
            self._event_history.append(event)
            if len(self._event_history) > self._max_history:
                self._event_history.pop(0)
            
            subscribers = self._subscribers.get(event_type, []).copy()
        
        # Call subscribers (outside lock to avoid deadlocks)
        for subscription in subscribers:
            try:
                # Apply filter if present
                if subscription.filter_func is None or subscription.filter_func(event):
                    subscription.callback(event)
            except Exception as e:
                # Log error but don't crash
                print(f"Error in event callback: {e}")
        
        # Update performance stats
        duration = time.perf_counter() - start_time
        with self._lock:
            self._performance_stats[event_type] = duration
            self._total_events_published += 1
    
    def publish_async(self, event_type: str, data: Any = None, 
                     source: str = "unknown") -> None:
        """Publish event asynchronously for performance."""
        def async_publish():
            self.publish(event_type, data, source)
        
        # Run in thread to avoid blocking
        thread = threading.Thread(target=async_publish, daemon=True)
        thread.start()
    
    def get_history(self, event_type: Optional[str] = None, 
                   limit: int = 100) -> List[Event]:
        """Get event history with optional filtering."""
        with self._lock:
            if event_type is None:
                return self._event_history[-limit:]
            else:
                filtered = [e for e in self._event_history if e.event_type == event_type]
                return filtered[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        with self._lock:
            return {
                "total_events": self._total_events_published,
                "event_types": len(self._subscribers),
                "total_subscribers": sum(len(subs) for subs in self._subscribers.values()),
                "avg_processing_time": sum(self._performance_stats.values()) / max(len(self._performance_stats), 1),
                "performance_by_type": self._performance_stats.copy()
            }
    
    def clear_history(self) -> None:
        """Clear event history."""
        with self._lock:
            self._event_history.clear()