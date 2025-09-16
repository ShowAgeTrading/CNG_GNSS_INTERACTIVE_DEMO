#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: test_event_bus.py
Purpose: Comprehensive unit tests for EventBus component
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Tests:
    - Core EventBus functionality (subscribe/unsubscribe, publishing)
    - Thread safety and concurrent operations
    - Error handling and edge cases
    - Performance characteristics
    - Memory management
"""

import pytest
import threading
import time
from typing import List, Any
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.event_bus import EventBus, Event


class TestEventBusCore:
    """Test core EventBus functionality."""
    
    def setup_method(self):
        """Setup fresh EventBus for each test."""
        self.event_bus = EventBus()
        self.received_events = []
        self.callback_count = 0
        self.subscription_ids = []
    
    def simple_callback(self, event: Event):
        """Simple test callback."""
        self.received_events.append(event)
        self.callback_count += 1
    
    def test_subscribe_unsubscribe(self):
        """Test basic subscribe/unsubscribe operations."""
        # Subscribe
        sub_id = self.event_bus.subscribe('test_event', self.simple_callback)
        assert isinstance(sub_id, str)
        assert 'test_event' in self.event_bus._subscribers
        assert len(self.event_bus._subscribers['test_event']) == 1
        
        # Unsubscribe
        success = self.event_bus.unsubscribe(sub_id)
        assert success is True
        assert len(self.event_bus._subscribers.get('test_event', [])) == 0
    
    def test_event_publishing_basic(self):
        """Test basic event publishing."""
        sub_id = self.event_bus.subscribe('test_event', self.simple_callback)
        
        # Publish event
        self.event_bus.publish('test_event', {'message': 'hello'})
        
        # Verify callback was called
        assert self.callback_count == 1
        assert len(self.received_events) == 1
        assert self.received_events[0].event_type == 'test_event'
        assert self.received_events[0].data == {'message': 'hello'}
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id)
    
    def test_multiple_subscribers_same_event(self):
        """Test multiple subscribers to same event type."""
        callback2_count = 0
        received_events2 = []
        
        def callback2(event: Event):
            nonlocal callback2_count
            callback2_count += 1
            received_events2.append(event)
        
        # Subscribe both callbacks
        sub_id1 = self.event_bus.subscribe('test_event', self.simple_callback)
        sub_id2 = self.event_bus.subscribe('test_event', callback2)
        
        # Publish event
        self.event_bus.publish('test_event', {'data': 'test'})
        
        # Both callbacks should receive the event
        assert self.callback_count == 1
        assert callback2_count == 1
        assert len(self.received_events) == 1
        assert len(received_events2) == 1
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id1)
        self.event_bus.unsubscribe(sub_id2)
    
    def test_event_type_specificity(self):
        """Test that events are only delivered to specific subscribers."""
        sub_id1 = self.event_bus.subscribe('event1', self.simple_callback)
        
        callback2_count = 0
        def callback2(event: Event):
            nonlocal callback2_count
            callback2_count += 1
        
        sub_id2 = self.event_bus.subscribe('event2', callback2)
        
        # Publish to event1 only
        self.event_bus.publish('event1', {'data': 'first'})
        
        # Only callback1 should receive it
        assert self.callback_count == 1
        assert callback2_count == 0
        
        # Publish to event2 only
        self.event_bus.publish('event2', {'data': 'second'})
        
        # Now callback2 should receive it too
        assert self.callback_count == 1  # unchanged
        assert callback2_count == 1
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id1)
        self.event_bus.unsubscribe(sub_id2)
    
    def test_event_filtering(self):
        """Test event filtering doesn't affect unsubscribed events."""
        sub_id = self.event_bus.subscribe('target_event', self.simple_callback)
        
        # Publish target and non-target events
        self.event_bus.publish('target_event', {'data': 'should_receive'})
        self.event_bus.publish('other_event', {'data': 'should_not_receive'})
        
        # Only target event should be received
        assert self.callback_count == 1
        assert self.received_events[0].event_type == 'target_event'
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id)


