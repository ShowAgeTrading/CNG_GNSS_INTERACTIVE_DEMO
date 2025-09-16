#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: test_camera_controller.py
Purpose: Unit tests for CameraController component
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - pytest - Testing framework
    - unittest.mock - Mocking for isolated testing

References:
    - Related Files: src/graphics/camera/camera_controller.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md

Tests:
    - Basic CameraController functionality
    - Input handling and processing
    - Camera mode management
    - Position and orientation updates
    - Constraint application
    - Error handling

Line Count: 180/200 (Soft Limit: 180)
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Set

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Mock Panda3D and utilities before importing camera controller
with patch.dict('sys.modules', {
    'direct': MagicMock(),
    'direct.showbase': MagicMock(),
    'direct.showbase.DirectObject': MagicMock(),
    'direct.task': MagicMock(),
    'panda3d': MagicMock(),
    'panda3d.core': MagicMock(),
    'graphics.utils.panda3d_utils': Mock(),
    'graphics.graphics_manager': Mock()
}):
    from graphics.camera.camera_controller import CameraController


class TestCameraControllerCore:
    """Test core CameraController functionality."""
    
    def setup_method(self):
        """Setup fresh CameraController for each test."""
        with patch('graphics.camera.camera_controller.DirectObject'):
            self.camera_controller = CameraController()
    
    def test_initialization_basic(self):
        """Test basic CameraController initialization."""
        assert self.camera_controller is not None
        assert self.camera_controller._distance == 15000.0  # Default Earth distance
        assert self.camera_controller._azimuth == 0.0
        assert self.camera_controller._elevation == 0.0
        assert self.camera_controller._target_distance == 15000.0
    
    def test_initialization_parameters(self):
        """Test CameraController initialization with custom parameters."""
        with patch('graphics.camera.camera_controller.DirectObject'):
            custom_controller = CameraController(
                initial_distance=25000.0,
                initial_azimuth=45.0,
                initial_elevation=30.0
            )
        
        assert custom_controller._distance == 25000.0
        assert custom_controller._azimuth == 45.0
        assert custom_controller._elevation == 30.0
    
    @patch('graphics.camera.camera_controller.base')
    def test_initialize_success(self, mock_base):
        """Test successful camera controller initialization."""
        mock_base.camera = Mock()
        
        result = self.camera_controller.initialize()
        
        assert result is True
        mock_base.camera.setPos.assert_called()
        mock_base.camera.lookAt.assert_called()
    
    @patch('graphics.camera.camera_controller.base', None)
    def test_initialize_no_base(self):
        """Test initialization when no Panda3D base is available."""
        result = self.camera_controller.initialize()
        
        assert result is False


class TestCameraControllerMovement:
    """Test camera movement and positioning."""
    
    def setup_method(self):
        """Setup camera controller with mocked Panda3D."""
        with patch('graphics.camera.camera_controller.DirectObject'):
            self.camera_controller = CameraController()
    
    def test_set_distance(self):
        """Test setting camera distance."""
        self.camera_controller.set_distance(20000.0)
        
        assert self.camera_controller._target_distance == 20000.0
    
    def test_set_distance_with_constraints(self):
        """Test distance setting respects constraints."""
        # Test minimum distance constraint
        self.camera_controller.set_distance(1000.0)  # Below Earth radius
        assert self.camera_controller._target_distance >= 6500.0  # Should be constrained
        
        # Test maximum distance constraint
        self.camera_controller.set_distance(200000.0)  # Very far
        assert self.camera_controller._target_distance <= 100000.0  # Should be constrained
    
    def test_rotate_azimuth(self):
        """Test azimuth rotation."""
        initial_azimuth = self.camera_controller._azimuth
        self.camera_controller.rotate_azimuth(45.0)
        
        assert self.camera_controller._azimuth == initial_azimuth + 45.0
    
    def test_rotate_elevation(self):
        """Test elevation rotation."""
        initial_elevation = self.camera_controller._elevation
        self.camera_controller.rotate_elevation(30.0)
        
        assert self.camera_controller._elevation == initial_elevation + 30.0
    
    def test_elevation_constraints(self):
        """Test elevation constraints are applied."""
        # Test maximum elevation
        self.camera_controller.rotate_elevation(100.0)  # Beyond 89 degrees
        assert self.camera_controller._elevation <= 89.0
        
        # Test minimum elevation
        self.camera_controller._elevation = 0.0
        self.camera_controller.rotate_elevation(-100.0)  # Beyond -89 degrees
        assert self.camera_controller._elevation >= -89.0
    
    @patch('graphics.camera.camera_controller.base')
    def test_update_camera_position(self, mock_base):
        """Test camera position update calculations."""
        mock_base.camera = Mock()
        
        # Set known values
        self.camera_controller._distance = 10000.0
        self.camera_controller._azimuth = 45.0
        self.camera_controller._elevation = 30.0
        
        self.camera_controller._update_camera_position()
        
        # Verify camera position was set (exact values depend on math)
        mock_base.camera.setPos.assert_called()
        mock_base.camera.lookAt.assert_called()


