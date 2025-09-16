# Phase 07: Data Integration and File Processing
**Version:** 1.0  
**Created:** 2025-09-15  
**Author:** GitHub Copilot  
**Purpose:** Integrate real NMEA data, error modeling, and export functionality  
**Estimated Duration:** 3-4 days  
**Complexity:** Medium-Large  

---

## Phase Overview

### Objectives
- Implement NMEA file parsing and playback for recorded GNSS data
- Create realistic error modeling affecting positioning accuracy
- Build comprehensive data export functionality (CSV, JSON, KML)
- Develop configuration management for data sources and processing
- Integrate file-based simulation with real-time positioning
- Prepare infrastructure for future NTRIP live data (disabled initially)

### Success Criteria
- [ ] NMEA files load and playback through simulation timeline
- [ ] Error models demonstrably affect positioning accuracy
- [ ] Export functions preserve complete session data
- [ ] Configuration system manages data sources and processing parameters
- [ ] File data integrates seamlessly with existing simulation components
- [ ] Performance supports large NMEA files (1GB+) without blocking UI

---

## Technical Architecture

### Data System Structure
```
src/data/
├── __init__.py                    # Data module exports
├── data_manager.py               # Main data coordination
├── parsers/
│   ├── nmea_parser.py           # NMEA sentence parsing
│   ├── rinex_parser.py          # RINEX observation files
│   ├── sp3_parser.py            # Precise orbit files
│   └── parser_factory.py        # Parser selection and creation
├── processors/
│   ├── data_preprocessor.py     # Data cleaning and validation
│   ├── time_synchronizer.py     # Time alignment across data sources
│   ├── quality_checker.py       # Data quality assessment
│   └── interpolator.py          # Data interpolation and smoothing
├── exporters/
│   ├── csv_exporter.py          # CSV format export
│   ├── json_exporter.py         # JSON format export
│   ├── kml_exporter.py          # Google Earth KML export
│   └── export_manager.py        # Export coordination
├── models/
│   ├── atmospheric_effects.py   # Advanced atmospheric modeling
│   ├── multipath_effects.py     # Detailed multipath simulation
│   ├── receiver_noise.py        # Realistic receiver noise
│   └── satellite_errors.py      # Satellite clock and orbit errors
└── sources/
    ├── file_source.py           # File-based data sources
    ├── ntrip_source.py          # NTRIP client (disabled/placeholder)
    └── simulation_source.py     # Generated simulation data
```

---

## Detailed Implementation Tasks

### Task 7.1: NMEA Data Parser Implementation
**Priority:** Critical  
**Estimated Time:** 5-6 hours  
**File:** `src/data/parsers/nmea_parser.py`

#### NMEA Parser Core
```python
class NMEAParser:
    """
    Comprehensive NMEA sentence parser supporting all major message types.
    
    Supported Messages:
    - GGA: Global Positioning System Fix Data
    - RMC: Recommended Minimum Navigation Information  
    - GSA: GPS DOP and Active Satellites
    - GSV: Satellites in View
    - VTG: Track Made Good and Ground Speed
    - GLL: Geographic Position (Latitude/Longitude)
    """
    
    def __init__(self) -> None:
        self._sentence_handlers: Dict[str, Callable] = {}
        self._statistics = ParsingStatistics()
        self._validation_enabled = True
        self._register_handlers()
        
    def parse_file(self, file_path: str) -> ParsedNMEAData:
        """Parse complete NMEA file and return structured data."""
        
    def parse_sentence(self, nmea_sentence: str) -> Optional[NMEAMessage]:
        """Parse single NMEA sentence."""
        
    def validate_checksum(self, sentence: str) -> bool:
        """Validate NMEA sentence checksum."""
        
    def get_parsing_statistics(self) -> ParsingStatistics:
        """Get statistics about parsed data quality."""

@dataclass
class NMEAMessage:
    """Base class for all NMEA message types."""
    message_type: str
    timestamp: datetime
    raw_sentence: str
    checksum_valid: bool

@dataclass
class GGAMessage(NMEAMessage):
    """GGA: Global Positioning System Fix Data."""
    latitude: float
    longitude: float
    altitude: float
    fix_quality: int              # 0=invalid, 1=GPS, 2=DGPS, 4=RTK fixed, 5=RTK float
    satellites_used: int
    hdop: float                   # Horizontal dilution of precision
    age_of_dgps: Optional[float]  # Age of DGPS corrections (seconds)
    dgps_station_id: Optional[str]

@dataclass
class ParsedNMEAData:
    """Complete NMEA file parsing results."""
    positions: List[GGAMessage]
    satellite_info: List[GSVMessage]
    timing_info: List[RMCMessage]
    quality_metrics: ParsingStatistics
    time_range: Tuple[datetime, datetime]
    total_sentences: int
```

