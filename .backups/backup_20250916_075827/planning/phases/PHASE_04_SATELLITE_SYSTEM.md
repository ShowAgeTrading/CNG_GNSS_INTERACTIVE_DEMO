# Phase 04: Satellite System Implementation
**Version:** 1.0  
**Created:** 2025-09-15  
**Author:** GitHub Copilot  
**Purpose:** Build satellite constellation management and orbital mechanics  
**Estimated Duration:** 4-5 days  
**Complexity:** Large  

---

## Phase Overview

### Objectives
- Implement accurate orbital mechanics for satellite constellation simulation
- Create satellite models with realistic rendering and animation
- Build constellation management for GPS, GLONASS, Galileo, and BeiDou
- Develop line-of-sight calculations for receiver-satellite visibility
- Implement satellite selection and tracking functionality
- Optimize performance for 100+ satellites with real-time updates

### Success Criteria
- [ ] Accurate orbital propagation matching real satellite positions
- [ ] 4 major GNSS constellations fully implemented and visible
- [ ] Line-of-sight calculations correct within 1-meter accuracy
- [ ] Satellite selection and tracking responsive to user interaction
- [ ] Performance maintains 60 FPS with 100+ active satellites
- [ ] Satellite data integrates seamlessly with receiver positioning

---

## Technical Architecture

### Satellite System Structure
```
src/satellite/
├── __init__.py                    # Satellite module exports
├── constellation_manager.py       # Overall constellation coordination
├── orbital/
│   ├── orbital_mechanics.py      # SGP4/SDP4 orbital propagation
│   ├── ephemeris_loader.py       # TLE and almanac data loading
│   └── coordinate_transforms.py   # ECI/ECEF transformations
├── models/
│   ├── satellite_renderer.py     # 3D satellite visualization
│   ├── constellation_types.py    # GPS, GLONASS, Galileo, BeiDou
│   └── satellite_database.py     # Satellite catalog and metadata
├── tracking/
│   ├── visibility_calculator.py  # Line-of-sight calculations
│   ├── selection_manager.py      # User selection handling
│   └── tracking_controller.py    # Camera tracking functionality
└── utils/
    ├── time_utils.py             # Time system conversions
    └── math_orbital.py           # Orbital mathematics utilities
```

---

## Detailed Implementation Tasks

### Task 4.1: Orbital Mechanics Engine
**Priority:** Critical  
**Estimated Time:** 8-10 hours  
**File:** `src/satellite/orbital/orbital_mechanics.py`

#### SGP4/SDP4 Implementation
```python
class OrbitalPropagator:
    """
    Accurate orbital mechanics using SGP4/SDP4 models.
    
    Capabilities:
    - High-precision satellite position prediction
    - Atmospheric drag and gravitational perturbation modeling
    - Support for all orbital regimes (LEO, MEO, GEO)
    - Real-time position updates synchronized with simulation time
    """
    
    def __init__(self) -> None:
        self._satellites: Dict[str, SatelliteOrbit] = {}
        self._earth_constants = EarthConstants()
        self._gravitational_model = GravitationalModel()
        
    def add_satellite(self, satellite_id: str, tle_data: TLEData) -> None:
        """Add satellite with Two-Line Element orbital parameters."""
        
    def propagate_position(self, satellite_id: str, julian_date: float) -> SatelliteState:
        """Calculate satellite position at specific time."""
        
    def propagate_all(self, simulation_time: datetime) -> Dict[str, SatelliteState]:
        """Update all satellite positions for current simulation time."""
        
    def get_orbital_elements(self, satellite_id: str) -> OrbitalElements:
        """Get current orbital elements for satellite."""
```

