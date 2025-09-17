#!/usr/bin/env python3
"""
Module Health Checker
Purpose: Test import and instantiation health of graphics system components
Author: GitHub Copilot
Created: 2025-09-17

Systematically tests each graphics module for import success and
basic instantiation to identify specific failure points.
"""

import sys
import importlib
from pathlib import Path
from typing import Dict, List, Any
import traceback
from datetime import datetime

# Add src to path for testing
workspace_root = Path(__file__).parent.parent.parent
src_path = workspace_root / "src"
sys.path.insert(0, str(src_path))

class ModuleHealthChecker:
    """Tests health of individual graphics modules."""
    
    def __init__(self):
        self.health_report = {
            "timestamp": datetime.now().isoformat(),
            "test_summary": {
                "total_modules": 0,
                "import_successful": 0,
                "import_failed": 0,
                "instantiation_successful": 0,
                "instantiation_failed": 0
            },
            "module_results": {},
            "critical_failures": [],
            "architecture_impact": []
        }
    
    def test_all_graphics_modules(self):
        """Test all modules in the graphics system."""
        
        # Test core graphics modules
        core_modules = [
            "graphics.graphics_manager",
            "graphics.config_manager",
            "graphics.event_handler", 
            "graphics.panda3d_initializer",
            "graphics.subsystem_manager",
            "graphics.subsystem_factory"
        ]
        
        # Test globe modules
        globe_modules = [
            "graphics.globe",
        ]
        
        # Test specialized modules (if they exist)
        specialized_modules = []
        
        # Find actual modules by scanning directories
        graphics_path = src_path / "graphics"
        if graphics_path.exists():
            actual_modules = self._discover_modules(graphics_path)
            all_test_modules = list(set(core_modules + globe_modules + actual_modules))
        else:
            all_test_modules = core_modules + globe_modules
        
        self.health_report["test_summary"]["total_modules"] = len(all_test_modules)
        
        # Test each module
        for module_name in all_test_modules:
            print(f"Testing module: {module_name}")
            self._test_single_module(module_name)
    
    def _discover_modules(self, graphics_path: Path) -> List[str]:
        """Discover actual modules in graphics directory."""
        modules = []
        
        for py_file in graphics_path.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue
                
            # Convert path to module name
            relative_path = py_file.relative_to(src_path)
            module_parts = list(relative_path.parts[:-1]) + [relative_path.stem]
            module_name = ".".join(module_parts)
            modules.append(module_name)
        
        return modules
    
    def _test_single_module(self, module_name: str):
        """Test a single module for import and instantiation."""
        
        module_result = {
            "module_name": module_name,
            "import_success": False,
            "import_error": None,
            "instantiation_tests": {},
            "class_discoveries": [],
            "function_discoveries": [],
            "dependencies": []
        }
        
        try:
            # Test import
            print(f"  → Importing {module_name}...")
            module = importlib.import_module(module_name)
            module_result["import_success"] = True
            self.health_report["test_summary"]["import_successful"] += 1
            
            # Discover classes and functions
            module_result["class_discoveries"] = [name for name in dir(module) if isinstance(getattr(module, name, None), type)]
            module_result["function_discoveries"] = [name for name in dir(module) if callable(getattr(module, name, None)) and not name.startswith('_')]
            
            # Test instantiation of key classes
            self._test_class_instantiation(module, module_result)
            
        except Exception as e:
            module_result["import_success"] = False
            module_result["import_error"] = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc()
            }
            self.health_report["test_summary"]["import_failed"] += 1
            
            # Add to critical failures if this is a core module
            if any(core in module_name for core in ["graphics_manager", "globe", "panda3d_initializer"]):
                self.health_report["critical_failures"].append({
                    "module": module_name,
                    "failure_type": "import_failure",
                    "impact": "HIGH - Core graphics functionality affected",
                    "error": str(e)
                })
        
        self.health_report["module_results"][module_name] = module_result
    
    def _test_class_instantiation(self, module, module_result: Dict[str, Any]):
        """Test instantiation of classes found in the module."""
        
        for class_name in module_result["class_discoveries"]:
            if class_name.startswith('_'):
                continue
                
            try:
                cls = getattr(module, class_name)
                
                # Try basic instantiation (no arguments)
                print(f"    → Testing {class_name} instantiation...")
                
                # Check if constructor requires arguments
                import inspect
                sig = inspect.signature(cls.__init__)
                params = [p for name, p in sig.parameters.items() if name != 'self' and p.default == inspect.Parameter.empty]
                
                if len(params) == 0:
                    # Try instantiation with no args
                    instance = cls()
                    module_result["instantiation_tests"][class_name] = {
                        "success": True,
                        "method": "no_args"
                    }
                    self.health_report["test_summary"]["instantiation_successful"] += 1
                else:
                    module_result["instantiation_tests"][class_name] = {
                        "success": False,
                        "method": "requires_args",
                        "required_params": [p.name for p in params]
                    }
                
            except Exception as e:
                module_result["instantiation_tests"][class_name] = {
                    "success": False,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
                self.health_report["test_summary"]["instantiation_failed"] += 1
    
    def analyze_architecture_impact(self):
        """Analyze impact on overall architecture."""
        
        # Check if core Phase 1-2 systems are affected
        core_phase2_modules = ["core.event_bus", "core.simulation_clock", "core.app_framework"]
        
        for core_module in core_phase2_modules:
            try:
                importlib.import_module(core_module)
                self.health_report["architecture_impact"].append({
                    "component": core_module,
                    "status": "HEALTHY",
                    "impact": "No impact - Phase 2 foundation intact"
                })
            except Exception as e:
                self.health_report["architecture_impact"].append({
                    "component": core_module,
                    "status": "BROKEN",
                    "impact": "CRITICAL - Phase 2 foundation compromised",
                    "error": str(e)
                })
        
        # Check graphics manager specifically
        graphics_import_failed = not any(
            result.get("import_success", False) 
            for module, result in self.health_report["module_results"].items()
            if "graphics_manager" in module
        )
        
        if graphics_import_failed:
            self.health_report["architecture_impact"].append({
                "component": "graphics_manager",
                "status": "BROKEN",
                "impact": "HIGH - Phase 3 integration impossible, Phase 4-10 blocked"
            })
    
    def generate_report(self):
        """Generate markdown report from health check results."""
        
        report_content = f"""# Module Health Report
**Generated:** {self.health_report['timestamp']}  
**Purpose:** Graphics system component health assessment

---

## Executive Summary

### Test Results Overview
- **Total Modules Tested:** {self.health_report['test_summary']['total_modules']}
- **Import Success:** {self.health_report['test_summary']['import_successful']}
- **Import Failures:** {self.health_report['test_summary']['import_failed']}
- **Instantiation Success:** {self.health_report['test_summary']['instantiation_successful']}
- **Instantiation Failures:** {self.health_report['test_summary']['instantiation_failed']}

### Health Status
"""
        
        if self.health_report['test_summary']['import_failed'] == 0:
            report_content += "✅ **HEALTHY** - All modules import successfully\n\n"
        elif self.health_report['test_summary']['import_failed'] < self.health_report['test_summary']['total_modules'] / 2:
            report_content += "⚠️  **DEGRADED** - Some modules failing\n\n" 
        else:
            report_content += "🚨 **CRITICAL** - Major system failure\n\n"
        
        # Critical Failures Section
        if self.health_report['critical_failures']:
            report_content += "## Critical Failures\n\n"
            for failure in self.health_report['critical_failures']:
                report_content += f"""### {failure['module']}
- **Impact:** {failure['impact']}
- **Error:** {failure['error']}
- **Type:** {failure['failure_type']}

"""
        
        # Architecture Impact Section
        report_content += "## Architecture Impact Analysis\n\n"
        for impact in self.health_report['architecture_impact']:
            status_icon = "✅" if impact['status'] == "HEALTHY" else "🚨"
            report_content += f"- {status_icon} **{impact['component']}:** {impact['impact']}\n"
        
        # Detailed Module Results
        report_content += "\n## Detailed Module Results\n\n"
        
        for module_name, result in self.health_report['module_results'].items():
            status_icon = "✅" if result['import_success'] else "❌"
            report_content += f"### {status_icon} {module_name}\n\n"
            
            if result['import_success']:
                report_content += f"- **Import:** Success\n"
                report_content += f"- **Classes Found:** {len(result['class_discoveries'])}\n"
                report_content += f"- **Functions Found:** {len(result['function_discoveries'])}\n"
                
                if result['instantiation_tests']:
                    report_content += "- **Instantiation Tests:**\n"
                    for class_name, test_result in result['instantiation_tests'].items():
                        test_icon = "✅" if test_result.get('success', False) else "❌"
                        report_content += f"  - {test_icon} {class_name}\n"
                
            else:
                report_content += f"- **Import:** FAILED\n"
                report_content += f"- **Error:** {result['import_error']['error_type']}: {result['import_error']['error_message']}\n"
            
            report_content += "\n"
        
        return report_content
    
    def save_report(self):
        """Save health report to markdown file."""
        
        report_content = self.generate_report()
        output_path = workspace_root / "investigation_base_camp" / "reports" / "module_status_report.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Module health report saved to: {output_path}")
        return output_path

def main():
    """Run complete module health check."""
    print("🏥 Starting Module Health Check...")
    
    checker = ModuleHealthChecker()
    checker.test_all_graphics_modules()
    checker.analyze_architecture_impact()
    
    # Print summary
    summary = checker.health_report["test_summary"]
    print(f"\n📊 Health Check Summary:")
    print(f"   📦 Total modules: {summary['total_modules']}")
    print(f"   ✅ Import success: {summary['import_successful']}")
    print(f"   ❌ Import failed: {summary['import_failed']}")
    print(f"   🏗️  Instantiation success: {summary['instantiation_successful']}")
    print(f"   💥 Instantiation failed: {summary['instantiation_failed']}")
    
    if checker.health_report['critical_failures']:
        print(f"\n🚨 CRITICAL FAILURES DETECTED:")
        for failure in checker.health_report['critical_failures']:
            print(f"   • {failure['module']}: {failure['impact']}")
    
    output_path = checker.save_report()
    print(f"\n💾 Complete health report saved to: {output_path}")

if __name__ == "__main__":
    main()