#### Advanced NMEA Processing
```python
class NMEAProcessor:
    """Advanced NMEA data processing and analysis."""
    
    def __init__(self) -> None:
        self._data_validator = NMEADataValidator()
        self._time_synchronizer = TimeSynchronizer()
        self._quality_assessor = DataQualityAssessor()
        
    def process_nmea_session(self, parsed_data: ParsedNMEAData) -> ProcessedSession:
        """Process raw NMEA data into usable simulation format."""
        
    def detect_data_gaps(self, positions: List[GGAMessage]) -> List[DataGap]:
        """Identify gaps in position data."""
        
    def assess_position_quality(self, positions: List[GGAMessage]) -> QualityReport:
        """Assess overall quality of position data."""
        
    def synchronize_timestamps(self, messages: List[NMEAMessage]) -> List[NMEAMessage]:
        """Synchronize timestamps across different message types."""
```

### Task 7.2: Error Model Implementation
**Priority:** High  
**Estimated Time:** 6-8 hours  
**Files:** `src/data/models/atmospheric_effects.py`, `multipath_effects.py`

#### Advanced Atmospheric Modeling
```python
class AtmosphericEffectsModel:
    """
    Detailed atmospheric error modeling for realistic positioning degradation.
    
    Models:
    - Ionospheric delay with solar activity correlation
    - Tropospheric delay with weather dependency
    - Seasonal and diurnal variations
    - Geographic and elevation angle dependencies
    """
    
    def __init__(self) -> None:
        self._ionosphere_model = IonosphereModel()
        self._troposphere_model = TroposphereModel()
        self._solar_activity = SolarActivityModel()
        self._weather_model = WeatherModel()
        
    def apply_atmospheric_errors(self, position: Vec3, 
                                satellite_positions: List[Vec3],
                                timestamp: datetime) -> List[float]:
        """Apply atmospheric delays to satellite ranges."""
        
    def get_ionospheric_correction(self, satellite_elevation: float,
                                  satellite_azimuth: float,
                                  frequency: float,
                                  solar_flux: float) -> float:
        """Calculate ionospheric delay correction."""
        
    def get_tropospheric_correction(self, elevation_angle: float,
                                   receiver_height: float,
                                   weather_params: WeatherParameters) -> float:
        """Calculate tropospheric delay correction."""

class IonosphereModel:
    """Detailed ionospheric delay modeling."""
    
    def __init__(self) -> None:
        self._klobuchar_coefficients = KlobucharCoefficients()
        self._solar_cycle_model = SolarCycleModel()
        
    def calculate_delay(self, user_position: Vec3, satellite_position: Vec3,
                       timestamp: datetime, frequency: float) -> float:
        """Calculate ionospheric delay in meters."""
        
    def get_vertical_delay(self, solar_flux_index: float, 
                          local_time: float) -> float:
        """Calculate vertical ionospheric delay."""
```

