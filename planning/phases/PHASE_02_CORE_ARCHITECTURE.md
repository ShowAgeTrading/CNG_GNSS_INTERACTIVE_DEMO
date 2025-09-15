# Phase 02: Core Architecture Implementation
**Version:** 1.0  
**Created:** 2025-09-15  
**Author:** GitHub Copilot  
**Purpose:** Build event-driven application framework with hot-reload support  
**Estimated Duration:** 2-3 days  
**Complexity:** Medium  

---

## Phase Overview

### Objectives
- Implement thread-safe event bus for decoupled communication
- Create simulation clock with time control (play/pause/speed/reverse)
- Build main application framework with lifecycle management
- Establish hot-reload infrastructure for plugins and modules
- Create configuration management system
- Implement basic logging and error handling

### Success Criteria
- [ ] Event bus supports pub/sub with thread safety
- [ ] Simulation clock controls time flow for all components
- [ ] Application starts, runs, and shuts down gracefully
- [ ] Hot-reload works for marked modules without restart
- [ ] Configuration loads from JSON with validation
- [ ] All core components have 90%+ test coverage

---

## Detailed Implementation Plan

### Task 2.1: Event Bus Implementation
**Priority:** Critical  
**Estimated Time:** 4-6 hours  
**File:** `src/core/event_bus.py`

#### Technical Specification
```python
class EventBus:
    """
    Thread-safe event bus supporting:
    - Multiple subscribers per event type
    - Event filtering and priorities
    - Async event handling
    - Performance monitoring
    """
    
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[EventSubscription]] = {}
        self._lock: threading.RLock = threading.RLock()
        self._event_history: List[Event] = []
        self._performance_stats: Dict[str, float] = {}
    
    def subscribe(self, event_type: str, callback: Callable, 
                  priority: int = 0, filter_func: Optional[Callable] = None) -> str:
        """Subscribe with priority and optional filtering."""
        
    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove subscription by ID."""
        
    def publish(self, event_type: str, data: Any = None, 
                source: str = "unknown") -> None:
        """Publish event to all matching subscribers."""
        
    def publish_async(self, event_type: str, data: Any = None) -> None:
        """Publish event asynchronously for performance."""
```

#### Event Types to Support
- `app.startup` - Application initialization
- `app.shutdown` - Application termination
- `time.play` - Simulation time started
- `time.pause` - Simulation time paused
- `time.step` - Single time step completed
- `satellite.selected` - Satellite selection changed
- `receiver.moved` - Receiver position updated
- `ui.refresh` - UI requires update
- `error.occurred` - Error condition detected
- `plugin.loaded` - Plugin hot-loaded
- `plugin.unloaded` - Plugin unloaded

#### Implementation Steps
1. Create EventSubscription dataclass for subscriber metadata
2. Implement thread-safe subscriber management with RLock
3. Add event publishing with priority ordering
4. Implement event filtering mechanisms
5. Add performance monitoring and statistics
6. Create async publishing for non-blocking operations

#### Testing Requirements
- Multiple subscribers on same event type
- Thread safety with concurrent publish/subscribe
- Event filtering works correctly
- Performance acceptable for 100+ events/second
- Memory usage remains bounded with event history

### Task 2.2: Simulation Clock Implementation
**Priority:** Critical  
**Estimated Time:** 3-4 hours  
**File:** `src/core/simulation_clock.py`

#### Technical Specification
```python
class SimulationClock:
    """
    Simulation time controller supporting:
    - Variable speed playback (0.1x to 100x)
    - Reverse time simulation
    - Precise time stepping
    - Time synchronization across components
    """
    
    def __init__(self, event_bus: EventBus, start_time: datetime = None) -> None:
        self._event_bus = event_bus
        self._current_time: datetime = start_time or datetime.utcnow()
        self._real_start_time: float = time.time()
        self._is_playing: bool = False
        self._speed_multiplier: float = 1.0
        self._step_size: timedelta = timedelta(seconds=1)
        
    def play(self) -> None:
        """Start time simulation."""
        
    def pause(self) -> None:
        """Pause time simulation."""
        
    def step_forward(self, steps: int = 1) -> None:
        """Advance time by specified steps."""
        
    def step_backward(self, steps: int = 1) -> None:
        """Reverse time by specified steps."""
        
    def set_speed(self, multiplier: float) -> None:
        """Set playback speed (0.1x to 100x)."""
        
    def set_time(self, new_time: datetime) -> None:
        """Jump to specific time."""
        
    @property
    def current_time(self) -> datetime:
        """Get current simulation time."""
```

