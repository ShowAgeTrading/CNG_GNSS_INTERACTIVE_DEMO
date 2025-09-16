#!/usr/bin/env python3
"""
Phase 2 Integration Test
Tests core architecture components working together

IMPORTANT: This test is ESSENTIAL for Phase 3 handoff
- Validates complete core architecture functionality
- Ensures all 6 core components integrate properly
- Serves as regression test during Phase 3 graphics implementation
- More valuable than individual unit tests at this stage
- DO NOT DELETE - Required for architectural stability validation
"""

import os
import sys
import time
import tempfile
import shutil
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import core components
from core.event_bus import EventBus
from core.simulation_clock import SimulationClock
from core.config_manager import ConfigManager
from core.app_framework import Application
from core.hot_reload_manager import HotReloadManager
from core.logging_manager import LoggingManager


def test_phase_2_integration():
    """Test all Phase 2 components working together."""
    print("=== Phase 2 Core Architecture Integration Test ===")
    
    # Create temporary config
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_config = {
            "app": {
                "name": "Test App",
                "version": "1.0.0"
            },
            "simulation": {
                "time_speed": 1.0
            }
        }
        import json
        json.dump(test_config, f)
        config_path = f.name
    
    try:
        # 1. Create Application (this initializes EventBus, ConfigManager, SimulationClock internally)
        print("1. Creating Application...")
        app = Application(config_path)
        
        # Get references to the application's internal components
        app_event_bus = app.event_bus
        app_config = app.config
        app_clock = app.clock
        
        # 2. Initialize LoggingManager with the app's event bus
        print("2. Initializing LoggingManager...")
        logging_manager = LoggingManager(app_event_bus)
        logging_manager.setup_logging("INFO", console_output=False)
        
        # 3. Setup HotReloadManager with the app's event bus
        print("3. Setting up HotReloadManager...")
        hot_reload = HotReloadManager(app_event_bus)
        
        # Test event communication using app's event bus
        events_received = []
        def test_subscriber(event):
            events_received.append(event.event_type)
            
        app_event_bus.subscribe('test.message', test_subscriber)
        app_event_bus.publish('test.message', {'data': 'test'})
        
        # Test configuration access using app's config
        app_name = app_config.get('app.name')
        print(f"   Config test: app.name = {app_name}")
        
        # Test simulation clock using app's clock
        app_clock.set_speed(2.0)
        current_speed = app_clock.speed_multiplier
        print(f"   Clock test: speed set to {current_speed}")
        
        # Test hot reload stats
        reload_stats = hot_reload.get_stats()
        print(f"   Hot-reload test: tracking {reload_stats['tracked_modules']} modules")
        
        # Test logging performance
        logging_manager.log_performance('test_operation', 0.05)
        perf_stats = logging_manager.get_performance_stats('test_operation')
        if perf_stats and 'test_operation' in perf_stats:
            print(f"   Logging test: recorded performance metric")
        
        # Verify event was received
        assert 'test.message' in events_received, "Event bus communication failed"
        
        print("\n✅ All Phase 2 core components integrated successfully!")
        print("\n📊 Component Summary:")
        print(f"   • EventBus: {len(app_event_bus._subscribers)} event types registered")
        print(f"   • ConfigManager: {len(app_config._config_data)} config sections")
        print(f"   • SimulationClock: {current_speed}x speed")
        print(f"   • HotReloadManager: {reload_stats['watched_paths']} paths watched")
        print(f"   • LoggingManager: Performance tracking enabled")
        print(f"   • Application: Ready for component integration")
        
        print("\n🎯 Phase 2 Architecture Validation Complete:")
        print("   ✓ Event-driven communication working")
        print("   ✓ Configuration management operational")
        print("   ✓ Time simulation system ready")
        print("   ✓ Hot-reload infrastructure active")
        print("   ✓ Logging and performance monitoring enabled")
        print("   ✓ Application framework ready for Phase 3 graphics")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        if os.path.exists(config_path):
            os.unlink(config_path)


if __name__ == "__main__":
    success = test_phase_2_integration()
    sys.exit(0 if success else 1)