class TestEventBusThreadSafety:
    """Test thread safety of EventBus."""
    
    def setup_method(self):
        """Setup fresh EventBus for each test."""
        self.event_bus = EventBus()
        self.results = []
        self.lock = threading.Lock()
    
    def thread_safe_callback(self, event: Event):
        """Thread-safe callback for testing."""
        with self.lock:
            self.results.append(event.data)
    
    def test_concurrent_subscribe_unsubscribe(self):
        """Test concurrent subscribe/unsubscribe operations."""
        subscription_ids = []
        threads = []
        
        def create_callback(i):
            def callback(event):
                with self.lock:
                    self.results.append(f"callback_{i}")
            return callback
        
        # Subscribe concurrently
        def subscribe_worker(i):
            callback = create_callback(i)
            sub_id = self.event_bus.subscribe('concurrent_test', callback)
            with self.lock:
                subscription_ids.append(sub_id)
        
        for i in range(10):
            thread = threading.Thread(target=subscribe_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all subscribes
        for thread in threads:
            thread.join()
        
        # Publish event - all callbacks should receive it
        self.event_bus.publish('concurrent_test', 'test_data')
        
        # Verify all callbacks were registered and called
        assert len(self.results) == 10
        
        # Cleanup
        for sub_id in subscription_ids:
            self.event_bus.unsubscribe(sub_id)
    
    def test_concurrent_publishing(self):
        """Test simultaneous event publishing from multiple threads."""
        sub_id = self.event_bus.subscribe('multi_thread_test', self.thread_safe_callback)
        
        threads = []
        
        def publish_worker(thread_id):
            for i in range(5):
                self.event_bus.publish('multi_thread_test', f"thread_{thread_id}_msg_{i}")
        
        # Start multiple publishing threads
        for i in range(4):
            thread = threading.Thread(target=publish_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Should have received all messages
        assert len(self.results) == 20  # 4 threads * 5 messages each
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id)
    
    def test_rlock_behavior(self):
        """Test RLock allows recursive locking."""
        lock_count = 0
        sub_id = None
        
        def recursive_callback(event: Event):
            nonlocal lock_count, sub_id
            lock_count += 1
            # This should not deadlock due to RLock
            if lock_count < 3:
                self.event_bus.publish('recursive_test', f"recursive_{lock_count}")
        
        sub_id = self.event_bus.subscribe('recursive_test', recursive_callback)
        self.event_bus.publish('recursive_test', 'initial')
        
        assert lock_count == 3
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id)


class TestEventBusErrorHandling:
    """Test error handling and edge cases."""
    
    def setup_method(self):
        """Setup fresh EventBus for each test."""
        self.event_bus = EventBus()
        self.successful_calls = 0
    
    def success_callback(self, event: Event):
        """Callback that always succeeds."""
        self.successful_calls += 1
    
    def test_callback_exception_isolation(self):
        """Test that callback exceptions don't crash other subscribers."""
        def failing_callback(event: Event):
            raise ValueError("Test exception")
        
        # Subscribe both failing and successful callbacks
        sub_id1 = self.event_bus.subscribe('error_test', failing_callback)
        sub_id2 = self.event_bus.subscribe('error_test', self.success_callback)
        
        # Publish event - should not raise exception
        self.event_bus.publish('error_test', 'test_data')
        
        # Successful callback should still have been called
        assert self.successful_calls == 1
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id1)
        self.event_bus.unsubscribe(sub_id2)
    
    def test_invalid_event_types(self):
        """Test handling of invalid event types."""
        # None event type should not crash
        sub_id1 = self.event_bus.subscribe(None, self.success_callback)
        self.event_bus.publish(None, 'test_data')
        
        # Empty string event type
        sub_id2 = self.event_bus.subscribe('', self.success_callback)
        self.event_bus.publish('', 'test_data')
        
        assert self.successful_calls == 2
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id1)
        self.event_bus.unsubscribe(sub_id2)
    
    def test_unsubscribe_nonexistent(self):
        """Test unsubscribing non-existent subscription doesn't crash."""
        # Should not raise exception
        result1 = self.event_bus.unsubscribe('nonexistent_id')
        result2 = self.event_bus.unsubscribe('another_fake_id')
        
        # Should return False for non-existent subscriptions
        assert result1 is False
        assert result2 is False
    
    def test_empty_event_data(self):
        """Test events with empty/None data."""
        sub_id = self.event_bus.subscribe('empty_test', self.success_callback)
        
        # Test various empty data scenarios
        self.event_bus.publish('empty_test', None)
        self.event_bus.publish('empty_test', {})
        self.event_bus.publish('empty_test', [])
        self.event_bus.publish('empty_test', '')
        
        assert self.successful_calls == 4
        
        # Cleanup
        self.event_bus.unsubscribe(sub_id)