#### Coordinate System Transformations
```python
class CoordinateTransforms:
    """Convert between different coordinate reference frames."""
    
    @staticmethod
    def eci_to_ecef(position_eci: Vec3, velocity_eci: Vec3, 
                    julian_date: float) -> Tuple[Vec3, Vec3]:
        """Convert Earth-Centered Inertial to Earth-Centered Earth-Fixed."""
        
    @staticmethod
    def ecef_to_geodetic(position_ecef: Vec3) -> Tuple[float, float, float]:
        """Convert ECEF to latitude, longitude, altitude."""
        
    @staticmethod
    def topocentric_coordinates(satellite_ecef: Vec3, observer_ecef: Vec3) -> TopoCoords:
        """Calculate azimuth, elevation, range from observer to satellite."""
```

#### Orbital Elements and State
```python
@dataclass
class OrbitalElements:
    """Keplerian orbital elements."""
    semi_major_axis: float          # km
    eccentricity: float            # dimensionless
    inclination: float             # radians
    right_ascension: float         # radians
    argument_of_perigee: float     # radians
    mean_anomaly: float            # radians
    epoch: datetime                # reference time

@dataclass
class SatelliteState:
    """Complete satellite state at specific time."""
    satellite_id: str
    position_eci: Vec3             # km, Earth-Centered Inertial
    velocity_eci: Vec3             # km/s, Earth-Centered Inertial
    position_ecef: Vec3            # km, Earth-Centered Earth-Fixed
    latitude: float                # degrees
    longitude: float               # degrees
    altitude: float                # km above sea level
    timestamp: datetime            # UTC time of state
```

### Task 4.2: Constellation Management
**Priority:** Critical  
**Estimated Time:** 6-8 hours  
**File:** `src/satellite/constellation_manager.py`

#### Constellation Controller
```python
class ConstellationManager(ComponentInterface):
    """
    Manages multiple GNSS constellations with real-time updates.
    
    Supported Constellations:
    - GPS (31 satellites)
    - GLONASS (24 satellites)  
    - Galileo (30 satellites)
    - BeiDou (35 satellites)
    """
    
    def __init__(self, event_bus: EventBus, clock: SimulationClock) -> None:
        self._event_bus = event_bus
        self._clock = clock
        self._constellations: Dict[str, Constellation] = {}
        self._orbital_propagator = OrbitalPropagator()
        self._update_interval = 1.0  # seconds
        self._last_update = None
        
    def initialize(self, app: Application) -> bool:
        """Load constellation data and initialize orbital propagator."""
        
    def update(self, delta_time: float) -> None:
        """Update all satellite positions based on simulation time."""
        
    def get_constellation(self, name: str) -> Optional[Constellation]:
        """Get specific constellation by name."""
        
    def get_all_satellites(self) -> List[SatelliteState]:
        """Get current state of all satellites across constellations."""
        
    def get_visible_satellites(self, observer_position: Vec3) -> List[SatelliteState]:
        """Get satellites visible from observer location."""
```

#### Constellation Definitions
```python
class Constellation:
    """Individual constellation (GPS, GLONASS, etc.) management."""
    
    def __init__(self, name: str, config: ConstellationConfig) -> None:
        self.name = name
        self.satellites: Dict[str, Satellite] = {}
        self.config = config
        self.active = True
        
    def load_tle_data(self, tle_file_path: str) -> None:
        """Load Two-Line Element data for constellation satellites."""
        
    def update_positions(self, simulation_time: datetime) -> None:
        """Update all satellite positions in constellation."""
        
    def get_satellite_count(self) -> int:
        """Get number of active satellites in constellation."""
        
    def set_visibility(self, visible: bool) -> None:
        """Enable/disable constellation visibility."""

@dataclass
class ConstellationConfig:
    """Configuration for constellation behavior."""
    update_interval: float = 1.0      # Position update frequency (seconds)
    max_satellites: int = 50          # Maximum satellites to track
    min_elevation: float = 5.0        # Minimum elevation for visibility (degrees)
    prediction_hours: int = 24        # Hours to pre-calculate positions
    color_scheme: Tuple[float, float, float] = (1.0, 1.0, 1.0)  # RGB color
```

### Task 4.3: Satellite Rendering and Visualization
**Priority:** High  
**Estimated Time:** 5-6 hours  
**Files:** `src/satellite/models/satellite_renderer.py`, `constellation_types.py`