#### Time Events to Publish
- `time.changed` - When simulation time updates
- `time.speed_changed` - When playback speed changes
- `time.direction_changed` - When forward/reverse changes
- `time.jump` - When time jumps to specific moment

#### Implementation Steps
1. Create precise time tracking with real-time synchronization
2. Implement variable speed playback calculations
3. Add reverse time simulation support
4. Create time step management for discrete updates
5. Integrate with event bus for time notifications
6. Add time persistence for session save/load

#### Testing Requirements
- Time accuracy within 1ms over 1-hour simulation
- Speed changes take effect immediately
- Reverse simulation works correctly
- Multiple components stay synchronized
- Performance impact minimal (<1ms per update)

### Task 2.3: Application Framework Implementation
**Priority:** Critical  
**Estimated Time:** 4-5 hours  
**File:** `src/core/app_framework.py`

#### Technical Specification
```python
class Application:
    """
    Main application framework managing:
    - Lifecycle (startup/running/shutdown)
    - Component registration and initialization
    - Error handling and recovery
    - Performance monitoring
    """
    
    def __init__(self, config_path: str = "config/app_config.json") -> None:
        self.event_bus = EventBus()
        self.clock = SimulationClock(self.event_bus)
        self.config = ConfigManager(config_path)
        self._components: Dict[str, ComponentInterface] = {}
        self._shutdown_requested: bool = False
        
    def register_component(self, name: str, component: ComponentInterface) -> None:
        """Register component for lifecycle management."""
        
    def startup(self) -> None:
        """Initialize all components and start main loop."""
        
    def run(self) -> None:
        """Main application loop."""
        
    def shutdown(self) -> None:
        """Graceful shutdown of all components."""
```

#### Component Interface
```python
class ComponentInterface:
    """Base interface for all application components."""
    
    def initialize(self, app: 'Application') -> bool:
        """Initialize component with app reference."""
        
    def update(self, delta_time: float) -> None:
        """Update component each frame."""
        
    def shutdown(self) -> None:
        """Cleanup component resources."""
        
    @property
    def name(self) -> str:
        """Component name for identification."""
```

#### Implementation Steps
1. Create component registration and lifecycle management
2. Implement startup sequence with dependency ordering
3. Add main loop with fixed timestep updates
4. Create graceful shutdown with resource cleanup
5. Add error handling and component failure recovery
6. Integrate performance monitoring and frame rate control

#### Testing Requirements
- Components initialize in correct dependency order
- Main loop maintains target frame rate (60 FPS)
- Shutdown completes within 5 seconds
- Component failures don't crash application
- Memory leaks prevented during startup/shutdown cycles

### Task 2.4: Hot-Reload Infrastructure
**Priority:** High  
**Estimated Time:** 5-6 hours  
**File:** `src/core/hot_reload_manager.py`

#### Technical Specification
```python
class HotReloadManager:
    """
    Hot-reload support for plugins and marked modules:
    - File system watching for changes
    - Module reloading with state preservation
    - Dependency tracking and cascading reloads
    - Error handling for failed reloads
    """
    
    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._watchers: Dict[str, FileSystemWatcher] = {}
        self._loaded_modules: Dict[str, ModuleInfo] = {}
        self._persistent_state: Dict[str, Any] = {}
        
    def watch_directory(self, path: str, patterns: List[str]) -> None:
        """Watch directory for file changes."""
        
    def reload_module(self, module_path: str) -> bool:
        """Reload specific module with state preservation."""
        
    def preserve_state(self, module_name: str, state: Dict[str, Any]) -> None:
        """Store state before module reload."""
        
    def restore_state(self, module_name: str) -> Dict[str, Any]:
        """Restore state after module reload."""
```

