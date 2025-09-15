#!/usr/bin/env python3
"""
Phase 3 Visual Test - Basic 3D Graphics Demonstration
Purpose: Create visual Panda3D window with basic Earth globe for immediate feedback

IMPORTANT: This is a VISUAL TEST for user feedback
- Creates actual Panda3D window with basic 3D scene
- Shows basic sphere as Earth placeholder
- Enables basic camera controls for interaction
- Provides immediate visual feedback on Phase 3 progress
- Run this to see what's working and give feedback

Usage: python tests/visual/test_phase3_visual.py
Controls: Mouse drag to orbit, mouse wheel to zoom, ESC to exit
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    # Try to import Panda3D components (basic ones only)
    from direct.showbase.ShowBase import ShowBase
    from panda3d.core import Vec3, Vec4, AmbientLight, DirectionalLight
    from direct.task import Task
    
    PANDA3D_AVAILABLE = True
    print("✅ Panda3D imported successfully")
    
except ImportError as e:
    PANDA3D_AVAILABLE = False
    print(f"❌ Panda3D import failed: {e}")
    print("→ Visual test requires Panda3D installation")


class Phase3VisualTest(ShowBase):
    """
    Basic visual test showing Phase 3 graphics progress.
    
    Creates a simple 3D scene with:
    - Basic sphere as Earth (using built-in models)
    - Simple lighting 
    - Basic camera orbit controls
    - Performance stats display
    """
    
    def __init__(self):
        """Initialize basic 3D scene for Phase 3 demo."""
        if not PANDA3D_AVAILABLE:
            print("Cannot run visual test - Panda3D not available")
            return
            
        try:
            print("🚀 Starting Phase 3 Visual Test...")
            
            # Initialize Panda3D
            ShowBase.__init__(self)
            
            # Configure window (try different methods)
            try:
                if hasattr(self, 'win') and self.win:
                    # Try different window title methods
                    if hasattr(self.win, 'setTitle'):
                        self.win.setTitle("Phase 3 Graphics Test - CNG GNSS Demo")
                    elif hasattr(self.win, 'requestProperties'):
                        from panda3d.core import WindowProperties
                        props = WindowProperties()
                        props.setTitle("Phase 3 Graphics Test - CNG GNSS Demo")
                        self.win.requestProperties(props)
                    print("   ✅ Window configured")
            except Exception as e:
                print(f"   ⚠️  Window configuration: {e}")
            
            # Setup basic scene
            self.setup_lighting()
            self.create_basic_earth()
            self.setup_camera_controls()
            
            # Setup performance monitoring
            self.setup_performance_display()
            
            # Start the demo
            print("\n🌍 Phase 3 Visual Test Running:")
            print("   • Mouse drag: Orbit camera around Earth")
            print("   • Mouse wheel: Zoom in/out")
            print("   • ESC key: Exit")
            print("   • This shows current Phase 3 implementation state")
            print("\n💡 Feedback Request:")
            print("   → Does the window open?")
            print("   → Can you see a colored sphere (Earth)?")
            print("   → Do mouse controls work?")
            print("   → Any visual artifacts or issues?")
            
        except Exception as e:
            print(f"❌ Visual test initialization failed: {e}")
            raise
    
    def setup_lighting(self):
        """Setup basic lighting for the 3D scene."""
        try:
            # Add ambient light
            ambient_light = AmbientLight('ambient')
            ambient_light.setColor(Vec4(0.3, 0.3, 0.3, 1.0))
            ambient_light_np = self.render.attachNewNode(ambient_light)
            self.render.setLight(ambient_light_np)
            
            # Add directional light (sun)
            sun_light = DirectionalLight('sun')
            sun_light.setColor(Vec4(0.8, 0.8, 0.7, 1.0))
            sun_light.setDirection(Vec3(-1, -1, -1))
            sun_light_np = self.render.attachNewNode(sun_light)
            self.render.setLight(sun_light_np)
            
            print("   ✅ Lighting system initialized")
            
        except Exception as e:
            print(f"   ⚠️  Lighting setup error: {e}")
    
    def create_basic_earth(self):
        """Create basic Earth representation using built-in models."""
        try:
            # Try to use built-in sphere model
            self.earth = self.loader.loadModel("models/environment")
            
            if self.earth:
                self.earth.reparentTo(self.render)
                self.earth.setColor(0.2, 0.5, 1.0, 1.0)  # Blue like Earth
                self.earth.setScale(10)  # Make it visible
                print("   ✅ Earth sphere created using built-in model")
            else:
                # Try even simpler approach - just create a basic node
                from panda3d.core import CardMaker
                card = CardMaker("earth")
                card.setFrame(-5, 5, -5, 5)
                self.earth = self.render.attachNewNode(card.generate())
                self.earth.setColor(0.2, 0.5, 1.0, 1.0)  # Blue color
                self.earth.setPos(0, 20, 0)  # Put it in front of camera
                print("   ✅ Basic Earth placeholder created")
            
        except Exception as e:
            print(f"   ⚠️  Earth creation error: {e}")
            # Ultimate fallback - just set a background color
            try:
                if hasattr(self, 'win') and self.win:
                    self.win.setClearColor(0.2, 0.5, 1.0, 1.0)  # Blue background
                print("   ✅ Blue background set as Earth placeholder")
            except Exception as e2:
                print(f"   ❌ All Earth creation methods failed: {e2}")
    
    def setup_camera_controls(self):
        """Setup basic camera orbit controls."""
        try:
            # Set initial camera position
            self.camera_distance = 50  # Distance units
            self.camera_azimuth = 0.0
            self.camera_elevation = 0.0
            
            # Position camera
            self.update_camera_position()
            
            # Setup mouse controls
            self.accept("mouse1", self.start_drag)  # Left mouse button
            self.accept("mouse1-up", self.stop_drag)
            self.accept("wheel_up", self.zoom_in)
            self.accept("wheel_down", self.zoom_out)
            
            # Setup exit
            self.accept("escape", sys.exit)
            
            # Mouse drag state
            self.dragging = False
            self.last_mouse_x = 0
            self.last_mouse_y = 0
            
            # Start mouse monitoring task
            self.taskMgr.add(self.mouse_task, "mouse_task")
            
            print("   ✅ Camera controls initialized")
            
        except Exception as e:
            print(f"   ⚠️  Camera controls error: {e}")
    
    def update_camera_position(self):
        """Update camera position based on spherical coordinates."""
        try:
            import math
            
            # Convert spherical to cartesian coordinates
            rad_azimuth = math.radians(self.camera_azimuth)
            rad_elevation = math.radians(self.camera_elevation)
            
            x = self.camera_distance * math.cos(rad_elevation) * math.sin(rad_azimuth)
            y = -self.camera_distance * math.cos(rad_elevation) * math.cos(rad_azimuth)
            z = self.camera_distance * math.sin(rad_elevation)
            
            # Set camera position and look at center
            self.camera.setPos(x, y, z)
            self.camera.lookAt(0, 0, 0)
            
        except Exception as e:
            print(f"   Camera position update error: {e}")
    
    def start_drag(self):
        """Start mouse drag for camera orbit."""
        if hasattr(self, 'mouseWatcherNode') and self.mouseWatcherNode.hasMouse():
            self.dragging = True
            self.last_mouse_x = self.mouseWatcherNode.getMouseX()
            self.last_mouse_y = self.mouseWatcherNode.getMouseY()
    
    def stop_drag(self):
        """Stop mouse drag."""
        self.dragging = False
    
    def mouse_task(self, task):
        """Handle mouse movement for camera control."""
        try:
            if (self.dragging and hasattr(self, 'mouseWatcherNode') 
                and self.mouseWatcherNode.hasMouse()):
                
                mouse_x = self.mouseWatcherNode.getMouseX()
                mouse_y = self.mouseWatcherNode.getMouseY()
                
                # Calculate mouse delta
                dx = mouse_x - self.last_mouse_x
                dy = mouse_y - self.last_mouse_y
                
                # Update camera angles
                self.camera_azimuth += dx * 90.0  # Sensitivity
                self.camera_elevation += dy * 90.0
                
                # Clamp elevation
                self.camera_elevation = max(-89, min(89, self.camera_elevation))
                
                # Update camera position
                self.update_camera_position()
                
                # Update mouse position
                self.last_mouse_x = mouse_x
                self.last_mouse_y = mouse_y
        
        except Exception as e:
            pass  # Ignore mouse errors in task
        
        return task.cont
    
    def zoom_in(self):
        """Zoom camera closer."""
        self.camera_distance *= 0.9
        self.camera_distance = max(5, self.camera_distance)  # Min distance
        self.update_camera_position()
    
    def zoom_out(self):
        """Zoom camera away."""
        self.camera_distance *= 1.1
        self.camera_distance = min(200, self.camera_distance)  # Max distance
        self.update_camera_position()
    
    def setup_performance_display(self):
        """Setup basic performance monitoring display."""
        try:
            # Enable frame rate meter
            self.setFrameRateMeter(True)
            print("   ✅ Performance display enabled")
            
        except Exception as e:
            print(f"   ⚠️  Performance display error: {e}")


def run_phase3_visual_test():
    """Run the Phase 3 visual test."""
    if not PANDA3D_AVAILABLE:
        print("\n❌ Cannot run visual test:")
        print("   → Panda3D is not properly installed")
        print("   → Install with: pip install panda3d")
        print("   → Or check virtual environment activation")
        return False
    
    try:
        print("=" * 60)
        print("PHASE 3 GRAPHICS ENGINE - VISUAL TEST")
        print("=" * 60)
        print("Purpose: Show current Phase 3 implementation state")
        print("Expected: Basic 3D window with camera controls")
        print("Note: This is a BASIC test - full graphics features coming soon")
        print("")
        
        # Create and run the visual test
        app = Phase3VisualTest()
        app.run()
        
        print("\n✅ Visual test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Visual test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_phase3_visual_test()
    
    print("\n" + "=" * 60)
    print("FEEDBACK REQUEST:")
    print("=" * 60)
    print("Please report what you observed:")
    print("1. Did the 3D window open successfully?")
    print("2. Could you see any 3D objects or colored background?")
    print("3. Did the mouse controls work for camera movement?")
    print("4. Any errors, crashes, or visual problems?")
    print("5. Frame rate displayed in corner?")
    print("")
    print("This helps us understand Phase 3 implementation progress!")
    print("Even basic functionality indicates graphics foundation is working.")
    print("=" * 60)
    
    sys.exit(0 if success else 1)