class TestCameraControllerInput:
    """Test camera input handling."""
    
    def setup_method(self):
        """Setup camera controller for input testing."""
        with patch('graphics.camera.camera_controller.DirectObject'):
            self.camera_controller = CameraController()
    
    def test_handle_mouse_drag(self):
        """Test mouse drag input handling."""
        initial_azimuth = self.camera_controller._azimuth
        initial_elevation = self.camera_controller._elevation
        
        # Simulate mouse drag
        self.camera_controller.handle_mouse_drag(10.0, 5.0)
        
        # Should change azimuth and elevation
        assert self.camera_controller._azimuth != initial_azimuth
        assert self.camera_controller._elevation != initial_elevation
    
    def test_handle_mouse_wheel(self):
        """Test mouse wheel zoom input."""
        initial_distance = self.camera_controller._target_distance
        
        # Simulate mouse wheel scroll
        self.camera_controller.handle_mouse_wheel(1.0)  # Zoom in
        assert self.camera_controller._target_distance < initial_distance
        
        self.camera_controller.handle_mouse_wheel(-1.0)  # Zoom out
        assert self.camera_controller._target_distance > initial_distance
    
    def test_handle_keyboard_input(self):
        """Test keyboard input handling."""
        keys_pressed = {'w', 'a'}  # Example key set
        
        # Should not crash with keyboard input
        self.camera_controller.handle_keyboard_input(keys_pressed)
    
    def test_input_sensitivity(self):
        """Test input sensitivity settings."""
        # Test with different sensitivity
        self.camera_controller.set_mouse_sensitivity(2.0)
        
        initial_azimuth = self.camera_controller._azimuth
        self.camera_controller.handle_mouse_drag(10.0, 0.0)
        change_high_sens = self.camera_controller._azimuth - initial_azimuth
        
        # Reset and test with lower sensitivity
        self.camera_controller._azimuth = initial_azimuth
        self.camera_controller.set_mouse_sensitivity(0.5)
        self.camera_controller.handle_mouse_drag(10.0, 0.0)
        change_low_sens = self.camera_controller._azimuth - initial_azimuth
        
        # Higher sensitivity should produce larger change
        assert abs(change_high_sens) > abs(change_low_sens)


class TestCameraControllerSmoothing:
    """Test camera movement smoothing."""
    
    def setup_method(self):
        """Setup camera controller for smoothing tests."""
        with patch('graphics.camera.camera_controller.DirectObject'):
            self.camera_controller = CameraController()
    
    @patch('graphics.camera.camera_controller.base')
    def test_smooth_movement_update(self, mock_base):
        """Test smooth camera movement over time."""
        mock_base.camera = Mock()
        
        # Set target different from current
        self.camera_controller._distance = 10000.0
        self.camera_controller._target_distance = 15000.0
        
        # Update should move towards target
        initial_distance = self.camera_controller._distance
        self.camera_controller.update(0.016)  # 60 FPS delta
        
        # Should have moved closer to target
        assert self.camera_controller._distance > initial_distance
        assert self.camera_controller._distance < self.camera_controller._target_distance
    
    def test_smoothing_factor_effect(self):
        """Test different smoothing factors."""
        # Test with high smoothing (slow movement)
        self.camera_controller._distance = 10000.0
        self.camera_controller._target_distance = 20000.0
        self.camera_controller._smooth_factor = 0.01  # Very slow
        
        initial_distance = self.camera_controller._distance
        self.camera_controller._smooth_distance_update(0.016)
        slow_change = self.camera_controller._distance - initial_distance
        
        # Reset and test with fast smoothing
        self.camera_controller._distance = 10000.0
        self.camera_controller._smooth_factor = 0.5  # Fast
        self.camera_controller._smooth_distance_update(0.016)
        fast_change = self.camera_controller._distance - initial_distance
        
        # Fast smoothing should produce larger change
        assert fast_change > slow_change