#### Multipath Error Modeling
```python
class MultipathEffectsModel:
    """
    Realistic multipath error simulation based on environment and geometry.
    
    Environment Types:
    - Open sky: Minimal multipath (0.1-0.5m errors)
    - Suburban: Moderate multipath (0.5-2m errors)  
    - Urban: High multipath (1-5m errors)
    - Urban canyon: Severe multipath (2-10m errors)
    """
    
    def __init__(self) -> None:
        self._environment_models: Dict[EnvironmentType, EnvironmentModel] = {}
        self._reflection_calculator = ReflectionCalculator()
        self._setup_environment_models()
        
    def apply_multipath_errors(self, satellite_positions: List[Vec3],
                              receiver_position: Vec3,
                              environment: EnvironmentType) -> List[float]:
        """Apply multipath errors to satellite measurements."""
        
    def calculate_reflection_delay(self, direct_path: float,
                                  reflected_path: float,
                                  reflection_coefficient: float) -> float:
        """Calculate multipath delay from reflection geometry."""
        
    def get_multipath_variance(self, elevation_angle: float,
                              environment: EnvironmentType) -> float:
        """Get expected multipath error variance."""

class EnvironmentModel:
    """Environment-specific multipath characteristics."""
    
    def __init__(self, env_type: EnvironmentType) -> None:
        self.environment_type = env_type
        self.reflection_surfaces: List[ReflectionSurface] = []
        self.base_noise_level: float = 0.0
        self.elevation_dependency: float = 1.0
        
    def generate_multipath_error(self, satellite_geometry: SatelliteGeometry) -> float:
        """Generate realistic multipath error for given geometry."""
```

### Task 7.3: Data Export System
**Priority:** Medium  
**Estimated Time:** 4-5 hours  
**Files:** `src/data/exporters/csv_exporter.py`, `json_exporter.py`, `kml_exporter.py`

#### Export Manager
```python
class ExportManager:
    """
    Coordinate data export across multiple formats and data types.
    
    Export Capabilities:
    - Position data with accuracy estimates
    - Satellite visibility and signal strength
    - Error model contributions
    - Session configuration and metadata
    - Time-stamped measurement logs
    """
    
    def __init__(self) -> None:
        self._exporters: Dict[ExportFormat, DataExporter] = {}
        self._register_exporters()
        
    def export_session_data(self, session_data: SessionData,
                           format_type: ExportFormat,
                           output_path: str,
                           options: ExportOptions) -> bool:
        """Export complete session data in specified format."""
        
    def export_position_track(self, positions: List[PositionSolution],
                             format_type: ExportFormat,
                             output_path: str) -> bool:
        """Export position track for external analysis."""
        
    def export_satellite_data(self, satellite_states: List[SatelliteState],
                             visibility_data: List[VisibilityData],
                             format_type: ExportFormat,
                             output_path: str) -> bool:
        """Export satellite visibility and signal data."""

class ExportFormat(Enum):
    """Supported export formats."""
    CSV = "csv"
    JSON = "json"
    KML = "kml"
    GPX = "gpx"
    NMEA = "nmea"
```

#### CSV Export Implementation
```python
class CSVExporter(DataExporter):
    """Export data to CSV format for spreadsheet analysis."""
    
    def __init__(self) -> None:
        self._delimiter = ","
        self._include_headers = True
        
    def export_positions(self, positions: List[PositionSolution],
                        output_path: str) -> bool:
        """Export position data to CSV with accuracy information."""
        
    def export_satellite_visibility(self, visibility_data: List[VisibilityData],
                                   output_path: str) -> bool:
        """Export satellite visibility data to CSV."""
        
    def export_error_contributions(self, error_data: List[ErrorContribution],
                                  output_path: str) -> bool:
        """Export error model contributions to CSV."""

# CSV Format Examples:
# positions.csv:
# timestamp,latitude,longitude,altitude,accuracy_horizontal,accuracy_vertical,solution_type,satellites_used
# 2025-09-15T12:00:00Z,-33.8688,151.2093,25.4,2.3,4.1,RTK_FIXED,12

# satellites.csv:  
# timestamp,satellite_id,elevation,azimuth,signal_strength,used_in_solution
# 2025-09-15T12:00:00Z,G01,45.2,123.4,-142.5,true
```

#### KML Export for Google Earth
```python
class KMLExporter(DataExporter):
    """Export data to KML format for Google Earth visualization."""
    
    def __init__(self) -> None:
        self._include_altitude = True
        self._color_by_accuracy = True
        
    def export_position_track(self, positions: List[PositionSolution],
                             output_path: str) -> bool:
        """Export position track as KML placemark path."""
        
    def export_receiver_locations(self, receivers: List[ReceiverInfo],
                                 output_path: str) -> bool:
        """Export receiver locations as KML placemarks."""
        
    def create_accuracy_visualization(self, positions: List[PositionSolution]) -> str:
        """Create KML elements showing position accuracy."""
```

