# Phase 05: Receiver System Implementation
**Version:** 1.0  
**Created:** 2025-09-15  
**Author:** GitHub Copilot  
**Purpose:** Build GNSS receiver positioning with base/rover/standalone modes  
**Estimated Duration:** 4-5 days  
**Complexity:** Large  

---

## Phase Overview

### Objectives
- Implement realistic GNSS receiver positioning algorithms
- Create base station, rover, and standalone receiver types
- Build RTK positioning with centimeter-level accuracy simulation
- Develop error modeling for atmospheric and multipath effects
- Implement receiver placement and configuration interface
- Integrate positioning solutions with visualization system

### Success Criteria
- [ ] Accurate positioning calculations using satellite data
- [ ] RTK mode shows centimeter-level accuracy improvements
- [ ] Error models demonstrate realistic positioning degradation
- [ ] Interactive receiver placement and configuration
- [ ] Real-time position updates synchronized with satellite movement
- [ ] Performance supports 10+ simultaneous receivers

---

## Technical Architecture

### Receiver System Structure
```
src/receiver/
├── __init__.py                    # Receiver module exports
├── receiver_manager.py            # Overall receiver coordination
├── positioning/
│   ├── positioning_engine.py     # Core positioning algorithms
│   ├── least_squares_solver.py   # Position calculation methods
│   ├── rtk_processor.py          # Real-Time Kinematic processing
│   └── kalman_filter.py          # State estimation and smoothing
├── receivers/
│   ├── base_station.py           # Reference station implementation
│   ├── rover_receiver.py         # Mobile receiver implementation
│   ├── standalone_receiver.py    # Single-point positioning
│   └── receiver_types.py         # Common receiver interfaces
├── errors/
│   ├── atmospheric_model.py      # Ionospheric and tropospheric delays
│   ├── multipath_model.py        # Signal reflection effects
│   ├── clock_error_model.py      # Receiver and satellite clock errors
│   └── noise_model.py            # Measurement noise simulation
├── visualization/
│   ├── receiver_renderer.py      # 3D receiver visualization
│   ├── position_plotter.py       # Position accuracy visualization
│   └── error_ellipse.py          # Uncertainty visualization
└── utils/
    ├── geodetic_utils.py         # Geodetic calculations
    └── statistics_utils.py       # Statistical analysis tools
```

---

## Detailed Implementation Tasks

### Task 5.1: Core Positioning Engine
**Priority:** Critical  
**Estimated Time:** 8-10 hours  
**File:** `src/receiver/positioning/positioning_engine.py`

#### Positioning Algorithm Implementation
```python
class PositioningEngine:
    """
    Core GNSS positioning engine with multiple solution methods.
    
    Capabilities:
    - Single Point Positioning (SPP) with 3-5 meter accuracy
    - Differential GPS (DGPS) with 1-3 meter accuracy
    - Real-Time Kinematic (RTK) with centimeter accuracy
    - Precise Point Positioning (PPP) for standalone precision
    """
    
    def __init__(self) -> None:
        self._least_squares_solver = LeastSquaresSolver()
        self._kalman_filter = ExtendedKalmanFilter()
        self._rtk_processor = RTKProcessor()
        self._atmosphere_model = AtmosphericModel()
        self._multipath_model = MultipathModel()
        
    def calculate_position(self, measurements: List[PseudorangeMeasurement],
                          receiver_type: ReceiverType) -> PositionSolution:
        """Calculate receiver position from satellite measurements."""
        
    def process_rtk_solution(self, rover_measurements: List[PseudorangeMeasurement],
                           base_corrections: List[DifferentialCorrection]) -> RTKSolution:
        """Process RTK solution using base station corrections."""
        
    def estimate_position_accuracy(self, solution: PositionSolution,
                                 geometry: SatelliteGeometry) -> AccuracyEstimate:
        """Estimate position accuracy based on satellite geometry and errors."""
```