class TestEventBusPerformance:
    """Test performance characteristics."""
    
    def setup_method(self):
        """Setup fresh EventBus for each test."""
        self.event_bus = EventBus()
        self.callback_times = []
    
    def timed_callback(self, event: Event):
        """Callback that records timing."""
        self.callback_times.append(time.time())
    
    def test_event_delivery_speed(self):
        """Test event delivery performance."""
        self.event_bus.subscribe('speed_test', self.timed_callback)
        
        start_time = time.time()
        
        # Publish many events quickly
        for i in range(100):
            self.event_bus.publish('speed_test', f'event_{i}')
        
        end_time = time.time()
        
        # Should complete quickly (under 1 second for 100 events)
        duration = end_time - start_time
        assert duration < 1.0
        assert len(self.callback_times) == 100
    
    def test_many_subscribers_performance(self):
        """Test performance with many subscribers."""
        callbacks_called = []
        
        # Create many callbacks
        def create_callback(i):
            def callback(event):
                callbacks_called.append(i)
            return callback
        
        # Subscribe 50 callbacks
        for i in range(50):
            self.event_bus.subscribe('many_subs_test', create_callback(i))
        
        start_time = time.time()
        self.event_bus.publish('many_subs_test', 'test_data')
        end_time = time.time()
        
        # Should complete quickly even with many subscribers
        duration = end_time - start_time
        assert duration < 0.1  # Should be very fast
        assert len(callbacks_called) == 50
    
    def test_subscription_overhead(self):
        """Test subscribe/unsubscribe performance."""
        subscription_ids = []
        
        # Create callbacks and subscribe
        for i in range(100):
            def callback(event, i=i):
                pass
            
            # Time subscriptions
            start_time = time.time()
            sub_id = self.event_bus.subscribe('overhead_test', callback)
            subscription_ids.append(sub_id)
        subscribe_time = time.time() - start_time
        
        # Time unsubscriptions
        start_time = time.time()
        for sub_id in subscription_ids:
            self.event_bus.unsubscribe(sub_id)
        unsubscribe_time = time.time() - start_time
        
        # Should be reasonably fast
        assert subscribe_time < 0.1
        assert unsubscribe_time < 0.1


class TestEventBusMemoryManagement:
    """Test memory management and cleanup."""
    
    def setup_method(self):
        """Setup fresh EventBus for each test."""
        self.event_bus = EventBus()
    
    def test_memory_cleanup_after_unsubscribe(self):
        """Test that unsubscribing cleans up memory properly."""
        subscription_ids = []
        
        # Create and subscribe many callbacks
        for i in range(20):
            def callback(event, i=i):
                pass
            sub_id = self.event_bus.subscribe('cleanup_test', callback)
            subscription_ids.append(sub_id)
        
        # Verify subscriptions exist
        assert len(self.event_bus._subscribers['cleanup_test']) == 20
        
        # Unsubscribe all
        for sub_id in subscription_ids:
            self.event_bus.unsubscribe(sub_id)
        
        # Verify cleanup - list should be empty
        assert len(self.event_bus._subscribers.get('cleanup_test', [])) == 0
    
    def test_rapid_subscribe_unsubscribe_cycles(self):
        """Test memory stability with rapid subscription changes."""
        # Rapid subscribe/unsubscribe cycles
        for cycle in range(10):
            subscription_ids = []
            
            # Subscribe batch
            for i in range(10):
                def callback(event, i=i):
                    pass
                sub_id = self.event_bus.subscribe(f'cycle_test_{i}', callback)
                subscription_ids.append(sub_id)
            
            # Unsubscribe batch
            for sub_id in subscription_ids:
                self.event_bus.unsubscribe(sub_id)
        
        # Should not accumulate memory - all should be cleaned up
        total_subscribers = sum(len(subs) for subs in self.event_bus._subscribers.values())
        assert total_subscribers == 0
    
    def test_large_event_payload_handling(self):
        """Test handling of large event payloads."""
        received_data = []
        
        def callback(event):
            received_data.append(len(str(event.data)))
        
        self.event_bus.subscribe('large_payload_test', callback)
        
        # Create large data payload
        large_data = {'data': 'x' * 10000}  # 10KB string
        self.event_bus.publish('large_payload_test', large_data)
        
        # Should handle large payload without issues
        assert len(received_data) == 1
        assert received_data[0] > 10000


# Integration with pytest fixtures for complex scenarios
@pytest.fixture
def event_bus():
    """Pytest fixture providing fresh EventBus instance."""
    return EventBus()


def test_callback_modification_during_execution(event_bus):
    """Test edge case where callback modifies subscriber list."""
    modification_count = 0
    
    def modifying_callback(event: Event):
        nonlocal modification_count
        modification_count += 1
        
        # Try to modify subscribers during callback execution
        def new_callback(e):
            pass
        
        if modification_count == 1:
            event_bus.subscribe('modification_test', new_callback)
    
    def stable_callback(event: Event):
        pass
    
    event_bus.subscribe('modification_test', modifying_callback)
    event_bus.subscribe('modification_test', stable_callback)
    
    # This should not crash or cause issues
    event_bus.publish('modification_test', 'test_data')
    
    # Both callbacks should have been called
    assert modification_count == 1
    # New callback should be registered
    assert len(event_bus._subscribers['modification_test']) == 3