class TestCameraControllerConstraints:
    """Test camera movement constraints."""
    
    def setup_method(self):
        """Setup camera controller for constraint testing."""
        with patch('graphics.camera.camera_controller.DirectObject'):
            self.camera_controller = CameraController()
    
    def test_distance_constraints(self):
        """Test distance constraints are enforced."""
        # Test constraint application
        constrained_distance = self.camera_controller._apply_distance_constraints(5000.0)
        assert constrained_distance >= 6500.0  # Earth radius constraint
        
        constrained_distance = self.camera_controller._apply_distance_constraints(200000.0)
        assert constrained_distance <= 100000.0  # Maximum distance constraint
        
        # Valid distance should pass through
        valid_distance = 15000.0
        constrained_distance = self.camera_controller._apply_distance_constraints(valid_distance)
        assert constrained_distance == valid_distance
    
    def test_elevation_constraints(self):
        """Test elevation constraints are enforced."""
        # Test constraint application
        constrained_elevation = self.camera_controller._apply_elevation_constraints(100.0)
        assert constrained_elevation <= 89.0  # Maximum elevation
        
        constrained_elevation = self.camera_controller._apply_elevation_constraints(-100.0)
        assert constrained_elevation >= -89.0  # Minimum elevation
        
        # Valid elevation should pass through
        valid_elevation = 45.0
        constrained_elevation = self.camera_controller._apply_elevation_constraints(valid_elevation)
        assert constrained_elevation == valid_elevation


class TestCameraControllerErrorHandling:
    """Test error handling in CameraController."""
    
    def setup_method(self):
        """Setup camera controller for error testing."""
        with patch('graphics.camera.camera_controller.DirectObject'):
            self.camera_controller = CameraController()
    
    def test_handle_invalid_input_values(self):
        """Test handling of invalid input values."""
        # Test with None values
        self.camera_controller.handle_mouse_drag(None, None)
        self.camera_controller.handle_mouse_wheel(None)
        
        # Test with extreme values
        self.camera_controller.handle_mouse_drag(float('inf'), float('inf'))
        self.camera_controller.set_distance(float('nan'))
        
        # Should not crash and should maintain valid state
        assert isinstance(self.camera_controller._distance, (int, float))
        assert not (self.camera_controller._distance != self.camera_controller._distance)  # Check for NaN
    
    def test_update_without_initialization(self):
        """Test update method without proper initialization."""
        # Should not crash even if not properly initialized
        self.camera_controller.update(0.016)
    
    @patch('graphics.camera.camera_controller.base')
    def test_update_with_panda3d_error(self, mock_base):
        """Test handling of Panda3D errors during update."""
        # Setup mock to raise exception
        mock_base.camera.setPos.side_effect = Exception("Panda3D error")
        
        # Should not crash
        self.camera_controller._update_camera_position()


# Integration fixture
@pytest.fixture
def camera_controller_initialized():
    """Pytest fixture providing initialized CameraController."""
    with patch('graphics.camera.camera_controller.DirectObject'), \
         patch('graphics.camera.camera_controller.base') as mock_base:
        mock_base.camera = Mock()
        controller = CameraController()
        controller.initialize()
        yield controller, mock_base


def test_complete_camera_interaction_sequence(camera_controller_initialized):
    """Test complete camera interaction sequence."""
    controller, mock_base = camera_controller_initialized
    
    # Simulate user interaction sequence
    controller.handle_mouse_drag(10.0, 5.0)  # Rotate camera
    controller.handle_mouse_wheel(2.0)       # Zoom in
    controller.update(0.016)                 # Update smoothing
    controller.handle_mouse_drag(-5.0, -2.0) # Rotate back
    controller.update(0.016)                 # Update again
    
    # Should have called Panda3D camera updates
    assert mock_base.camera.setPos.call_count >= 2
    assert mock_base.camera.lookAt.call_count >= 2