### Task 7.4: Configuration Management
**Priority:** Medium  
**Estimated Time:** 3-4 hours  
**File:** `src/data/data_manager.py`

#### Data Source Configuration
```python
class DataManager(ComponentInterface):
    """
    Central coordination of all data sources and processing.
    
    Data Sources:
    - NMEA files: Recorded GNSS data playback
    - Simulation: Generated satellite and receiver data
    - Configuration: Error model parameters and settings
    - Future: NTRIP streams (infrastructure prepared)
    """
    
    def __init__(self, event_bus: EventBus, config: ConfigManager) -> None:
        self._event_bus = event_bus
        self._config = config
        self._active_sources: Dict[str, DataSource] = {}
        self._processors: Dict[str, DataProcessor] = {}
        self._current_session: Optional[DataSession] = None
        
    def initialize(self, app: Application) -> bool:
        """Initialize data management system."""
        
    def load_nmea_file(self, file_path: str) -> bool:
        """Load NMEA file and prepare for playback."""
        
    def start_data_playback(self, playback_speed: float = 1.0) -> None:
        """Start data playback synchronized with simulation time."""
        
    def apply_error_models(self, enable_errors: Dict[str, bool]) -> None:
        """Enable/disable specific error models."""
        
    def export_session_data(self, export_config: ExportConfig) -> bool:
        """Export current session data."""

@dataclass
class DataSession:
    """Complete data session information."""
    session_id: str
    start_time: datetime
    end_time: datetime
    data_sources: List[DataSourceInfo]
    receivers: List[ReceiverConfig]
    error_models: Dict[str, ErrorModelConfig]
    export_history: List[ExportRecord]
```

#### Configuration Schema
```json
{
  "data_sources": {
    "nmea_files": {
      "enabled": true,
      "default_directory": "assets/data/nmea",
      "auto_detect_format": true,
      "validation_level": "strict"
    },
    "ntrip": {
      "enabled": false,
      "placeholder": "Future NTRIP integration"
    }
  },
  "error_models": {
    "atmospheric": {
      "enabled": true,
      "ionosphere_model": "klobuchar",
      "troposphere_model": "saastamoinen",
      "solar_activity_level": "medium"
    },
    "multipath": {
      "enabled": true,
      "default_environment": "suburban",
      "elevation_masking": 5.0
    },
    "receiver_noise": {
      "enabled": true,
      "pseudorange_noise": 0.3,
      "carrier_phase_noise": 0.01
    }
  },
  "export": {
    "default_format": "csv",
    "include_accuracy": true,
    "timestamp_format": "iso8601",
    "coordinate_system": "wgs84"
  }
}
```

### Task 7.5: Data Quality and Validation
**Priority:** Medium  
**Estimated Time:** 2-3 hours  
**File:** `src/data/processors/quality_checker.py`

#### Data Quality Assessment
```python
class DataQualityChecker:
    """
    Assess and report on data quality for loaded datasets.
    
    Quality Metrics:
    - Data completeness and gap analysis
    - Position accuracy consistency
    - Satellite visibility patterns
    - Time synchronization quality
    - Error model realism validation
    """
    
    def __init__(self) -> None:
        self._quality_thresholds = QualityThresholds()
        self._statistics_calculator = StatisticsCalculator()
        
    def assess_nmea_quality(self, parsed_data: ParsedNMEAData) -> QualityReport:
        """Comprehensive quality assessment of NMEA data."""
        
    def check_position_consistency(self, positions: List[PositionSolution]) -> ConsistencyReport:
        """Check position data for outliers and inconsistencies."""
        
    def validate_error_realism(self, positions: List[PositionSolution],
                              error_contributions: List[ErrorContribution]) -> ValidationReport:
        """Validate that error models produce realistic degradation."""

@dataclass
class QualityReport:
    """Data quality assessment results."""
    overall_quality: QualityLevel    # EXCELLENT, GOOD, FAIR, POOR
    completeness_score: float        # 0-1, percentage of expected data present
    accuracy_consistency: float      # 0-1, consistency of accuracy estimates
    temporal_coverage: float         # 0-1, temporal completeness
    satellite_diversity: float       # 0-1, variety of satellites used
    identified_issues: List[QualityIssue]
    recommendations: List[str]
```