#### Measurement Processing
```python
@dataclass
class PseudorangeMeasurement:
    """Raw pseudorange measurement from satellite."""
    satellite_id: str
    pseudorange: float              # meters
    carrier_phase: Optional[float]  # cycles (for RTK)
    signal_strength: float          # dB-Hz
    elevation_angle: float          # degrees
    azimuth_angle: float           # degrees
    timestamp: datetime            # measurement time

@dataclass
class PositionSolution:
    """Complete positioning solution."""
    position: Vec3                  # ECEF coordinates (meters)
    latitude: float                # degrees
    longitude: float               # degrees
    altitude: float                # meters above sea level
    position_accuracy: Vec3        # 1-sigma accuracy (m)
    velocity: Optional[Vec3]       # velocity vector (m/s)
    timestamp: datetime            # solution time
    solution_type: SolutionType    # SPP, DGPS, RTK_FLOAT, RTK_FIXED
    satellites_used: int           # number of satellites in solution
    geometric_dilution: float      # GDOP value
```

#### Least Squares Solver
```python
class LeastSquaresSolver:
    """Weighted least squares position solver."""
    
    def __init__(self) -> None:
        self._max_iterations = 10
        self._convergence_threshold = 0.001  # meters
        
    def solve_position(self, measurements: List[PseudorangeMeasurement],
                      satellite_positions: Dict[str, Vec3],
                      initial_position: Vec3) -> PositionSolution:
        """Iterative least squares solution for receiver position."""
        
    def calculate_design_matrix(self, measurements: List[PseudorangeMeasurement],
                              satellite_positions: Dict[str, Vec3],
                              receiver_position: Vec3) -> np.ndarray:
        """Calculate design matrix for least squares."""
        
    def calculate_weight_matrix(self, measurements: List[PseudorangeMeasurement]) -> np.ndarray:
        """Calculate measurement weight matrix based on signal quality."""
```

### Task 5.2: RTK Processing Implementation
**Priority:** High  
**Estimated Time:** 6-8 hours  
**File:** `src/receiver/positioning/rtk_processor.py`

#### Real-Time Kinematic Processing
```python
class RTKProcessor:
    """
    Real-Time Kinematic processing for centimeter accuracy.
    
    RTK Processing Steps:
    - Form double-difference observations
    - Resolve integer carrier phase ambiguities
    - Apply differential corrections from base station
    - Estimate position with centimeter precision
    """
    
    def __init__(self) -> None:
        self._ambiguity_resolver = AmbiguityResolver()
        self._baseline_processor = BaselineProcessor()
        self._quality_monitor = RTKQualityMonitor()
        
    def process_rtk_epoch(self, rover_obs: List[PseudorangeMeasurement],
                         base_obs: List[PseudorangeMeasurement],
                         baseline_length: float) -> RTKSolution:
        """Process single RTK epoch with rover and base observations."""
        
    def form_double_differences(self, rover_obs: List[PseudorangeMeasurement],
                              base_obs: List[PseudorangeMeasurement]) -> List[DoubleDifference]:
        """Form double-difference observations to eliminate errors."""
        
    def resolve_ambiguities(self, double_differences: List[DoubleDifference]) -> AmbiguitySet:
        """Resolve integer carrier phase ambiguities."""
        
    def estimate_baseline(self, resolved_observations: List[DoubleDifference],
                         ambiguities: AmbiguitySet) -> BaselineVector:
        """Estimate precise baseline from base to rover."""

@dataclass
class RTKSolution(PositionSolution):
    """Extended position solution with RTK-specific information."""
    baseline_vector: Vec3          # vector from base to rover (m)
    baseline_length: float         # baseline distance (m)
    ambiguity_status: AmbiguityStatus  # FIXED, FLOAT, or INVALID
    age_of_corrections: float      # seconds since base corrections
    rtk_ratio: float              # ambiguity resolution confidence
```

#### Ambiguity Resolution
```python
class AmbiguityResolver:
    """Integer ambiguity resolution for RTK positioning."""
    
    def __init__(self) -> None:
        self._lambda_method = LAMBDAMethod()
        self._ratio_threshold = 3.0  # minimum ratio for fixed solution
        
    def resolve_ambiguities(self, float_ambiguities: np.ndarray,
                          covariance_matrix: np.ndarray) -> AmbiguityResolution:
        """Resolve integer ambiguities using LAMBDA method."""
        
    def validate_resolution(self, candidates: List[AmbiguityCandidate]) -> AmbiguityStatus:
        """Validate ambiguity resolution using ratio test."""
        
    def decorrelate_ambiguities(self, ambiguities: np.ndarray,
                              covariance: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Decorrelate ambiguity estimates for better resolution."""
```

