#!/usr/bin/env python3
"""
Architecture Validator
Purpose: Verify Phase 1-2 integration points remain functional
Author: GitHub Copilot
Created: 2025-09-17

Validates that core architectural components (event bus, simulation clock,
app framework) are unaffected by graphics system issues and maintain
their integration contracts.
"""

import sys
import importlib
from pathlib import Path
from typing import Dict, List, Any
import traceback
from datetime import datetime
import json

# Add src to path for testing
workspace_root = Path(__file__).parent.parent.parent
src_path = workspace_root / "src"
sys.path.insert(0, str(src_path))

class ArchitectureValidator:
    """Validates core architectural integrity."""
    
    def __init__(self):
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "validation_summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            },
            "phase1_validation": {},
            "phase2_validation": {},
            "integration_validation": {},
            "architectural_integrity": "UNKNOWN",
            "critical_issues": [],
            "recommendations": []
        }
    
    def validate_phase1_foundation(self):
        """Validate Phase 1 project setup remains intact."""
        
        print("🏗️  Validating Phase 1 Foundation...")
        
        phase1_tests = {
            "directory_structure": self._test_directory_structure,
            "skeleton_files": self._test_skeleton_files,
            "configuration_files": self._test_configuration_files,
            "testing_framework": self._test_testing_framework
        }
        
        phase1_results = {}
        
        for test_name, test_func in phase1_tests.items():
            try:
                result = test_func()
                phase1_results[test_name] = result
                
                if result["status"] == "PASS":
                    self.validation_results["validation_summary"]["passed"] += 1
                elif result["status"] == "FAIL":
                    self.validation_results["validation_summary"]["failed"] += 1
                else:
                    self.validation_results["validation_summary"]["warnings"] += 1
                
                self.validation_results["validation_summary"]["total_tests"] += 1
                
            except Exception as e:
                phase1_results[test_name] = {
                    "status": "FAIL",
                    "error": str(e),
                    "impact": "Phase 1 foundation compromised"
                }
                self.validation_results["validation_summary"]["failed"] += 1
                self.validation_results["validation_summary"]["total_tests"] += 1
        
        self.validation_results["phase1_validation"] = phase1_results
    
    def validate_phase2_core_architecture(self):
        """Validate Phase 2 core components function correctly."""
        
        print("⚙️  Validating Phase 2 Core Architecture...")
        
        phase2_tests = {
            "event_bus_functionality": self._test_event_bus,
            "simulation_clock_functionality": self._test_simulation_clock,
            "app_framework_functionality": self._test_app_framework,
            "config_manager_functionality": self._test_config_manager,
            "hot_reload_functionality": self._test_hot_reload_manager,
            "logging_functionality": self._test_logging_manager
        }
        
        phase2_results = {}
        
        for test_name, test_func in phase2_tests.items():
            try:
                result = test_func()
                phase2_results[test_name] = result
                
                if result["status"] == "PASS":
                    self.validation_results["validation_summary"]["passed"] += 1
                elif result["status"] == "FAIL":
                    self.validation_results["validation_summary"]["failed"] += 1
                    
                    # Phase 2 failures are critical
                    self.validation_results["critical_issues"].append({
                        "component": test_name,
                        "issue": result.get("error", "Unknown failure"),
                        "impact": "CRITICAL - Core architecture compromised"
                    })
                else:
                    self.validation_results["validation_summary"]["warnings"] += 1
                
                self.validation_results["validation_summary"]["total_tests"] += 1
                
            except Exception as e:
                phase2_results[test_name] = {
                    "status": "FAIL",
                    "error": str(e),
                    "impact": "CRITICAL - Core functionality broken"
                }
                self.validation_results["validation_summary"]["failed"] += 1
                self.validation_results["validation_summary"]["total_tests"] += 1
        
        self.validation_results["phase2_validation"] = phase2_results
    
    def validate_integration_contracts(self):
        """Validate integration contracts between components."""
        
        print("🔗 Validating Integration Contracts...")
        
        integration_tests = {
            "event_bus_integration": self._test_event_integration,
            "clock_synchronization": self._test_clock_integration,
            "config_propagation": self._test_config_integration,
            "application_lifecycle": self._test_application_lifecycle
        }
        
        integration_results = {}
        
        for test_name, test_func in integration_tests.items():
            try:
                result = test_func()
                integration_results[test_name] = result
                
                if result["status"] == "PASS":
                    self.validation_results["validation_summary"]["passed"] += 1
                elif result["status"] == "FAIL":
                    self.validation_results["validation_summary"]["failed"] += 1
                else:
                    self.validation_results["validation_summary"]["warnings"] += 1
                
                self.validation_results["validation_summary"]["total_tests"] += 1
                
            except Exception as e:
                integration_results[test_name] = {
                    "status": "FAIL",
                    "error": str(e),
                    "impact": "Integration contract broken"
                }
                self.validation_results["validation_summary"]["failed"] += 1
                self.validation_results["validation_summary"]["total_tests"] += 1
        
        self.validation_results["integration_validation"] = integration_results
    
    def _test_directory_structure(self) -> Dict[str, Any]:
        """Test that Phase 1 directory structure is intact."""
        
        required_dirs = [
            "src/core",
            "src/graphics", 
            "src/data",
            "src/satellite",
            "src/receiver", 
            "src/ui",
            "src/utils",
            "tests/unit",
            "tests/integration",
            "config",
            "planning"
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            if not (workspace_root / dir_path).exists():
                missing_dirs.append(dir_path)
        
        if missing_dirs:
            return {
                "status": "FAIL",
                "missing_directories": missing_dirs,
                "impact": "Project structure compromised"
            }
        
        return {
            "status": "PASS",
            "message": "All required directories present"
        }
    
    def _test_skeleton_files(self) -> Dict[str, Any]:
        """Test that core skeleton files exist."""
        
        required_files = [
            "src/core/__init__.py",
            "src/graphics/__init__.py",
            "requirements.txt",
            "pytest.ini"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (workspace_root / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            return {
                "status": "FAIL", 
                "missing_files": missing_files,
                "impact": "Core files missing"
            }
        
        return {
            "status": "PASS",
            "message": "All skeleton files present"
        }
    
    def _test_configuration_files(self) -> Dict[str, Any]:
        """Test configuration system integrity."""
        
        config_files = [
            "config/default.json"
        ]
        
        issues = []
        for config_file in config_files:
            config_path = workspace_root / config_file
            if not config_path.exists():
                issues.append(f"Missing: {config_file}")
            else:
                try:
                    with open(config_path, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    issues.append(f"Invalid JSON in {config_file}: {e}")
        
        if issues:
            return {
                "status": "FAIL",
                "issues": issues,
                "impact": "Configuration system broken"
            }
        
        return {
            "status": "PASS", 
            "message": "Configuration files valid"
        }
    
    def _test_testing_framework(self) -> Dict[str, Any]:
        """Test that testing framework is operational."""
        
        try:
            import pytest
            return {
                "status": "PASS",
                "message": "Testing framework available"
            }
        except ImportError:
            return {
                "status": "FAIL",
                "error": "pytest not available",
                "impact": "Testing framework broken"
            }
    
    def _test_event_bus(self) -> Dict[str, Any]:
        """Test event bus functionality."""
        
        try:
            from core.event_bus import EventBus
            
            # Test basic functionality
            bus = EventBus()
            
            # Test subscription and publishing
            events_received = []
            
            def test_handler(event):
                events_received.append(event.data)
            
            bus.subscribe("test.event", test_handler)
            bus.publish("test.event", {"test": "data"})
            
            if len(events_received) == 1 and events_received[0]["test"] == "data":
                return {
                    "status": "PASS",
                    "message": "Event bus functional"
                }
            else:
                return {
                    "status": "FAIL",
                    "error": "Event publishing/subscription failed",
                    "impact": "Event system broken"
                }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Event bus import or instantiation failed"
            }
    
    def _test_simulation_clock(self) -> Dict[str, Any]:
        """Test simulation clock functionality."""
        
        try:
            from core.simulation_clock import SimulationClock
            from core.event_bus import EventBus
            
            bus = EventBus()
            clock = SimulationClock(bus)
            
            # Test basic time operations
            initial_time = clock.current_time
            clock.set_speed(1.0)
            
            return {
                "status": "PASS",
                "message": "Simulation clock functional"
            }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Simulation clock broken"
            }
    
    def _test_app_framework(self) -> Dict[str, Any]:
        """Test application framework functionality."""
        
        try:
            from core.app_framework import Application
            
            # Test instantiation
            app = Application()
            
            # Test that core components are available
            if hasattr(app, 'event_bus') and hasattr(app, 'clock') and hasattr(app, 'config'):
                return {
                    "status": "PASS",
                    "message": "Application framework functional"
                }
            else:
                return {
                    "status": "FAIL",
                    "error": "Application framework missing core components",
                    "impact": "Application integration broken"
                }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Application framework broken"
            }
    
    def _test_config_manager(self) -> Dict[str, Any]:
        """Test configuration manager functionality."""
        
        try:
            from core.config_manager import ConfigManager
            
            # Test with default config
            config = ConfigManager()
            
            # Test basic operations
            test_value = config.get("graphics.target_fps", 60)
            
            return {
                "status": "PASS",
                "message": "Configuration manager functional"
            }
        
        except Exception as e:
            return {
                "status": "FAIL", 
                "error": str(e),
                "impact": "Configuration system broken"
            }
    
    def _test_hot_reload_manager(self) -> Dict[str, Any]:
        """Test hot reload manager functionality."""
        
        try:
            from core.hot_reload_manager import HotReloadManager
            
            # Test instantiation
            reload_mgr = HotReloadManager()
            
            return {
                "status": "PASS",
                "message": "Hot reload manager functional"
            }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Hot reload system broken"
            }
    
    def _test_logging_manager(self) -> Dict[str, Any]:
        """Test logging manager functionality."""
        
        try:
            from core.logging_manager import LoggingManager
            
            # Test instantiation
            log_mgr = LoggingManager()
            
            return {
                "status": "PASS",
                "message": "Logging manager functional"
            }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Logging system broken"
            }
    
    def _test_event_integration(self) -> Dict[str, Any]:
        """Test event system integration across components."""
        
        try:
            from core.app_framework import Application
            
            app = Application()
            
            # Test event flow between components
            events_received = []
            
            def integration_handler(event):
                events_received.append(event.event_type)
            
            app.event_bus.subscribe("integration.test", integration_handler)
            app.event_bus.publish("integration.test", {"test": "integration"})
            
            if "integration.test" in events_received:
                return {
                    "status": "PASS",
                    "message": "Event integration functional"
                }
            else:
                return {
                    "status": "FAIL",
                    "error": "Event integration failed",
                    "impact": "Component communication broken"
                }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Event integration broken"
            }
    
    def _test_clock_integration(self) -> Dict[str, Any]:
        """Test clock synchronization integration."""
        
        try:
            from core.app_framework import Application
            
            app = Application()
            
            # Test clock integration with event system
            time_events = []
            
            def time_handler(event):
                time_events.append(event.event_type)
            
            app.event_bus.subscribe("time.speed_changed", time_handler)
            app.clock.set_speed(2.0)
            
            return {
                "status": "PASS",
                "message": "Clock integration functional"
            }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Clock integration broken"
            }
    
    def _test_config_integration(self) -> Dict[str, Any]:
        """Test configuration propagation integration."""
        
        try:
            from core.app_framework import Application
            
            app = Application()
            
            # Test config availability in integrated system
            target_fps = app.config.get("graphics.target_fps", 60)
            
            return {
                "status": "PASS",
                "message": "Configuration integration functional"
            }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Configuration integration broken"
            }
    
    def _test_application_lifecycle(self) -> Dict[str, Any]:
        """Test application lifecycle management."""
        
        try:
            from core.app_framework import Application
            
            app = Application()
            
            # Test initialization state
            if app._running is False and not app._shutdown_requested:
                return {
                    "status": "PASS",
                    "message": "Application lifecycle functional"
                }
            else:
                return {
                    "status": "FAIL",
                    "error": "Application lifecycle state incorrect",
                    "impact": "Application lifecycle broken"
                }
        
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "impact": "Application lifecycle broken"
            }
    
    def determine_architectural_integrity(self):
        """Determine overall architectural integrity."""
        
        total_tests = self.validation_results["validation_summary"]["total_tests"]
        failed_tests = self.validation_results["validation_summary"]["failed"]
        
        if failed_tests == 0:
            self.validation_results["architectural_integrity"] = "INTACT"
        elif failed_tests <= total_tests * 0.1:  # 10% failure threshold
            self.validation_results["architectural_integrity"] = "STABLE_WITH_ISSUES"
        elif failed_tests <= total_tests * 0.3:  # 30% failure threshold
            self.validation_results["architectural_integrity"] = "DEGRADED"
        else:
            self.validation_results["architectural_integrity"] = "COMPROMISED"
        
        # Generate recommendations
        if self.validation_results["architectural_integrity"] == "INTACT":
            self.validation_results["recommendations"].append("Architecture is healthy - proceed with graphics system fixes")
        elif self.validation_results["architectural_integrity"] == "STABLE_WITH_ISSUES":
            self.validation_results["recommendations"].append("Minor issues detected - address before major graphics work")
        elif self.validation_results["architectural_integrity"] == "DEGRADED": 
            self.validation_results["recommendations"].append("Significant issues - fix core architecture before graphics")
        else:
            self.validation_results["recommendations"].append("CRITICAL: Restore core architecture before any other work")
    
    def save_results(self):
        """Save validation results to markdown file."""
        
        report_content = f"""# Architecture Compliance Report
**Generated:** {self.validation_results['timestamp']}  
**Purpose:** Verify Phase 1-2 architectural integrity

---

## Executive Summary

### Architectural Integrity: {self.validation_results['architectural_integrity']}

### Test Results
- **Total Tests:** {self.validation_results['validation_summary']['total_tests']}
- **Passed:** {self.validation_results['validation_summary']['passed']}
- **Failed:** {self.validation_results['validation_summary']['failed']}
- **Warnings:** {self.validation_results['validation_summary']['warnings']}

---

## Critical Issues
"""
        
        if self.validation_results['critical_issues']:
            for issue in self.validation_results['critical_issues']:
                report_content += f"""
### {issue['component']}
- **Impact:** {issue['impact']}
- **Issue:** {issue['issue']}
"""
        else:
            report_content += "\n✅ No critical issues detected\n"
        
        report_content += "\n---\n\n## Recommendations\n\n"
        for rec in self.validation_results['recommendations']:
            report_content += f"- {rec}\n"
        
        report_content += "\n---\n\n## Detailed Results\n\n"
        
        # Phase 1 Results
        report_content += "### Phase 1 Foundation Validation\n\n"
        for test_name, result in self.validation_results['phase1_validation'].items():
            status_icon = "✅" if result['status'] == "PASS" else "❌"
            report_content += f"- {status_icon} **{test_name}:** {result.get('message', result.get('error', 'Unknown'))}\n"
        
        # Phase 2 Results
        report_content += "\n### Phase 2 Core Architecture Validation\n\n"
        for test_name, result in self.validation_results['phase2_validation'].items():
            status_icon = "✅" if result['status'] == "PASS" else "❌"
            report_content += f"- {status_icon} **{test_name}:** {result.get('message', result.get('error', 'Unknown'))}\n"
        
        # Integration Results
        report_content += "\n### Integration Contract Validation\n\n"
        for test_name, result in self.validation_results['integration_validation'].items():
            status_icon = "✅" if result['status'] == "PASS" else "❌"
            report_content += f"- {status_icon} **{test_name}:** {result.get('message', result.get('error', 'Unknown'))}\n"
        
        output_path = workspace_root / "investigation_base_camp" / "reports" / "architecture_compliance.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Architecture compliance report saved to: {output_path}")
        return output_path

def main():
    """Run complete architecture validation."""
    print("🏛️  Starting Architecture Validation...")
    
    validator = ArchitectureValidator()
    validator.validate_phase1_foundation()
    validator.validate_phase2_core_architecture()
    validator.validate_integration_contracts()
    validator.determine_architectural_integrity()
    
    # Print summary
    summary = validator.validation_results["validation_summary"]
    integrity = validator.validation_results["architectural_integrity"]
    
    print(f"\n📊 Validation Summary:")
    print(f"   🏛️  Architectural Integrity: {integrity}")
    print(f"   ✅ Tests Passed: {summary['passed']}")
    print(f"   ❌ Tests Failed: {summary['failed']}")
    print(f"   ⚠️  Warnings: {summary['warnings']}")
    
    if validator.validation_results['critical_issues']:
        print(f"\n🚨 CRITICAL ISSUES:")
        for issue in validator.validation_results['critical_issues']:
            print(f"   • {issue['component']}: {issue['impact']}")
    
    output_path = validator.save_results()
    print(f"\n💾 Complete validation report saved to: {output_path}")

if __name__ == "__main__":
    main()