---

## Integration Points

### Time System Integration
- **Synchronized Playback:** NMEA data playback synchronized with simulation clock
- **Time Control:** Play/pause/speed controls affect data playback
- **Time Jumping:** Scrubbing to specific times loads appropriate data
- **Historical Data:** Support for reverse time playback with NMEA data

### Receiver System Integration
- **Position Override:** NMEA positions can override calculated positions
- **Error Application:** Error models applied to both NMEA and calculated positions
- **Accuracy Comparison:** Compare NMEA reported accuracy with model predictions
- **RTK Integration:** NMEA RTK data used to validate RTK algorithms

### UI Integration
- **File Loading:** UI controls for NMEA file selection and loading
- **Error Controls:** UI toggles for enabling/disabling error models
- **Export Interface:** UI dialogs for data export configuration
- **Quality Display:** Real-time display of data quality metrics

---

## Performance Optimization

### Large File Handling
```python
class LargeFileProcessor:
    """Handle large NMEA files without blocking UI."""
    
    def __init__(self) -> None:
        self._chunk_size = 10000  # Process 10k sentences at a time
        self._background_processor = BackgroundProcessor()
        
    def process_large_file(self, file_path: str) -> AsyncIterator[ProcessingProgress]:
        """Process large file in background with progress updates."""
        
    def stream_file_data(self, file_path: str, 
                        time_window: Tuple[datetime, datetime]) -> Iterator[NMEAMessage]:
        """Stream relevant data for specific time window."""
```

### Memory Management
- **Streaming Processing:** Large files processed in chunks
- **Data Caching:** Intelligent caching of frequently accessed data
- **Memory Bounds:** Automatic cleanup of old data outside time window
- **Background Processing:** Non-blocking file processing with progress updates

---

## Testing Strategy

### Unit Tests Required
- [ ] NMEA parser accuracy with standard test sentences
- [ ] Error model behavior under various conditions
- [ ] Export format correctness and data integrity
- [ ] Configuration loading and validation
- [ ] Data quality assessment accuracy

### Integration Tests Required
- [ ] NMEA playback integration with simulation timeline
- [ ] Error models affecting positioning calculations
- [ ] Export functions preserving complete session data
- [ ] Large file processing without UI blocking

### Data Validation Tests
- [ ] Parse standard NMEA test files correctly
- [ ] Error models produce expected degradation patterns
- [ ] Export/import round-trip preserves data accuracy
- [ ] Quality assessment identifies known data issues

---

## Success Metrics

### Functional Requirements
- **File Support:** Parse 95%+ of standard NMEA sentences correctly
- **Error Realism:** Error models produce realistic positioning degradation
- **Export Completeness:** Exported data preserves all essential information
- **Performance:** Process 1GB NMEA files without UI blocking

### User Experience Requirements
- **File Loading:** NMEA files load and begin playback within 10 seconds
- **Error Visualization:** Error effects clearly visible in position displays
- **Export Speed:** Data export completes within 30 seconds for typical sessions
- **Quality Feedback:** Data quality issues clearly communicated to user

---

## Handoff to Phase 08

### Data Foundation Complete
- NMEA file processing and playback operational
- Realistic error modeling affecting positioning accuracy
- Comprehensive export functionality for external analysis
- Configuration system managing data sources and processing

### Plugin System Preparation
- Data processing pipeline ready for plugin extensions
- Export system extensible for new output formats
- Error modeling framework ready for custom error models
- Configuration system supports plugin-specific settings

---

**References:**
- Previous Phase: `planning/phases/PHASE_06_UI_CONTROLS.md`
- Next Phase: `planning/phases/PHASE_08_PLUGIN_SYSTEM.md`
- Master Plan: `planning/MASTER_IMPLEMENTATION_PLAN.md`
- Integration Map: `planning/active_memo/INTEGRATION_MAP.md`

**Line Count:** 499/500