### Task 5.3: Receiver Types Implementation
**Priority:** High  
**Estimated Time:** 5-6 hours  
**Files:** `src/receiver/receivers/base_station.py`, `rover_receiver.py`, `standalone_receiver.py`

#### Base Station Implementation
```python
class BaseStation(ComponentInterface):
    """
    GNSS base station providing differential corrections.
    
    Functions:
    - Continuously track all visible satellites
    - Generate differential corrections for atmospheric errors
    - Broadcast corrections to rover receivers
    - Monitor data quality and integrity
    """
    
    def __init__(self, position: Vec3, station_id: str) -> None:
        self.position = position        # Known precise position (ECEF)
        self.station_id = station_id
        self._tracking_channels = {}    # Active satellite tracking
        self._corrections = {}          # Generated corrections
        self._data_logger = BaseStationLogger()
        
    def initialize(self, app: Application) -> bool:
        """Initialize base station with known position."""
        
    def update(self, delta_time: float) -> None:
        """Update tracking and generate corrections."""
        
    def process_satellite_data(self, satellite_states: List[SatelliteState]) -> None:
        """Process visible satellites and calculate corrections."""
        
    def generate_corrections(self) -> List[DifferentialCorrection]:
        """Generate differential corrections for rover receivers."""
        
    def get_station_health(self) -> StationHealth:
        """Get base station operational status."""

@dataclass
class DifferentialCorrection:
    """Differential correction data from base station."""
    satellite_id: str
    pseudorange_correction: float   # meters
    range_rate_correction: float    # m/s
    ionospheric_correction: float   # meters
    tropospheric_correction: float  # meters
    timestamp: datetime            # correction generation time
    correction_age: float          # seconds since measurement
```

#### Rover Receiver Implementation
```python
class RoverReceiver(ComponentInterface):
    """
    Mobile GNSS receiver with RTK capability.
    
    Capabilities:
    - Autonomous positioning (SPP mode)
    - Differential positioning (DGPS mode)
    - RTK positioning with base station corrections
    - Continuous position logging and tracking
    """
    
    def __init__(self, rover_id: str, receiver_config: ReceiverConfig) -> None:
        self.rover_id = rover_id
        self.config = receiver_config
        self._current_position: Optional[PositionSolution] = None
        self._positioning_engine = PositioningEngine()
        self._base_station_link: Optional[BaseStation] = None
        self._position_history: List[PositionSolution] = []
        
    def set_base_station(self, base_station: BaseStation) -> None:
        """Link rover to base station for RTK processing."""
        
    def process_positioning(self, satellite_states: List[SatelliteState]) -> PositionSolution:
        """Calculate position using available satellites."""
        
    def update_position_display(self) -> None:
        """Update 3D visualization of rover position."""
        
    def get_position_accuracy(self) -> AccuracyEstimate:
        """Get current position accuracy estimate."""
```

#### Standalone Receiver Implementation
```python
class StandaloneReceiver(ComponentInterface):
    """
    Single-point positioning receiver without differential corrections.
    
    Characteristics:
    - Uses only satellite signals for positioning
    - Typical accuracy: 3-5 meters (95% confidence)
    - Affected by atmospheric delays and satellite errors
    - Most common type for consumer applications
    """
    
    def __init__(self, receiver_id: str) -> None:
        self.receiver_id = receiver_id
        self._positioning_engine = PositioningEngine()
        self._error_models = [AtmosphericModel(), MultipathModel(), NoiseModel()]
        
    def calculate_spp_solution(self, satellite_states: List[SatelliteState]) -> PositionSolution:
        """Calculate Single Point Position solution."""
        
    def apply_error_models(self, measurements: List[PseudorangeMeasurement]) -> List[PseudorangeMeasurement]:
        """Apply realistic error models to measurements."""
```

### Task 5.4: Error Modeling System
**Priority:** Medium  
**Estimated Time:** 4-5 hours  
**Files:** `src/receiver/errors/atmospheric_model.py`, `multipath_model.py`, `clock_error_model.py`