#### Hot-Reload Markers
```python
# Module-level markers for hot-reload behavior
__hot_reload__ = True  # Enable hot-reload for this module
__persistent_state__ = ["user_preferences", "session_data"]  # State to preserve
__reload_dependencies__ = ["other_module"]  # Modules to reload together
```

#### Implementation Steps
1. Create file system watching with configurable patterns
2. Implement module reloading with importlib machinery
3. Add state preservation/restoration mechanisms
4. Create dependency tracking for cascading reloads
5. Add error handling for failed reload attempts
6. Integrate with event bus for reload notifications

#### Testing Requirements
- File changes detected within 100ms
- Module reloads complete within 1 second
- State preservation works across reload cycles
- Failed reloads don't break application
- Dependency cascading works correctly

### Task 2.5: Configuration Management
**Priority:** High  
**Estimated Time:** 2-3 hours  
**File:** `src/core/config_manager.py`

#### Technical Specification
```python
class ConfigManager:
    """
    Configuration management with:
    - JSON schema validation
    - Environment variable support
    - Runtime configuration updates
    - Default value handling
    """
    
    def __init__(self, config_path: str) -> None:
        self._config_path = config_path
        self._config_data: Dict[str, Any] = {}
        self._schema: Dict[str, Any] = {}
        self._validators: Dict[str, Callable] = {}
        
    def load_config(self, schema_path: str = None) -> None:
        """Load configuration with optional schema validation."""
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support."""
        
    def set(self, key: str, value: Any) -> None:
        """Set configuration value with validation."""
        
    def save(self) -> None:
        """Save current configuration to file."""
```

#### Configuration Structure
```json
{
    "app": {
        "title": "CNG GNSS Interactive Demo",
        "version": "1.0.0",
        "log_level": "INFO",
        "performance_monitoring": true
    },
    "graphics": {
        "target_fps": 60,
        "vsync": true,
        "anti_aliasing": 4
    },
    "simulation": {
        "default_time_speed": 1.0,
        "time_step_ms": 16.67,
        "max_satellites": 100
    },
    "plugins": {
        "auto_reload": true,
        "watch_directories": ["src/plugins"],
        "load_on_startup": []
    }
}
```

#### Implementation Steps
1. Create JSON loading with schema validation
2. Add dot notation key access (e.g., "app.title")
3. Implement environment variable overrides
4. Add runtime configuration change notifications
5. Create configuration file watching for live updates

#### Testing Requirements
- Invalid JSON handled gracefully
- Schema validation catches configuration errors
- Environment variables override file values
- Configuration changes trigger appropriate events
- Default values provided for missing keys

### Task 2.6: Logging and Error Handling
**Priority:** Medium  
**Estimated Time:** 2-3 hours  
**File:** `src/core/logging_manager.py`

#### Technical Specification
```python
class LoggingManager:
    """
    Centralized logging with:
    - Multiple output destinations (file, console, UI)
    - Log level filtering and formatting
    - Performance impact monitoring
    - Error aggregation and reporting
    """
    
    def __init__(self, config: ConfigManager, event_bus: EventBus) -> None:
        self._config = config
        self._event_bus = event_bus
        self._loggers: Dict[str, logging.Logger] = {}
        self._error_counts: Dict[str, int] = {}
        
    def get_logger(self, name: str) -> logging.Logger:
        """Get or create logger for specific module."""
        
    def setup_logging(self) -> None:
        """Configure logging based on configuration."""
        
    def log_performance(self, operation: str, duration: float) -> None:
        """Log performance metrics for operations."""
```

#### Implementation Steps
1. Set up Python logging with appropriate formatters
2. Create file rotation and size management
3. Add event bus integration for UI log display
4. Implement performance logging and monitoring
5. Create error aggregation and reporting

