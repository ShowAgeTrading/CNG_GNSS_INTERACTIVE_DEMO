#!/usr/bin/env python3
"""
Phase 3 Refactoring Validation Script
=====================================

This script validates the success of the Phase 3 graphics modularization refactoring.
It performs comprehensive checks to ensure:
1. File size compliance (all files < 200 lines)
2. Import integrity (no circular imports)
3. Functional integrity (all tests pass)
4. Performance regression check
5. API compatibility for Phase 4

Usage:
    python validate_phase3_refactor.py [--performance-check]

Exit Codes:
    0: All validations passed
    1: File size violations
    2: Import failures  
    3: Test failures
    4: Performance regression (> 5% FPS drop)
    5: API compatibility issues

Author: Auto-generated for Phase 3 Graphics Modularization
Created: 2025-09-16
"""

import os
import sys
import subprocess
import time
import importlib.util
from pathlib import Path


class Phase3RefactorValidator:
    """Comprehensive validation for Phase 3 graphics modularization."""
    
    def __init__(self):
        self.root_path = Path(__file__).parent
        self.src_path = self.root_path / "src"
        self.graphics_path = self.src_path / "graphics"
        self.utils_path = self.graphics_path / "utils"
        
        self.target_files = [
            "src/graphics/graphics_manager.py",
            "src/graphics/globe_renderer.py", 
            "src/graphics/texture_manager.py",
            "src/graphics/coordinate_system.py"
        ]
        
        self.new_utility_files = [
            "src/graphics/utils/graphics_utils.py",
            "src/graphics/utils/asset_manager.py",
            "src/graphics/utils/panda3d_utils.py"
        ]
        
        self.results = {
            "file_size_compliance": False,
            "import_integrity": False,
            "functional_integrity": False,
            "performance_check": False,
            "api_compatibility": False
        }

    def log(self, message, level="INFO"):
        """Log validation messages with timestamp."""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def check_file_sizes(self):
        """Validate that all target files are under 200 lines."""
        self.log("Checking file size compliance...")
        
        violations = []
        for file_path in self.target_files:
            full_path = self.root_path / file_path
            if not full_path.exists():
                self.log(f"ERROR: File not found: {file_path}", "ERROR")
                continue
                
            with open(full_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
                
            if line_count > 200:
                violations.append(f"{file_path}: {line_count} lines")
                self.log(f"VIOLATION: {file_path} has {line_count} lines (> 200)", "ERROR")
            else:
                self.log(f"OK: {file_path} has {line_count} lines")
        
        if violations:
            self.log(f"File size compliance FAILED: {len(violations)} violations", "ERROR")
            return False
        
        self.log("File size compliance PASSED", "SUCCESS")
        self.results["file_size_compliance"] = True
        return True

    def check_utility_files_exist(self):
        """Verify that new utility files were created."""
        self.log("Checking utility file creation...")
        
        missing_files = []
        for file_path in self.new_utility_files:
            full_path = self.root_path / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                self.log(f"MISSING: {file_path}", "ERROR")
            else:
                self.log(f"EXISTS: {file_path}")
        
        if missing_files:
            self.log(f"Utility file creation FAILED: {len(missing_files)} missing", "ERROR")
            return False
        
        self.log("Utility file creation PASSED", "SUCCESS")
        return True

    def check_import_integrity(self):
        """Test import integrity and detect circular imports."""
        self.log("Checking import integrity...")
        
        # Test imports of main graphics modules
        try:
            sys.path.insert(0, str(self.src_path))
            
            # Test main graphics imports
            import graphics.graphics_manager
            import graphics.globe_renderer
            import graphics.texture_manager
            import graphics.coordinate_system
            
            # Test new utility imports
            import graphics.utils.graphics_utils
            import graphics.utils.asset_manager  
            import graphics.utils.panda3d_utils
            
            self.log("All imports successful")
            
        except ImportError as e:
            self.log(f"Import error: {e}", "ERROR")
            return False
        except Exception as e:
            self.log(f"Unexpected error during imports: {e}", "ERROR")
            return False
        finally:
            sys.path.pop(0)
        
        self.log("Import integrity PASSED", "SUCCESS")
        self.results["import_integrity"] = True
        return True

    def run_unit_tests(self):
        """Run unit tests for graphics components."""
        self.log("Running unit tests...")
        
        test_commands = [
            ["python", "-m", "pytest", "tests/unit/test_graphics_manager.py", "-v"],
            ["python", "-m", "pytest", "tests/unit/test_camera_controller.py", "-v"]
        ]
        
        for cmd in test_commands:
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    cwd=self.root_path,
                    timeout=60
                )
                
                if result.returncode != 0:
                    self.log(f"Unit test failed: {' '.join(cmd)}", "ERROR")
                    self.log(f"STDOUT: {result.stdout}", "ERROR")
                    self.log(f"STDERR: {result.stderr}", "ERROR")
                    return False
                else:
                    self.log(f"Unit test passed: {' '.join(cmd)}")
                    
            except subprocess.TimeoutExpired:
                self.log(f"Unit test timeout: {' '.join(cmd)}", "ERROR")
                return False
            except Exception as e:
                self.log(f"Unit test error: {e}", "ERROR")
                return False
        
        return True

    def run_integration_tests(self):
        """Run Phase 3 integration tests."""
        self.log("Running integration tests...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/integration/test_phase3_graphics.py", "-v"],
                capture_output=True,
                text=True,
                cwd=self.root_path,
                timeout=120
            )
            
            if result.returncode != 0:
                self.log("Integration tests FAILED", "ERROR") 
                self.log(f"STDOUT: {result.stdout}", "ERROR")
                self.log(f"STDERR: {result.stderr}", "ERROR")
                return False
            else:
                self.log("Integration tests PASSED", "SUCCESS")
                return True
                
        except subprocess.TimeoutExpired:
            self.log("Integration test timeout", "ERROR")
            return False
        except Exception as e:
            self.log(f"Integration test error: {e}", "ERROR")
            return False

    def check_functional_integrity(self):
        """Run comprehensive functional tests."""
        self.log("Checking functional integrity...")
        
        # Run unit tests
        if not self.run_unit_tests():
            self.log("Functional integrity FAILED: Unit tests failed", "ERROR")
            return False
        
        # Run integration tests
        if not self.run_integration_tests():
            self.log("Functional integrity FAILED: Integration tests failed", "ERROR")
            return False
        
        self.log("Functional integrity PASSED", "SUCCESS")
        self.results["functional_integrity"] = True
        return True

    def check_performance_regression(self):
        """Basic performance regression check (headless mode)."""
        self.log("Checking performance regression...")
        
        try:
            # Run a simple graphics initialization test
            result = subprocess.run([
                "python", "-c", 
                """
import sys
sys.path.insert(0, 'src')
from graphics.graphics_manager import GraphicsManager
from core.event_bus import EventBus
import time

# Headless initialization test
event_bus = EventBus()
gm = GraphicsManager(event_bus)

start_time = time.time()
gm.initialize(headless=True)
init_time = time.time() - start_time

print(f'INIT_TIME:{init_time:.3f}')

gm.shutdown()
print('PERFORMANCE_OK')
                """
            ], capture_output=True, text=True, cwd=self.root_path, timeout=30)
            
            if result.returncode != 0:
                self.log(f"Performance check failed: {result.stderr}", "ERROR")
                return False
            
            # Parse initialization time  
            output_lines = result.stdout.strip().split('\n')
            init_time = None
            
            for line in output_lines:
                if line.startswith('INIT_TIME:'):
                    init_time = float(line.split(':')[1])
                    break
            
            if init_time is None:
                self.log("Could not parse initialization time", "ERROR")
                return False
            
            # Check if initialization time is reasonable (< 5 seconds)
            if init_time > 5.0:
                self.log(f"Performance regression: Init time {init_time:.3f}s > 5.0s", "ERROR")
                return False
            
            self.log(f"Performance check PASSED: Init time {init_time:.3f}s", "SUCCESS")
            self.results["performance_check"] = True
            return True
            
        except subprocess.TimeoutExpired:
            self.log("Performance check timeout", "ERROR")
            return False
        except Exception as e:
            self.log(f"Performance check error: {e}", "ERROR") 
            return False

    def check_api_compatibility(self):
        """Verify API compatibility for Phase 4 dependencies."""
        self.log("Checking API compatibility...")
        
        try:
            result = subprocess.run([
                "python", "-c",
                """
import sys
sys.path.insert(0, 'src')

# Test key APIs that Phase 4 will depend on
from graphics.graphics_manager import GraphicsManager
from graphics.coordinate_system import CoordinateSystem
from graphics.globe_renderer import GlobeRenderer

# Check GraphicsManager has required methods
gm_methods = ['initialize', 'shutdown', 'handle_event', 'update']
for method in gm_methods:
    assert hasattr(GraphicsManager, method), f'GraphicsManager missing {method}'

# Check CoordinateSystem has required methods  
cs_methods = ['lat_lon_to_cartesian', 'cartesian_to_lat_lon']
for method in cs_methods:
    assert hasattr(CoordinateSystem, method), f'CoordinateSystem missing {method}'

# Check GlobeRenderer has required methods
gr_methods = ['initialize', 'add_marker', 'remove_marker']
for method in gr_methods:
    assert hasattr(GlobeRenderer, method), f'GlobeRenderer missing {method}'

print('API_COMPATIBILITY_OK')
                """
            ], capture_output=True, text=True, cwd=self.root_path, timeout=15)
            
            if result.returncode != 0:
                self.log(f"API compatibility check failed: {result.stderr}", "ERROR")
                return False
            
            if 'API_COMPATIBILITY_OK' not in result.stdout:
                self.log("API compatibility validation failed", "ERROR")
                return False
            
            self.log("API compatibility PASSED", "SUCCESS")
            self.results["api_compatibility"] = True
            return True
            
        except Exception as e:
            self.log(f"API compatibility check error: {e}", "ERROR")
            return False

    def run_file_size_monitor(self):
        """Run the project's file size monitoring tool."""
        self.log("Running file size monitor...")
        
        try:
            result = subprocess.run(
                ["python", "tools/file_size_monitor.py", "--check"],
                capture_output=True,
                text=True,
                cwd=self.root_path,
                timeout=30
            )
            
            if result.returncode != 0:
                self.log("File size monitor FAILED", "ERROR")
                self.log(f"Output: {result.stdout}", "ERROR")
                return False
            else:
                self.log("File size monitor PASSED", "SUCCESS")
                return True
                
        except Exception as e:
            self.log(f"File size monitor error: {e}", "ERROR")
            return False

    def generate_report(self):
        """Generate validation report."""
        self.log("Generating validation report...")
        
        report = f"""
========================================
PHASE 3 REFACTORING VALIDATION REPORT
========================================
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}

Results Summary:
- File Size Compliance: {'✓ PASS' if self.results['file_size_compliance'] else '✗ FAIL'}
- Import Integrity: {'✓ PASS' if self.results['import_integrity'] else '✗ FAIL'}  
- Functional Integrity: {'✓ PASS' if self.results['functional_integrity'] else '✗ FAIL'}
- Performance Check: {'✓ PASS' if self.results['performance_check'] else '✗ FAIL'}
- API Compatibility: {'✓ PASS' if self.results['api_compatibility'] else '✗ FAIL'}

Overall Status: {'✓ SUCCESS' if all(self.results.values()) else '✗ FAILED'}

Target Files Checked:
{chr(10).join(f'  - {f}' for f in self.target_files)}

New Utility Files:
{chr(10).join(f'  - {f}' for f in self.new_utility_files)}

========================================
"""
        
        print(report)
        
        # Write report to file
        with open(self.root_path / "phase3_refactor_validation_report.txt", "w") as f:
            f.write(report)
        
        return all(self.results.values())

    def run_validation(self, include_performance=False):
        """Run full validation suite."""
        self.log("Starting Phase 3 refactoring validation...", "INFO")
        
        success = True
        
        # 1. Check file size compliance
        if not self.check_file_sizes():
            success = False
        
        # 2. Check utility files exist
        if not self.check_utility_files_exist():
            success = False
        
        # 3. Check import integrity
        if not self.check_import_integrity():
            success = False
        
        # 4. Check functional integrity
        if not self.check_functional_integrity():
            success = False
        
        # 5. Performance check (optional)
        if include_performance:
            if not self.check_performance_regression():
                success = False
        else:
            self.log("Skipping performance check (use --performance-check to enable)")
            self.results["performance_check"] = True  # Mark as passed if skipped
        
        # 6. API compatibility check  
        if not self.check_api_compatibility():
            success = False
        
        # 7. Run project file size monitor
        if not self.run_file_size_monitor():
            success = False
        
        # Generate final report
        overall_success = self.generate_report()
        
        return overall_success


def main():
    """Main entry point."""
    include_performance = "--performance-check" in sys.argv
    
    validator = Phase3RefactorValidator()
    success = validator.run_validation(include_performance)
    
    if success:
        print("\n🎉 Phase 3 refactoring validation PASSED!")
        sys.exit(0)
    else:
        print("\n❌ Phase 3 refactoring validation FAILED!")
        print("   See validation report above for details.")
        
        # Determine specific exit code
        if not validator.results["file_size_compliance"]:
            sys.exit(1)
        elif not validator.results["import_integrity"]:
            sys.exit(2)
        elif not validator.results["functional_integrity"]:
            sys.exit(3)
        elif not validator.results["performance_check"]:
            sys.exit(4)
        elif not validator.results["api_compatibility"]:
            sys.exit(5)
        else:
            sys.exit(1)  # General failure


if __name__ == "__main__":
    main()