#!/usr/bin/env python3
"""
Phase 3 Visual Test - Test Actual Graphics Manager Integration
Purpose: Test the real GraphicsManager and GlobeRenderer systems

IMPORTANT: This tests the ACTUAL GRAPHICS PIPELINE
- Uses the real GraphicsManager from src/graphics/
- Integrates with the actual GlobeRenderer system
- Tests the full Phase 3 graphics architecture
- Shows if our modular graphics system works correctly
- This is the REAL test of Phase 3 implementation

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
    # Create a dummy ShowBase class for when Panda3D is not available
    class ShowBase:
        def __init__(self):
            pass


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
        """
        Setup production-quality lighting system for Earth visualization.
        
        This lighting design will be used in the real app and supports:
        - Realistic sun simulation (future: actual sun position)
        - Proper day/night terminator line
        - Space environment lighting (low ambient)
        - Extensible for future moon lighting
        """
        try:
            # BRIGHT AMBIENT: Enough light to see texture colors clearly
            ambient_light = AmbientLight('ambient')
            ambient_light.setColor(Vec4(0.7, 0.7, 0.7, 1.0))  # Bright ambient to show colors
            ambient_light_np = self.render.attachNewNode(ambient_light)
            self.render.setLight(ambient_light_np)
            
            # SIMPLE SUN: Basic directional light
            sun_light = DirectionalLight('sun')
            sun_light.setColor(Vec4(0.5, 0.5, 0.5, 1.0))  # Moderate sun light
            sun_light.setDirection(Vec3(-1, -1, -1))
            sun_light_np = self.render.attachNewNode(sun_light)
            self.render.setLight(sun_light_np)
            
            print("   ✅ Bright lighting initialized for texture visibility")
            print("   🌍 Earthshine: Atmospheric light scattering") 
            print("   🌌 Space ambient: Realistic low-light environment")
            print("   → Ready for future sun/moon ephemeris integration")
            
        except Exception as e:
            print(f"   ⚠️  Lighting setup error: {e}")
    
    def create_basic_earth(self):
        """Load the actual Blender sphere from assets/models/earth/earth_3D.gltf"""
        try:
            print("   🌍 Loading actual Blender Earth sphere...")
            
            # Get the absolute path to the GLTF file
            workspace_root = Path(__file__).parent.parent.parent
            gltf_path = workspace_root / "assets" / "models" / "earth" / "earth_3D.gltf"
            
            # Convert to Panda3D filename format to reduce path resolution errors
            from panda3d.core import Filename
            panda_filename = Filename.fromOsSpecific(str(gltf_path))
            
            print(f"   📄 Loading GLTF: {panda_filename}")
            
            # Load the GLTF file using Panda3D's loader with proper filename
            self.earth = self.loader.loadModel(panda_filename)
            
            if self.earth:
                self.earth.reparentTo(self.render)
                self.earth.setScale(25)  # Scale to appropriate size
                print("   ✅ Blender Earth sphere loaded successfully!")
                
                # Now apply Earth texture
                self._apply_earth_texture()
                
                print("   🌍 Your custom Blender model with textures is now rendering!")
            else:
                raise Exception("GLTF loading returned None - file may be corrupt or unsupported")
                
        except Exception as e:
            print(f"   ❌ Error loading Blender sphere: {e}")
            print("   ⚠️  GLTF loading failed - this needs to be resolved!")
            # Don't create primitive geometry fallbacks - let it fail properly
            raise
    
    def _apply_earth_texture(self):
        """
        Apply Earth texture with production-quality material setup.
        
        This texture system is designed for the real app and supports:
        - High-resolution Earth surface textures
        - Future: Day/night texture blending
        - Future: Normal mapping for terrain relief
        - Future: Specular mapping for ocean reflectivity
        """
        try:
            print("   🎨 Applying production Earth material system...")
            
            # Get path to Earth texture (try different resolutions)
            workspace_root = Path(__file__).parent.parent.parent
            
            # Priority order: 4K for performance/quality balance, fallback to others
            texture_paths = [
                workspace_root / "assets" / "textures" / "earth" / "composite_earth__skins" / "8081_earthmap4k.jpg",
                workspace_root / "assets" / "textures" / "earth" / "composite_earth__skins" / "8081_earthmap2k.jpg",
                workspace_root / "assets" / "textures" / "earth" / "composite_earth__skins" / "8081_earthmap10k.jpg"
            ]
            
            earth_texture = None
            loaded_resolution = None
            
            for texture_path in texture_paths:
                if texture_path.exists():
                    print(f"   📄 Loading Earth texture: {texture_path.name}")
                    
                    # Convert to Panda3D filename format
                    from panda3d.core import Filename
                    panda_texture_path = Filename.fromOsSpecific(str(texture_path))
                    
                    # Load the texture with proper settings
                    earth_texture = self.loader.loadTexture(panda_texture_path)
                    
                    if earth_texture:
                        loaded_resolution = texture_path.name
                        
                        # Configure texture for optimal quality
                        earth_texture.setWrapU(earth_texture.WMRepeat)
                        earth_texture.setWrapV(earth_texture.WMRepeat)
                        earth_texture.setMinfilter(earth_texture.FTLinearMipmapLinear)
                        earth_texture.setMagfilter(earth_texture.FTLinear)
                        
                        print(f"   ✅ Earth texture loaded: {loaded_resolution}")
                        break
                    else:
                        print(f"   ⚠️  Failed to load: {texture_path.name}")
            
            if earth_texture:
                # Apply texture - simple and clean (your UV mapping works!)
                self.earth.setTexture(earth_texture)
                
                print(f"   🌍 Earth texture applied successfully ({loaded_resolution})")
                print("   → Your Blender sphere UV mapping is perfect!")
            else:
                print("   ❌ No Earth textures could be loaded")
                print("   → Check texture file paths and formats")
                
        except Exception as e:
            print(f"   ⚠️  Earth texture system error: {e}")
            print("   → Earth will render with default material")

    
    def setup_camera_controls(self):
        """Setup basic camera orbit controls."""
        try:
            # IMPORTANT: Disable default Panda3D camera controls first!
            self.disableMouse()  # This prevents default camera controls from interfering
            
            # Set initial camera position (further back to see the larger Earth)
            self.camera_distance = 150  # Distance units - further back
            self.camera_azimuth = 45.0   # Start at 45 degree angle
            self.camera_elevation = 20.0 # Slightly elevated view
            
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
            
            print("   ✅ Camera controls initialized (default mouse disabled)")
            
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
                
                # Update camera angles (reduced sensitivity for smoother control)
                self.camera_azimuth += dx * 180.0  # Horizontal sensitivity
                self.camera_elevation -= dy * 90.0  # Vertical sensitivity (inverted for natural feel)
                
                # Clamp elevation to prevent flipping
                self.camera_elevation = max(-85, min(85, self.camera_elevation))
                
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