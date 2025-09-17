#!/usr/bin/env python3
"""
Test Path Tracer
Purpose: Compare visual test success path vs production failure path
Author: GitHub Copilot
Created: 2025-09-17

Analyzes why visual test works (direct Panda3D) vs why production
graphics modules fail, providing detailed path comparison.
"""

import sys
import ast
import importlib
from pathlib import Path
from typing import Dict, List, Any, Set
import traceback
from datetime import datetime

# Add src to path for analysis
workspace_root = Path(__file__).parent.parent.parent
src_path = workspace_root / "src"
tests_path = workspace_root / "tests"
sys.path.insert(0, str(src_path))

class TestPathTracer:
    """Traces and compares execution paths between visual test and production code."""
    
    def __init__(self):
        self.analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "visual_test_analysis": {},
            "production_path_analysis": {},
            "path_comparison": {},
            "divergence_points": [],
            "success_factors": [],
            "failure_factors": [],
            "recommendations": []
        }
    
    def analyze_visual_test_path(self):
        """Analyze the visual test execution path that works."""
        
        print("🎯 Analyzing Visual Test Success Path...")
        
        visual_test_path = tests_path / "visual" / "test_phase3_visual.py"
        
        if not visual_test_path.exists():
            self.analysis_results["visual_test_analysis"]["error"] = f"Visual test not found: {visual_test_path}"
            return
        
        # Parse visual test file
        with open(visual_test_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
            
            # Extract import strategy
            imports = self._extract_imports_from_ast(tree)
            
            # Extract class and method structure
            classes = self._extract_classes_from_ast(tree)
            
            # Analyze execution flow
            execution_flow = self._analyze_execution_flow(tree)
            
            self.analysis_results["visual_test_analysis"] = {
                "file_path": str(visual_test_path),
                "imports": imports,
                "classes": classes,
                "execution_flow": execution_flow,
                "success_strategy": self._identify_success_strategy(imports, classes)
            }
            
            # Test if visual test actually works
            self._test_visual_test_execution()
            
        except Exception as e:
            self.analysis_results["visual_test_analysis"]["parse_error"] = {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
    
    def analyze_production_path(self):
        """Analyze the production graphics system execution path."""
        
        print("🏭 Analyzing Production Path Failures...")
        
        # Key production modules to analyze
        production_modules = [
            "graphics.graphics_manager",
            "graphics.panda3d_initializer", 
            "graphics.globe",
        ]
        
        production_analysis = {}
        
        for module_name in production_modules:
            print(f"  → Analyzing {module_name}")
            
            module_analysis = {
                "module_name": module_name,
                "import_success": False,
                "import_error": None,
                "file_analysis": None
            }
            
            try:
                # Test import
                module = importlib.import_module(module_name)
                module_analysis["import_success"] = True
                
                # Analyze the source file
                module_file = self._find_module_file(module_name)
                if module_file:
                    module_analysis["file_analysis"] = self._analyze_production_module_file(module_file)
                
            except Exception as e:
                module_analysis["import_error"] = {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "traceback": traceback.format_exc()
                }
                
                # Still try to analyze the source file
                module_file = self._find_module_file(module_name)
                if module_file:
                    try:
                        module_analysis["file_analysis"] = self._analyze_production_module_file(module_file)
                    except Exception as file_e:
                        module_analysis["file_analysis"] = {"parse_error": str(file_e)}
            
            production_analysis[module_name] = module_analysis
        
        self.analysis_results["production_path_analysis"] = production_analysis
    
    def compare_execution_paths(self):
        """Compare visual test vs production execution paths."""
        
        print("🔄 Comparing Execution Paths...")
        
        visual_imports = self.analysis_results["visual_test_analysis"].get("imports", [])
        visual_strategy = self.analysis_results["visual_test_analysis"].get("success_strategy", {})
        
        # Analyze differences in approach
        comparison = {
            "import_strategy_differences": [],
            "architectural_differences": [],
            "execution_differences": [],
            "dependency_differences": []
        }
        
        # Compare import strategies
        visual_direct_imports = [imp for imp in visual_imports if "panda3d" in imp.get("module", "")]
        if visual_direct_imports:
            comparison["import_strategy_differences"].append({
                "visual_approach": "Direct Panda3D imports",
                "production_approach": "Modular graphics system",
                "impact": "Visual test bypasses modular architecture"
            })
        
        # Analyze production module issues
        for module_name, module_data in self.analysis_results["production_path_analysis"].items():
            if not module_data.get("import_success", False):
                error_info = module_data.get("import_error", {})
                comparison["dependency_differences"].append({
                    "module": module_name,
                    "issue": error_info.get("error", "Unknown error"),
                    "type": error_info.get("error_type", "Unknown"),
                    "impact": "Production module non-functional"
                })
        
        self.analysis_results["path_comparison"] = comparison
        
        # Identify key divergence points
        self._identify_divergence_points()
        
        # Identify success and failure factors
        self._identify_success_failure_factors()
    
    def _extract_imports_from_ast(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import statements from AST."""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                        "line": node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append({
                        "type": "from_import",
                        "module": node.module,
                        "names": [alias.name for alias in node.names],
                        "line": node.lineno
                    })
        
        return imports
    
    def _extract_classes_from_ast(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions from AST."""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append({
                            "name": item.name,
                            "line": item.lineno,
                            "args": [arg.arg for arg in item.args.args]
                        })
                
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "bases": [self._get_base_name(base) for base in node.bases],
                    "methods": methods
                })
        
        return classes
    
    def _get_base_name(self, base_node) -> str:
        """Get base class name from AST node."""
        if isinstance(base_node, ast.Name):
            return base_node.id
        elif isinstance(base_node, ast.Attribute):
            return f"{self._get_base_name(base_node.value)}.{base_node.attr}"
        else:
            return "Unknown"
    
    def _analyze_execution_flow(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze execution flow of the test."""
        
        flow = {
            "main_execution": False,
            "class_instantiation": [],
            "method_calls": [],
            "panda3d_usage": []
        }
        
        # Look for main execution
        for node in ast.walk(tree):
            if isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
                if hasattr(node.test.left, 'id') and node.test.left.id == '__name__':
                    flow["main_execution"] = True
        
        # Look for Panda3D specific usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if "loader" in str(node.func.attr) or "loadModel" in str(node.func.attr):
                        flow["panda3d_usage"].append({
                            "type": "model_loading",
                            "line": node.lineno
                        })
        
        return flow
    
    def _identify_success_strategy(self, imports: List[Dict], classes: List[Dict]) -> Dict[str, Any]:
        """Identify the success strategy used by visual test."""
        
        strategy = {
            "approach": "unknown",
            "key_components": [],
            "critical_success_factors": []
        }
        
        # Check for direct Panda3D usage
        panda3d_imports = [imp for imp in imports if "panda3d" in imp.get("module", "")]
        if panda3d_imports:
            strategy["approach"] = "direct_panda3d"
            strategy["key_components"] = [imp["module"] for imp in panda3d_imports]
            strategy["critical_success_factors"].append("Bypasses modular graphics system")
            strategy["critical_success_factors"].append("Uses Panda3D built-in functionality directly")
        
        # Check for ShowBase inheritance
        showbase_classes = [cls for cls in classes if "ShowBase" in cls.get("bases", [])]
        if showbase_classes:
            strategy["critical_success_factors"].append("Inherits from Panda3D ShowBase for direct engine access")
        
        return strategy
    
    def _test_visual_test_execution(self):
        """Test if the visual test actually executes successfully."""
        
        try:
            # Try to import the test module
            import sys
            test_path = tests_path / "visual"
            sys.path.insert(0, str(test_path))
            
            # This will test if imports work
            import test_phase3_visual
            
            self.analysis_results["visual_test_analysis"]["execution_test"] = {
                "import_success": True,
                "message": "Visual test module imports successfully"
            }
            
        except Exception as e:
            self.analysis_results["visual_test_analysis"]["execution_test"] = {
                "import_success": False,
                "error": str(e),
                "message": "Visual test module import failed"
            }
    
    def _find_module_file(self, module_name: str) -> Path:
        """Find the source file for a module."""
        
        parts = module_name.split(".")
        current_path = src_path
        
        for part in parts:
            current_path = current_path / part
            
        # Try .py file
        py_file = current_path.with_suffix(".py")
        if py_file.exists():
            return py_file
            
        # Try __init__.py in directory
        init_file = current_path / "__init__.py"
        if init_file.exists():
            return init_file
            
        return None
    
    def _analyze_production_module_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a production module source file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            return {
                "file_path": str(file_path),
                "imports": self._extract_imports_from_ast(tree),
                "classes": self._extract_classes_from_ast(tree),
                "dependencies": self._extract_dependencies(tree)
            }
            
        except Exception as e:
            return {
                "file_path": str(file_path),
                "parse_error": str(e)
            }
    
    def _extract_dependencies(self, tree: ast.AST) -> List[str]:
        """Extract external dependencies from AST."""
        
        dependencies = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if not alias.name.startswith('.'):
                        dependencies.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module and not node.module.startswith('.'):
                    dependencies.add(node.module.split('.')[0])
        
        return sorted(list(dependencies))
    
    def _identify_divergence_points(self):
        """Identify key points where visual test and production paths diverge."""
        
        divergence_points = []
        
        # Visual test success factors vs production failures
        visual_strategy = self.analysis_results["visual_test_analysis"].get("success_strategy", {})
        
        if visual_strategy.get("approach") == "direct_panda3d":
            divergence_points.append({
                "point": "Graphics Engine Access",
                "visual_approach": "Direct Panda3D ShowBase inheritance",
                "production_approach": "Modular GraphicsManager system",
                "impact": "Visual test bypasses all modular components"
            })
        
        # Import strategy divergence
        for module_name, module_data in self.analysis_results["production_path_analysis"].items():
            if not module_data.get("import_success", False):
                divergence_points.append({
                    "point": f"Module Import: {module_name}",
                    "visual_approach": "Not required - uses direct Panda3D",
                    "production_approach": f"Requires {module_name} to function",
                    "impact": f"Production blocked by {module_name} failure"
                })
        
        self.analysis_results["divergence_points"] = divergence_points
    
    def _identify_success_failure_factors(self):
        """Identify key success and failure factors."""
        
        # Success factors from visual test
        success_factors = []
        visual_strategy = self.analysis_results["visual_test_analysis"].get("success_strategy", {})
        
        for factor in visual_strategy.get("critical_success_factors", []):
            success_factors.append({
                "factor": factor,
                "component": "Visual Test",
                "impact": "Enables working 3D graphics"
            })
        
        # Failure factors from production system
        failure_factors = []
        
        for module_name, module_data in self.analysis_results["production_path_analysis"].items():
            if not module_data.get("import_success", False):
                error_info = module_data.get("import_error", {})
                failure_factors.append({
                    "factor": f"Import failure in {module_name}",
                    "component": module_name,
                    "error": error_info.get("error", "Unknown"),
                    "impact": "Blocks production graphics system"
                })
        
        self.analysis_results["success_factors"] = success_factors
        self.analysis_results["failure_factors"] = failure_factors
    
    def generate_recommendations(self):
        """Generate actionable recommendations based on path analysis."""
        
        recommendations = []
        
        # Based on divergence analysis
        if self.analysis_results["divergence_points"]:
            recommendations.append({
                "priority": "HIGH",
                "category": "Architecture Alignment",
                "action": "Align production graphics modules with visual test success pattern",
                "details": "Ensure production modules use same Panda3D patterns that work in visual test"
            })
        
        # Based on specific failures
        gltf_failures = [f for f in self.analysis_results["failure_factors"] if "gltf" in f.get("error", "").lower()]
        if gltf_failures:
            recommendations.append({
                "priority": "CRITICAL",
                "category": "Dependency Fix",
                "action": "Replace broken GLTF dependencies with Panda3D built-ins",
                "details": "Visual test works without GLTF - production should follow same pattern"
            })
        
        # Based on success factors
        direct_panda3d_success = any("direct" in str(f) for f in self.analysis_results["success_factors"])
        if direct_panda3d_success:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Implementation Strategy", 
                "action": "Implement production modules using direct Panda3D patterns internally",
                "details": "Keep modular architecture but use proven direct Panda3D implementation internally"
            })
        
        self.analysis_results["recommendations"] = recommendations
    
    def save_analysis(self):
        """Save test path analysis to markdown file."""
        
        report_content = f"""# Test Behavior Analysis Report
**Generated:** {self.analysis_results['timestamp']}  
**Purpose:** Compare visual test success vs production failure paths

---

## Executive Summary

### Path Divergence Analysis
Visual test works by **{self.analysis_results['visual_test_analysis'].get('success_strategy', {}).get('approach', 'unknown approach')}** while production system fails due to **{len(self.analysis_results['failure_factors'])} critical issues**.

---

## Visual Test Success Analysis

### Success Strategy
- **Approach:** {self.analysis_results['visual_test_analysis'].get('success_strategy', {}).get('approach', 'Unknown')}
- **Key Components:** {', '.join(self.analysis_results['visual_test_analysis'].get('success_strategy', {}).get('key_components', []))}

### Critical Success Factors
"""
        
        for factor in self.analysis_results.get('success_factors', []):
            report_content += f"- ✅ **{factor['factor']}** - {factor['impact']}\n"
        
        report_content += "\n---\n\n## Production Path Failure Analysis\n\n"
        
        for factor in self.analysis_results.get('failure_factors', []):
            report_content += f"- ❌ **{factor['factor']}** - {factor['impact']}\n"
            if 'error' in factor:
                report_content += f"  - Error: {factor['error']}\n"
        
        report_content += "\n---\n\n## Key Divergence Points\n\n"
        
        for divergence in self.analysis_results.get('divergence_points', []):
            report_content += f"""### {divergence['point']}
- **Visual Approach:** {divergence['visual_approach']}
- **Production Approach:** {divergence['production_approach']} 
- **Impact:** {divergence['impact']}

"""
        
        report_content += "---\n\n## Recommendations\n\n"
        
        for rec in self.analysis_results.get('recommendations', []):
            priority_icon = "🚨" if rec['priority'] == "CRITICAL" else "⚠️" if rec['priority'] == "HIGH" else "💡"
            report_content += f"""### {priority_icon} {rec['category']} ({rec['priority']} Priority)
**Action:** {rec['action']}  
**Details:** {rec['details']}

"""
        
        output_path = workspace_root / "investigation_base_camp" / "reports" / "test_behavior_analysis.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Test behavior analysis saved to: {output_path}")
        return output_path

def main():
    """Run complete test path tracing analysis."""
    print("🔍 Starting Test Path Tracing Analysis...")
    
    tracer = TestPathTracer()
    tracer.analyze_visual_test_path()
    tracer.analyze_production_path()
    tracer.compare_execution_paths()
    tracer.generate_recommendations()
    
    # Print summary
    divergence_count = len(tracer.analysis_results.get("divergence_points", []))
    failure_count = len(tracer.analysis_results.get("failure_factors", []))
    success_count = len(tracer.analysis_results.get("success_factors", []))
    
    print(f"\n📊 Path Analysis Summary:")
    print(f"   ✅ Success factors identified: {success_count}")
    print(f"   ❌ Failure factors identified: {failure_count}")
    print(f"   🔄 Key divergence points: {divergence_count}")
    
    if failure_count > 0:
        print(f"\n🚨 KEY FINDINGS:")
        for factor in tracer.analysis_results.get("failure_factors", []):
            if "gltf" in factor.get("error", "").lower():
                print(f"   • GLTF dependency issue in {factor['component']}")
    
    output_path = tracer.save_analysis()
    print(f"\n💾 Complete analysis saved to: {output_path}")

if __name__ == "__main__":
    main()