#!/usr/bin/env python3
"""
Phase 3 Test Runner - Run all Phase 3 graphics tests
Purpose: Execute all Phase 3 tests in proper order with clear results

Usage: python run_phase3_tests.py [--visual]
Options:
    --visual    Also run the visual test (opens 3D window)
    --unit      Run only unit tests
    --integration   Run only integration test

This script runs:
1. Unit tests for graphics components
2. Integration test with Phase 2 core
3. Optional visual test for user feedback
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
        
        # Print output
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        success = result.returncode == 0
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\nResult: {status} (Exit code: {result.returncode})")
        
        return success
        
    except Exception as e:
        print(f"❌ Command execution failed: {e}")
        return False


def main():
    """Run Phase 3 tests based on command line arguments."""
    parser = argparse.ArgumentParser(description="Run Phase 3 graphics tests")
    parser.add_argument("--visual", action="store_true", 
                       help="Run visual test (opens 3D window)")
    parser.add_argument("--unit", action="store_true",
                       help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", 
                       help="Run only integration test")
    
    args = parser.parse_args()
    
    # If no specific test type specified, run unit and integration
    if not (args.unit or args.integration or args.visual):
        args.unit = True
        args.integration = True
    
    print("🧪 PHASE 3 GRAPHICS ENGINE TEST SUITE")
    print("=====================================")
    print(f"Running from: {Path.cwd()}")
    print(f"Python: {sys.executable}")
    
    results = []
    
    # Run unit tests
    if args.unit:
        print("\n📋 UNIT TESTS")
        print("=" * 40)
        
        unit_tests = [
            ("tests/unit/test_graphics_manager.py", "Graphics Manager Unit Tests"),
            ("tests/unit/test_camera_controller.py", "Camera Controller Unit Tests")
        ]
        
        for test_file, description in unit_tests:
            if Path(test_file).exists():
                success = run_command([sys.executable, test_file], description)
                results.append((description, success))
            else:
                print(f"⚠️  Test file not found: {test_file}")
                results.append((description, False))
    
    # Run integration test
    if args.integration:
        print("\n🔗 INTEGRATION TEST")
        print("=" * 40)
        
        integration_test = "tests/integration/test_phase3_graphics.py"
        if Path(integration_test).exists():
            success = run_command([sys.executable, integration_test], 
                                "Phase 3 Graphics Integration Test")
            results.append(("Integration Test", success))
        else:
            print(f"⚠️  Integration test not found: {integration_test}")
            results.append(("Integration Test", False))
    
    # Run visual test
    if args.visual:
        print("\n👁️  VISUAL TEST")
        print("=" * 40)
        print("This will open a 3D window for visual feedback...")
        print("Close the window or press ESC when done reviewing.")
        print()
        
        visual_test = "tests/visual/test_phase3_visual.py"
        if Path(visual_test).exists():
            success = run_command([sys.executable, visual_test], 
                                "Phase 3 Visual Feedback Test")
            results.append(("Visual Test", success))
        else:
            print(f"⚠️  Visual test not found: {visual_test}")
            results.append(("Visual Test", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed_count = 0
    total_count = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:10} {test_name}")
        if success:
            passed_count += 1
    
    print(f"\nOverall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All Phase 3 tests PASSED!")
        exit_code = 0
    else:
        print("⚠️  Some Phase 3 tests FAILED - check output above")
        exit_code = 1
    
    print("\n📋 NEXT STEPS:")
    if args.visual:
        print("   → Review visual test feedback for Phase 3 graphics quality")
        print("   → Report any visual issues or missing features")
    print("   → Fix any failing tests before continuing Phase 3 development")
    print("   → Run integration tests after Phase 3 changes")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())