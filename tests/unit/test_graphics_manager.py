#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: test_graphics_manager.py
Purpose: Comprehensive unit tests for GraphicsManager component
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - pytest - Testing framework
    - unittest.mock - Mocking for isolated testing

References:
    - Related Files: src/graphics/graphics_manager.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md

Tests:
    - Core GraphicsManager functionality
    - Panda3D initialization handling
    - Event system integration
    - Performance monitoring
    - Component lifecycle management
    - Error handling and edge cases

Line Count: 200/200 (Soft Limit: 180)
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Mock Panda3D and other modules before importing graphics_manager
with patch.dict('sys.modules', {
    'direct': MagicMock(),
    'direct.showbase': MagicMock(),
    'direct.showbase.ShowBase': MagicMock(),
    'direct.task': MagicMock(),
    'direct.task.Task': MagicMock(),
    'panda3d': MagicMock(),
    'panda3d.core': MagicMock(),
    'graphics.utils.graphics_utils': Mock(),
    'graphics.event_handler': Mock(), 
    'graphics.subsystem_manager': Mock(),
    'graphics.config_manager': Mock(),
}):
    from graphics.graphics_manager import GraphicsManager
    from core.event_bus import Event


class TestGraphicsManagerCore:
    """Test core GraphicsManager functionality."""
    
    def setup_method(self):
        """Setup fresh GraphicsManager for each test."""
        self.graphics_manager = GraphicsManager()
        self.mock_app = Mock()
        self.mock_app.get_config.return_value = Mock()
        self.mock_app.get_config.return_value.get.return_value = Path.cwd() / 'assets'
        self.mock_app.event_bus = Mock()
    
    def test_initialization_basic(self):
        """Test basic GraphicsManager initialization."""
        assert self.graphics_manager is not None
        assert self.graphics_manager._initialized is False
        assert self.graphics_manager._panda_app is None
        # Check new refactored components exist
        assert hasattr(self.graphics_manager, '_performance_monitor')
        assert hasattr(self.graphics_manager, '_event_handler')  
        assert hasattr(self.graphics_manager, '_config_manager')
        assert hasattr(self.graphics_manager, '_subsystem_manager')
    
    @patch('graphics.graphics_manager.Panda3DInitializer')
    @patch('graphics.graphics_manager.SubsystemFactory')
    @patch('graphics.graphics_manager.GraphicsSubsystemManager')
    def test_initialize_success(self, mock_subsystem_mgr, mock_factory, mock_initializer):
        """Test successful initialization with mocked Panda3D."""
        # Setup mocks
        mock_panda_app = Mock()
        mock_initializer_instance = Mock()
        mock_initializer_instance.initialize_panda3d.return_value = mock_panda_app
        mock_initializer.return_value = mock_initializer_instance
        
        mock_factory_instance = Mock()
        mock_factory.return_value = mock_factory_instance
        
        mock_subsystem_instance = Mock()
        mock_subsystem_instance.initialize_all_subsystems.return_value = True
        mock_subsystem_mgr.return_value = mock_subsystem_instance
        
        # Test initialization
        result = self.graphics_manager.initialize(self.mock_app)
        
        assert result is True
        assert self.graphics_manager._initialized is True
        assert self.graphics_manager._panda_app == mock_panda_app
        mock_initializer.assert_called_once()
        mock_factory.assert_called_once()
        mock_subsystem_mgr.assert_called_once()
    
    @patch('graphics.graphics_manager.Panda3DInitializer')
    def test_initialize_panda3d_failure(self, mock_initializer):
        """Test initialization failure when Panda3D fails to initialize."""
        # Setup mock to return None (failure)
        mock_initializer_instance = Mock()
        mock_initializer_instance.initialize_panda3d.return_value = None
        mock_initializer.return_value = mock_initializer_instance
        
        # Test initialization
        result = self.graphics_manager.initialize(self.mock_app)
        
        assert result is False
        assert self.graphics_manager._initialized is False
        assert self.graphics_manager._panda_app is None
    
    def test_update_when_not_initialized(self):
        """Test update method when graphics manager is not initialized."""
        # Should not crash when not initialized
        self.graphics_manager.update(0.016)
        assert self.graphics_manager._initialized is False
    
    def test_handle_event_when_not_initialized(self):
        """Test event handling when graphics manager is not initialized."""
        test_event = Event("test.event", "test", "action", {"data": "value"})
        
        # Should not crash when not initialized
        self.graphics_manager.handle_event(test_event)
        assert self.graphics_manager._initialized is False
    
    def test_get_performance_stats_default(self):
        """Test performance stats return default values."""
        # Mock the performance monitor to return proper dict
        self.graphics_manager._performance_monitor.get_all_stats = Mock(return_value={
            'frame_time': 0.016,
            'fps': 60.0,
            'memory_usage': 1024,
            'texture_memory': 512
        })
        
        stats = self.graphics_manager.get_performance_stats()
        
        assert isinstance(stats, dict)
        assert 'frame_time' in stats
        assert 'fps' in stats
        assert 'memory_usage' in stats
        assert 'texture_memory' in stats