#### 3D Satellite Rendering
```python
class SatelliteRenderer:
    """
    3D visualization of satellites with constellation-specific appearance.
    
    Rendering Features:
    - Realistic satellite models with solar panels
    - Constellation-specific coloring and icons
    - Orbital trail visualization
    - Distance-based level of detail
    - Selection highlighting and information display
    """
    
    def __init__(self, graphics_manager: GraphicsManager) -> None:
        self._graphics = graphics_manager
        self._satellite_nodes: Dict[str, NodePath] = {}
        self._orbital_trails: Dict[str, LineSegs] = {}
        self._selection_highlight: NodePath = None
        self._lod_manager = SatelliteLODManager()
        
    def create_satellite_model(self, satellite: Satellite) -> NodePath:
        """Create 3D model for satellite based on constellation type."""
        
    def update_satellite_position(self, satellite_id: str, state: SatelliteState) -> None:
        """Update satellite 3D position and orientation."""
        
    def update_orbital_trail(self, satellite_id: str, trail_points: List[Vec3]) -> None:
        """Update orbital trail visualization."""
        
    def highlight_satellite(self, satellite_id: str) -> None:
        """Highlight selected satellite with visual indicator."""
        
    def set_constellation_visibility(self, constellation: str, visible: bool) -> None:
        """Show/hide entire constellation."""
```

#### Constellation-Specific Models
```python
class ConstellationTypes:
    """Define visual characteristics for each constellation type."""
    
    GPS_CONFIG = SatelliteVisualConfig(
        model_file="gps_satellite.obj",
        base_color=(0.2, 0.7, 1.0),        # Light blue
        scale=1.0,
        solar_panel_count=2,
        antenna_type="patch_array"
    )
    
    GLONASS_CONFIG = SatelliteVisualConfig(
        model_file="glonass_satellite.obj", 
        base_color=(1.0, 0.3, 0.3),        # Red
        scale=1.1,
        solar_panel_count=2,
        antenna_type="helical"
    )
    
    GALILEO_CONFIG = SatelliteVisualConfig(
        model_file="galileo_satellite.obj",
        base_color=(0.3, 1.0, 0.3),        # Green
        scale=0.9,
        solar_panel_count=2,
        antenna_type="phased_array"
    )
    
    BEIDOU_CONFIG = SatelliteVisualConfig(
        model_file="beidou_satellite.obj",
        base_color=(1.0, 0.8, 0.2),        # Yellow
        scale=1.0,
        solar_panel_count=2,
        antenna_type="patch_array"
    )
```

#### Level of Detail Management
```python
class SatelliteLODManager:
    """Optimize satellite rendering based on distance and visibility."""
    
    def __init__(self) -> None:
        self.lod_distances = {
            "high_detail": 50000.0,      # < 50,000 km: Full 3D model
            "medium_detail": 200000.0,   # < 200,000 km: Simplified model
            "low_detail": 1000000.0,     # < 1,000,000 km: Icon only
            "invisible": float('inf')     # > 1,000,000 km: Hidden
        }
        
    def get_lod_level(self, camera_distance: float) -> str:
        """Determine appropriate level of detail for satellite."""
        
    def apply_lod(self, satellite_node: NodePath, lod_level: str) -> None:
        """Apply level of detail settings to satellite model."""
```

### Task 4.4: Visibility and Line-of-Sight Calculations
**Priority:** Critical  
**Estimated Time:** 4-5 hours  
**File:** `src/satellite/tracking/visibility_calculator.py`