#### Atmospheric Error Models
```python
class AtmosphericModel:
    """
    Model ionospheric and tropospheric signal delays.
    
    Error Sources:
    - Ionospheric delay: Variable with solar activity (1-20m error)
    - Tropospheric delay: Weather-dependent (0.1-2.5m error)
    - Seasonal and diurnal variations
    - Elevation angle dependency
    """
    
    def __init__(self) -> None:
        self._ionosphere_model = KlobucharModel()
        self._troposphere_model = SaastamoinenModel()
        
    def calculate_ionospheric_delay(self, satellite_pos: Vec3, receiver_pos: Vec3,
                                  frequency: float, time: datetime) -> float:
        """Calculate ionospheric delay in meters."""
        
    def calculate_tropospheric_delay(self, elevation_angle: float, 
                                   receiver_altitude: float,
                                   weather_params: WeatherParameters) -> float:
        """Calculate tropospheric delay in meters."""
        
    def get_total_atmospheric_delay(self, satellite_state: SatelliteState,
                                  receiver_position: Vec3,
                                  signal_frequency: float) -> float:
        """Get combined atmospheric delay for satellite signal."""

@dataclass
class WeatherParameters:
    """Weather conditions affecting tropospheric delay."""
    temperature: float      # Celsius
    pressure: float        # millibars
    humidity: float        # percentage (0-100)
```

#### Multipath Error Model
```python
class MultipathModel:
    """
    Model signal reflection and multipath effects.
    
    Multipath Sources:
    - Ground reflections
    - Building and structure reflections
    - Vehicle body reflections
    - Varying with receiver environment and satellite geometry
    """
    
    def __init__(self) -> None:
        self._environment_type = EnvironmentType.OPEN_SKY
        self._multipath_parameters = MultipathParameters()
        
    def calculate_multipath_error(self, elevation_angle: float,
                                 azimuth_angle: float,
                                 environment: EnvironmentType) -> float:
        """Calculate multipath-induced range error."""
        
    def set_environment(self, env_type: EnvironmentType) -> None:
        """Set receiver environment affecting multipath."""
        
    def get_multipath_variance(self, satellite_geometry: SatelliteGeometry) -> float:
        """Get expected multipath error variance."""

class EnvironmentType(Enum):
    """Different receiver environments with varying multipath."""
    OPEN_SKY = "open_sky"           # Minimal multipath
    SUBURBAN = "suburban"           # Moderate multipath
    URBAN = "urban"                # High multipath
    URBAN_CANYON = "urban_canyon"   # Severe multipath
```

### Task 5.5: Receiver Visualization
**Priority:** Medium  
**Estimated Time:** 3-4 hours  
**Files:** `src/receiver/visualization/receiver_renderer.py`, `position_plotter.py`

#### 3D Receiver Rendering
```python
class ReceiverRenderer:
    """
    3D visualization of GNSS receivers and positioning results.
    
    Visualization Features:
    - Different models for base station, rover, standalone
    - Position accuracy ellipses and error visualization
    - Real-time position tracking and trail display
    - Signal quality and satellite count indicators
    """
    
    def __init__(self, graphics_manager: GraphicsManager) -> None:
        self._graphics = graphics_manager
        self._receiver_models: Dict[str, NodePath] = {}
        self._position_trails: Dict[str, LineSegs] = {}
        self._accuracy_ellipses: Dict[str, NodePath] = {}
        
    def create_receiver_model(self, receiver: ComponentInterface) -> NodePath:
        """Create 3D model for receiver based on type."""
        
    def update_receiver_position(self, receiver_id: str, 
                               solution: PositionSolution) -> None:
        """Update receiver position and accuracy visualization."""
        
    def show_accuracy_ellipse(self, receiver_id: str, 
                            accuracy: AccuracyEstimate) -> None:
        """Display position accuracy ellipse around receiver."""
        
    def update_position_trail(self, receiver_id: str, 
                            positions: List[Vec3]) -> None:
        """Update position history trail visualization."""
```

#### Position Accuracy Visualization
```python
class PositionPlotter:
    """Statistical visualization of position accuracy and errors."""
    
    def __init__(self) -> None:
        self._position_samples: Dict[str, List[Vec3]] = {}
        self._error_statistics: Dict[str, ErrorStatistics] = {}
        
    def add_position_sample(self, receiver_id: str, position: Vec3, 
                          true_position: Vec3) -> None:
        """Add position sample for accuracy analysis."""
        
    def calculate_error_statistics(self, receiver_id: str) -> ErrorStatistics:
        """Calculate position error statistics."""
        
    def create_accuracy_plot(self, receiver_id: str) -> AccuracyPlot:
        """Create accuracy visualization plot."""

@dataclass
class ErrorStatistics:
    """Position error statistical analysis."""
    mean_error: Vec3           # mean position error (m)
    rms_error: float          # RMS position error (m)
    cep_50: float             # 50% circular error probability (m)
    cep_95: float             # 95% circular error probability (m)
    vertical_accuracy: float   # 95% vertical accuracy (m)
    sample_count: int         # number of position samples
```