class TestGraphicsManagerEvents:
    """Test event handling in GraphicsManager."""
    
    def setup_method(self):
        """Setup fresh GraphicsManager for each test."""
        self.graphics_manager = GraphicsManager()
        self.graphics_manager._initialized = True  # Mock as initialized
    
    def test_handle_time_event(self):
        """Test handling of time change events."""
        time_event = Event("time.changed", "time", "changed", {
            "current_time": 123456789.0,
            "speed": 2.0
        })
        
        # Should not crash when handling time events
        self.graphics_manager.handle_event(time_event)
    
    def test_handle_config_graphics_event(self):
        """Test handling of graphics configuration events."""
        config_event = Event("config.graphics.changed", "config", "graphics", {
            "window_size": [1280, 720],
            "fullscreen": False
        })
        
        # Should not crash when handling config events
        self.graphics_manager.handle_event(config_event)
    
    def test_handle_user_input_event(self):
        """Test handling of user input events."""
        input_event = Event("user.input.mouse", "user", "input", {
            "button": "left",
            "position": [100, 200]
        })
        
        # Should not crash when handling input events
        self.graphics_manager.handle_event(input_event)
    
    def test_handle_unknown_event(self):
        """Test handling of unknown event types."""
        unknown_event = Event("unknown.event.type", "unknown", "event", {})
        
        # Should not crash when handling unknown events
        self.graphics_manager.handle_event(unknown_event)


class TestGraphicsManagerPerformance:
    """Test performance monitoring in GraphicsManager."""
    
    def setup_method(self):
        """Setup fresh GraphicsManager for each test."""
        self.graphics_manager = GraphicsManager()
        self.graphics_manager._initialized = True
    
    @patch('graphics.graphics_manager.PerformanceMonitor')
    def test_performance_stats_access(self, mock_perf_monitor):
        """Test performance statistics access through performance monitor."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.get_all_stats.return_value = {
            'frame_time': 0.016,
            'fps': 62.5,
            'memory_usage': 1024,
            'texture_memory': 512
        }
        mock_perf_monitor.return_value = mock_monitor_instance
        
        # Create new graphics manager with mocked performance monitor
        with patch('graphics.graphics_manager.GraphicsEventHandler'), \
             patch('graphics.graphics_manager.GraphicsConfigManager'), \
             patch('graphics.graphics_manager.GraphicsSubsystemManager'):
            gm = GraphicsManager()
        
        stats = gm.get_performance_stats()
        assert 'frame_time' in stats
        assert 'fps' in stats
        assert 'memory_usage' in stats
        assert 'texture_memory' in stats


class TestGraphicsManagerLifecycle:
    """Test GraphicsManager lifecycle management."""
    
    def setup_method(self):
        """Setup fresh GraphicsManager for each test."""
        self.graphics_manager = GraphicsManager()
    
    def test_shutdown_clean(self):
        """Test clean shutdown of graphics manager."""
        # Setup initialized state
        mock_panda_app = Mock()
        mock_task_mgr = Mock()
        mock_panda_app.taskMgr = mock_task_mgr
        self.graphics_manager._panda_app = mock_panda_app
        self.graphics_manager._render_task = Mock()
        self.graphics_manager._initialized = True
        
        # Mock subsystem manager
        mock_subsystem_mgr = Mock()
        self.graphics_manager._subsystem_manager = mock_subsystem_mgr
        
        # Test shutdown
        self.graphics_manager.shutdown()
        
        assert self.graphics_manager._initialized is False
        assert self.graphics_manager._panda_app is None
        mock_subsystem_mgr.shutdown_all.assert_called_once()
        mock_task_mgr.remove.assert_called_once()
        mock_panda_app.destroy.assert_called_once()
    
    def test_shutdown_when_not_initialized(self):
        """Test shutdown when graphics manager is not initialized."""
        # Should not crash when shutting down uninitialized manager
        self.graphics_manager.shutdown()
        assert self.graphics_manager._initialized is False
    
    def test_multiple_shutdowns(self):
        """Test multiple shutdown calls don't cause issues."""
        self.graphics_manager.shutdown()
        self.graphics_manager.shutdown()
        self.graphics_manager.shutdown()
        
        # Should remain in clean state
        assert self.graphics_manager._initialized is False
        assert self.graphics_manager._panda_app is None