#### Testing Requirements
- Log files created and rotated correctly
- Performance impact minimal (<1ms per log entry)
- Error aggregation works without memory leaks
- Log levels filter correctly
- UI integration displays logs in real-time

---

## Integration Points

### Event Bus Integration
- All components must subscribe to relevant events
- Event publishing should be non-blocking where possible
- Event history available for debugging
- Performance monitoring for event processing

### Clock Integration  
- All time-dependent components subscribe to time events
- Time synchronization maintained across components
- Simulation state persists across pause/resume cycles

### Hot-Reload Integration
- Components mark hot-reloadable sections appropriately
- State preservation works for UI and simulation data
- Error recovery prevents application crashes during reload

---

## Testing Strategy

### Unit Tests Required
- [ ] EventBus thread safety with concurrent operations
- [ ] SimulationClock time accuracy and synchronization
- [ ] Application startup/shutdown lifecycle
- [ ] HotReloadManager module reloading
- [ ] ConfigManager validation and persistence
- [ ] LoggingManager performance and formatting

### Integration Tests Required
- [ ] Event flow between components
- [ ] Time synchronization across multiple components
- [ ] Configuration changes affecting multiple systems
- [ ] Hot-reload preserving application state
- [ ] Error propagation and handling

### Performance Tests Required
- [ ] Event bus handles 1000+ events/second
- [ ] Clock updates maintain 60 FPS target
- [ ] Hot-reload completes within 1 second
- [ ] Memory usage remains stable over time
- [ ] Application startup time under 3 seconds

---

## Success Metrics

### Functional Requirements
- Event bus delivers events to all subscribers within 1ms
- Simulation clock maintains time accuracy within 0.1%
- Application achieves 60 FPS with basic components loaded
- Hot-reload preserves 95% of marked state correctly
- Configuration validation catches 100% of schema violations

### Performance Requirements
- Memory usage under 100MB for core components
- CPU usage under 10% when idle
- Event processing overhead under 0.1ms per event
- Configuration access under 0.01ms per call
- Log entry creation under 0.1ms per entry

### Reliability Requirements
- Zero crashes during normal operation
- Graceful handling of all configuration errors
- Recovery from hot-reload failures within 1 second
- Component failure isolation (one failure doesn't crash app)
- 99.9% uptime during extended operation

---

## Risk Assessment

### High-Risk Areas
1. **Thread Safety in Event Bus**
   - Risk: Race conditions causing data corruption
   - Mitigation: Comprehensive threading tests, deadlock detection

2. **Hot-Reload State Management**
   - Risk: State loss during module reload
   - Mitigation: Conservative state preservation, rollback mechanisms

### Medium-Risk Areas
1. **Performance Degradation**
   - Risk: Event bus becomes bottleneck under load
   - Mitigation: Performance profiling, async processing

2. **Configuration Complexity**
   - Risk: Invalid configurations causing startup failures
   - Mitigation: Robust validation, fallback defaults

---

## Handoff to Phase 03

### Deliverables Completed
- Fully functional event-driven architecture
- Time simulation system with precise control
- Application framework ready for component integration
- Hot-reload infrastructure for development productivity
- Configuration and logging systems operational

### Integration Points for Graphics
- Event bus ready for graphics events (render, viewport changes)
- Simulation clock provides time for animations and updates
- Application framework ready to register graphics components
- Configuration system supports graphics settings
- Hot-reload enables rapid graphics development iteration

### Performance Baselines Established
- Event processing: <1ms per event
- Time updates: 60 FPS capability
- Memory usage: <100MB baseline
- Startup time: <3 seconds
- Hot-reload time: <1 second

---

**References:**
- Previous Phase: `planning/phases/PHASE_01_PROJECT_SETUP.md`
- Next Phase: `planning/phases/PHASE_03_GRAPHICS_ENGINE.md`
- Master Plan: `planning/MASTER_IMPLEMENTATION_PLAN.md`
- Template: `planning/templates/UNIVERSAL_CODE_TEMPLATE.md`

**Line Count:** 498/500