#### Visibility Engine
```python
class VisibilityCalculator:
    """
    Calculate satellite visibility from ground-based observers.
    
    Calculations:
    - Line-of-sight determination with Earth occlusion
    - Elevation and azimuth angles
    - Range and range rate
    - Atmospheric effects on signal path
    - Multipath potential assessment
    """
    
    def __init__(self) -> None:
        self._earth_radius = 6371.0  # km
        self._atmosphere_height = 100.0  # km
        self._min_elevation = 5.0  # degrees
        
    def is_satellite_visible(self, satellite_pos: Vec3, observer_pos: Vec3) -> bool:
        """Determine if satellite is visible from observer location."""
        
    def calculate_look_angles(self, satellite_pos: Vec3, 
                            observer_pos: Vec3) -> LookAngles:
        """Calculate azimuth, elevation, and range to satellite."""
        
    def get_visible_satellites(self, satellite_states: List[SatelliteState],
                             observer_position: Vec3) -> List[VisibleSatellite]:
        """Filter satellites by visibility from observer."""
        
    def calculate_signal_strength(self, satellite_pos: Vec3, observer_pos: Vec3,
                                satellite_power: float) -> float:
        """Estimate received signal strength accounting for path loss."""

@dataclass
class LookAngles:
    """Observer-to-satellite angular measurements."""
    azimuth: float      # degrees from north (0-360)
    elevation: float    # degrees above horizon (0-90)
    range_km: float     # distance in kilometers
    range_rate: float   # rate of change in km/s

@dataclass
class VisibleSatellite:
    """Satellite with visibility information."""
    satellite_state: SatelliteState
    look_angles: LookAngles
    signal_strength: float
    multipath_risk: float  # 0-1, higher = more multipath potential
```

### Task 4.5: Satellite Selection and Tracking
**Priority:** Medium  
**Estimated Time:** 3-4 hours  
**Files:** `src/satellite/tracking/selection_manager.py`, `tracking_controller.py`

#### Selection Management
```python
class SatelliteSelectionManager:
    """
    Handle user selection and highlighting of satellites.
    
    Features:
    - Click-to-select satellite functionality
    - Multi-select with modifier keys
    - Constellation-wide selection
    - Selection persistence across time changes
    - Information display for selected satellites
    """
    
    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._selected_satellites: Set[str] = set()
        self._hover_satellite: Optional[str] = None
        self._selection_mode = SelectionMode.SINGLE
        
    def handle_mouse_click(self, screen_pos: Vec2, camera: Camera) -> None:
        """Handle mouse click for satellite selection."""
        
    def handle_mouse_hover(self, screen_pos: Vec2, camera: Camera) -> None:
        """Handle mouse hover for satellite highlighting."""
        
    def select_satellite(self, satellite_id: str, append: bool = False) -> None:
        """Select specific satellite by ID."""
        
    def select_constellation(self, constellation_name: str) -> None:
        """Select all satellites in constellation."""
        
    def clear_selection(self) -> None:
        """Clear all satellite selections."""
        
    def get_selected_info(self) -> List[SatelliteInfo]:
        """Get detailed information about selected satellites."""
```

#### Camera Tracking
```python
class SatelliteTrackingController:
    """Control camera to track selected satellites."""
    
    def __init__(self, camera_controller: CameraController) -> None:
        self._camera = camera_controller
        self._tracking_target: Optional[str] = None
        self._tracking_mode = TrackingMode.FOLLOW
        self._tracking_distance = 5000.0  # km
        
    def start_tracking(self, satellite_id: str, mode: TrackingMode) -> None:
        """Begin tracking specified satellite."""
        
    def stop_tracking(self) -> None:
        """Stop satellite tracking and return camera control to user."""
        
    def update_tracking(self, satellite_states: Dict[str, SatelliteState]) -> None:
        """Update camera position to track target satellite."""
        
    def set_tracking_distance(self, distance_km: float) -> None:
        """Set distance from satellite for tracking camera."""

class TrackingMode(Enum):
    """Different satellite tracking camera modes."""
    FOLLOW = "follow"           # Camera follows satellite movement
    OBSERVE = "observe"         # Camera points at satellite from fixed position
    ORBIT = "orbit"            # Camera orbits around satellite
    CHASE = "chase"            # Camera follows from behind satellite
```

---

## Integration Points