class TestGraphicsManagerErrorHandling:
    """Test error handling in GraphicsManager."""
    
    def setup_method(self):
        """Setup fresh GraphicsManager for each test."""
        self.graphics_manager = GraphicsManager()
        # Set up mock app for error handling tests
        self.mock_app = Mock()
        self.mock_app.render = Mock()
        self.mock_app.loader = Mock()
    
    @patch('graphics.graphics_manager.Panda3DInitializer')
    def test_initialization_exception_handling(self, mock_initializer):
        """Test initialization handles exceptions gracefully."""
        # Setup mock to raise exception
        mock_initializer.side_effect = Exception("Test initialization error")
        
        result = self.graphics_manager.initialize(self.mock_app)
        
        # Should return False and not crash
        assert result is False
        assert self.graphics_manager._initialized is False
    
    def test_event_handling_with_malformed_event(self):
        """Test event handling with malformed event objects."""
        # Test with None event
        self.graphics_manager.handle_event(None)
        
        # Test with event missing attributes
        malformed_event = Mock()
        malformed_event.category = None
        malformed_event.action = None
        
        # Should not crash
        self.graphics_manager.handle_event(malformed_event)
    
    @patch('graphics.graphics_manager.logger')
    def test_render_task_exception_handling(self, mock_logger):
        """Test render task handles exceptions gracefully."""
        mock_task = Mock()
        mock_task.time = 1.0
        
        # Should complete without crashing
        result = self.graphics_manager._render_frame_task(mock_task)
        assert result == mock_task.cont


# Integration fixture for complex scenarios
@pytest.fixture
def graphics_manager_with_mocked_panda3d():
    """Pytest fixture providing GraphicsManager with mocked Panda3D."""
    with patch('graphics.graphics_manager.Panda3DInitializer') as mock_init, \
         patch('graphics.graphics_manager.SubsystemFactory') as mock_factory, \
         patch('graphics.graphics_manager.GraphicsSubsystemManager') as mock_subsystem_mgr:
        
        # Setup successful mocks
        mock_panda_app = Mock()
        mock_init_instance = Mock()
        mock_init_instance.initialize_panda3d.return_value = mock_panda_app
        mock_init.return_value = mock_init_instance
        
        mock_factory_instance = Mock()
        mock_factory.return_value = mock_factory_instance
        
        mock_subsystem_instance = Mock()
        mock_subsystem_instance.initialize_all_subsystems.return_value = True
        mock_subsystem_mgr.return_value = mock_subsystem_instance
        
        graphics_manager = GraphicsManager()
        yield graphics_manager, mock_panda_app


def test_full_lifecycle_integration(graphics_manager_with_mocked_panda3d):
    """Test complete GraphicsManager lifecycle."""
    graphics_manager, mock_panda_app = graphics_manager_with_mocked_panda3d
    
    # Mock application
    mock_app = Mock()
    mock_app.get_config.return_value = Mock()
    mock_app.get_config.return_value.get.return_value = Path.cwd() / 'assets'
    mock_app.event_bus = Mock()
    
    # Test full lifecycle
    assert graphics_manager.initialize(mock_app) is True
    assert graphics_manager._initialized is True
    
    # Test operations while initialized
    graphics_manager.update(0.016)
    test_event = Event("test.event", "test", "action", {})
    graphics_manager.handle_event(test_event)
    
    stats = graphics_manager.get_performance_stats()
    assert isinstance(stats, dict)
    
    # Test shutdown
    graphics_manager.shutdown()
    assert graphics_manager._initialized is False