---

## Integration Points

### Satellite System Integration
- **Satellite Positions:** Use real-time satellite states for positioning
- **Visibility Data:** Filter satellites based on line-of-sight calculations
- **Signal Quality:** Use satellite elevation and signal strength estimates
- **Time Synchronization:** Position updates synchronized with satellite updates

### Graphics System Integration
- **Receiver Models:** 3D visualization of different receiver types
- **Position Trails:** Real-time position tracking and history display
- **Accuracy Visualization:** Error ellipses and uncertainty indicators
- **User Interaction:** Click-to-place receiver positioning

### Event System Integration
- **Position Events:** `receiver.position.updated`, `receiver.accuracy.changed`
- **RTK Events:** `rtk.fixed`, `rtk.float`, `rtk.lost`
- **Configuration Events:** `receiver.placed`, `receiver.configured`
- **Error Events:** `positioning.error`, `base_station.offline`

---

## Performance Optimization

### Positioning Performance
```python
class PositioningOptimizer:
    """Optimize positioning calculations for real-time performance."""
    
    def __init__(self) -> None:
        self._update_rates = {
            'base_station': 1.0,      # 1 Hz update rate
            'rover_rtk': 5.0,         # 5 Hz for RTK
            'standalone': 1.0         # 1 Hz for SPP
        }
        
    def schedule_position_updates(self, receivers: List[ComponentInterface]) -> None:
        """Schedule position updates based on receiver type and priority."""
        
    def batch_satellite_calculations(self, receivers: List[ComponentInterface],
                                   satellites: List[SatelliteState]) -> None:
        """Batch satellite visibility and range calculations."""
```

### Memory Management
- **Position History Limiting:** Maintain bounded position trail history
- **Measurement Buffering:** Efficient storage of raw measurements
- **Solution Caching:** Cache common calculations across receivers
- **Error Model Optimization:** Pre-compute atmospheric correction tables

---

## Testing Strategy

### Unit Tests Required
- [ ] Positioning algorithm accuracy (known position verification)
- [ ] RTK processing with synthetic base/rover data
- [ ] Error model behavior under various conditions
- [ ] Receiver type functionality and configuration
- [ ] Coordinate transformations and geodetic calculations

### Integration Tests Required
- [ ] Position updates with satellite movement
- [ ] Base station to rover communication simulation
- [ ] Graphics integration with position visualization
- [ ] Performance with multiple simultaneous receivers

### Accuracy Verification
- [ ] Single point positioning within 5m accuracy
- [ ] RTK positioning within 10cm accuracy (when fixed)
- [ ] Error models produce realistic degradation
- [ ] Statistical analysis matches expected performance

---

## Success Metrics

### Functional Requirements
- **SPP Accuracy:** 3-5 meter accuracy (95% confidence)
- **RTK Accuracy:** <10cm accuracy when fixed solution achieved
- **Update Rate:** Real-time position updates at 1-5 Hz
- **Reliability:** Robust operation with partial satellite coverage

### Performance Requirements
- **Processing Time:** <50ms per position solution
- **Memory Usage:** <50MB additional for receiver system
- **Scalability:** Support 10+ simultaneous receivers
- **Responsiveness:** UI updates within 100ms of position change

---

## Handoff to Phase 06

### Positioning Foundation Complete
- All receiver types operational with realistic accuracy
- RTK processing provides centimeter-level precision
- Error models demonstrate positioning limitations
- Real-time position updates integrated with visualization

### UI Integration Ready
- Receiver placement and configuration APIs defined
- Position display and accuracy visualization operational
- Event system provides position updates for UI components
- Performance optimized for interactive user controls

---

**References:**
- Previous Phase: `planning/phases/PHASE_04_SATELLITE_SYSTEM.md`
- Next Phase: `planning/phases/PHASE_06_UI_CONTROLS.md`
- Master Plan: `planning/MASTER_IMPLEMENTATION_PLAN.md`
- Integration Map: `planning/active_memo/INTEGRATION_MAP.md`

**Line Count:** 499/500