### Graphics System Integration
- **Satellite Models:** 3D models rendered through graphics pipeline
- **Orbital Trails:** Line geometry for satellite path visualization
- **Selection Highlighting:** Visual feedback through material changes
- **Camera Tracking:** Integration with camera control system

### Time System Integration
- **Position Updates:** Satellite positions update with simulation time
- **Predictive Calculation:** Pre-calculate positions for smooth animation
- **Time Synchronization:** All satellites stay synchronized with clock
- **Historical Playback:** Support reverse time simulation

### Event System Integration
- **Selection Events:** `satellite.selected`, `satellite.deselected`
- **Visibility Events:** `satellite.visible`, `satellite.occluded`
- **Tracking Events:** `satellite.tracking.started`, `satellite.tracking.stopped`
- **Update Events:** `satellite.positions.updated`

---

## Performance Optimization

### Update Strategies
```python
class SatelliteUpdateOptimizer:
    """Optimize satellite position updates for performance."""
    
    def __init__(self) -> None:
        self._update_priorities: Dict[str, float] = {}
        self._lod_updates: Dict[str, float] = {}
        
    def prioritize_updates(self, visible_satellites: List[str],
                          selected_satellites: List[str]) -> None:
        """Prioritize updates for visible and selected satellites."""
        
    def batch_position_updates(self, satellite_states: List[SatelliteState]) -> None:
        """Batch position updates to minimize graphics calls."""
        
    def cull_distant_satellites(self, camera_position: Vec3,
                              max_distance: float) -> List[str]:
        """Remove satellites beyond visibility range from updates."""
```

### Memory Management
- **Satellite Model Pooling:** Reuse 3D models across similar satellites
- **Trail Point Limiting:** Limit orbital trail history to prevent memory growth
- **State Caching:** Cache calculated positions for performance
- **Garbage Collection:** Regular cleanup of unused satellite data

---

## Testing Strategy

### Unit Tests Required
- [ ] Orbital mechanics accuracy (compare with known satellite positions)
- [ ] Coordinate transformations (ECI/ECEF/geodetic conversions)
- [ ] Visibility calculations (line-of-sight with Earth occlusion)
- [ ] Selection handling (click detection and multi-select)
- [ ] Performance under load (100+ satellites updating)

### Integration Tests Required
- [ ] Graphics rendering with satellite updates
- [ ] Time synchronization across simulation speed changes
- [ ] Event flow for satellite selection and tracking
- [ ] Camera tracking behavior with satellite movement

### Accuracy Verification
- [ ] Satellite positions within 100m of published ephemeris data
- [ ] Visibility calculations match ground-truth data
- [ ] Orbital propagation stable over 24-hour simulation
- [ ] Coordinate transformations accurate to centimeter level

---

## Success Metrics

### Functional Requirements
- **Accuracy:** Satellite positions within 100m of real positions
- **Performance:** 60 FPS with 100+ active satellites
- **Responsiveness:** Selection response <50ms
- **Stability:** No crashes during 8-hour continuous operation

### User Experience Requirements
- **Visual Quality:** Satellites clearly distinguishable by constellation
- **Interaction:** Intuitive selection and tracking controls
- **Information:** Clear display of satellite status and orbital data
- **Performance:** Smooth animation without frame drops

---

## Handoff to Phase 05

### Satellite Data Ready for Receivers
- Accurate satellite positions available in real-time
- Visibility calculations provide satellite-receiver line-of-sight
- Signal strength estimates available for positioning calculations
- Event system provides satellite state updates to receiver system

### Integration Points Established
- Satellite state data structure defined and stable
- Visibility API ready for receiver positioning calculations
- Event communication established for satellite updates
- Performance optimized for additional receiver calculations

---

**References:**
- Previous Phase: `planning/phases/PHASE_03_GRAPHICS_ENGINE.md`
- Next Phase: `planning/phases/PHASE_05_RECEIVER_SYSTEM.md`
- Master Plan: `planning/MASTER_IMPLEMENTATION_PLAN.md`
- Integration Map: `planning/active_memo/INTEGRATION_MAP.md`

**Line Count:** 496/500