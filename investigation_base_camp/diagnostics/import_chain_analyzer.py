#!/usr/bin/env python3
"""
Import Chain Analyzer
Purpose: Deep analysis of import dependencies in graphics modules
Author: GitHub Copilot
Created: 2025-09-17

Analyzes complete import chains to identify broken dependencies
and their impact on the module ecosystem.
"""

import sys
import json
import importlib
from pathlib import Path
from typing import Dict, List, Set, Any
import traceback
import ast

# Add src to path for analysis
workspace_root = Path(__file__).parent.parent.parent
src_path = workspace_root / "src"
sys.path.insert(0, str(src_path))

class ImportChainAnalyzer:
    """Analyzes import chains and identifies broken dependencies."""
    
    def __init__(self):
        self.analysis_results = {
            "timestamp": "2025-09-17",
            "workspace_root": str(workspace_root),
            "src_modules_analyzed": [],
            "import_chains": {},
            "broken_imports": [],
            "working_imports": [],
            "circular_dependencies": [],
            "external_dependencies": {},
            "recommendations": []
        }
    
    def analyze_graphics_modules(self):
        """Analyze all modules in src/graphics/ recursively."""
        graphics_path = src_path / "graphics"
        
        if not graphics_path.exists():
            self.analysis_results["error"] = f"Graphics path not found: {graphics_path}"
            return
            
        # Find all Python files in graphics directory
        python_files = list(graphics_path.rglob("*.py"))
        
        for py_file in python_files:
            if py_file.name == "__init__.py":
                continue
                
            module_path = self._get_module_path(py_file)
            self.analysis_results["src_modules_analyzed"].append(module_path)
            
            # Analyze this specific module
            self._analyze_single_module(py_file, module_path)
    
    def _get_module_path(self, file_path: Path) -> str:
        """Convert file path to Python module path."""
        relative_path = file_path.relative_to(src_path)
        module_parts = list(relative_path.parts[:-1]) + [relative_path.stem]
        return ".".join(module_parts)
    
    def _analyze_single_module(self, file_path: Path, module_path: str):
        """Analyze imports for a single module."""
        try:
            # Parse the Python file to extract import statements
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            imports = self._extract_imports_from_ast(tree)
            
            # Store import information
            self.analysis_results["import_chains"][module_path] = {
                "file_path": str(file_path),
                "direct_imports": imports,
                "import_success": {},
                "import_errors": {}
            }
            
            # Test each import
            for import_item in imports:
                try:
                    if import_item["type"] == "import":
                        importlib.import_module(import_item["module"])
                    elif import_item["type"] == "from_import":
                        module = importlib.import_module(import_item["module"])
                        # Test if the imported names exist
                        for name in import_item["names"]:
                            if not hasattr(module, name):
                                raise AttributeError(f"Module {import_item['module']} has no attribute {name}")
                    
                    self.analysis_results["import_chains"][module_path]["import_success"][import_item["module"]] = True
                    self.analysis_results["working_imports"].append({
                        "module": module_path,
                        "import": import_item["module"],
                        "type": import_item["type"]
                    })
                    
                except Exception as e:
                    error_info = {
                        "module": module_path,
                        "failed_import": import_item["module"],
                        "import_type": import_item["type"],
                        "error": str(e),
                        "error_type": type(e).__name__
                    }
                    
                    self.analysis_results["import_chains"][module_path]["import_errors"][import_item["module"]] = error_info
                    self.analysis_results["broken_imports"].append(error_info)
            
        except Exception as e:
            self.analysis_results["broken_imports"].append({
                "module": module_path,
                "failed_import": "PARSE_ERROR",
                "error": str(e),
                "error_type": type(e).__name__
            })
    
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
    
    def generate_recommendations(self):
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Count broken vs working imports
        broken_count = len(self.analysis_results["broken_imports"])
        working_count = len(self.analysis_results["working_imports"])
        
        if broken_count > 0:
            recommendations.append(f"CRITICAL: {broken_count} broken imports found - production modules non-functional")
        
        if working_count > 0:
            recommendations.append(f"POSITIVE: {working_count} imports work correctly")
        
        # Identify most common failure patterns
        error_types = {}
        for error in self.analysis_results["broken_imports"]:
            error_type = error.get("error_type", "Unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        for error_type, count in error_types.items():
            recommendations.append(f"Common failure: {error_type} ({count} occurrences)")
        
        # Check for specific known issues
        gltf_imports = [e for e in self.analysis_results["broken_imports"] if "gltf" in e.get("failed_import", "").lower()]
        if gltf_imports:
            recommendations.append(f"IDENTIFIED ISSUE: {len(gltf_imports)} GLTF-related import failures - likely missing gltf library")
        
        self.analysis_results["recommendations"] = recommendations
    
    def save_results(self):
        """Save analysis results to JSON file."""
        output_path = workspace_root / "investigation_base_camp" / "reports" / "dependency_analysis.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        print(f"Import chain analysis saved to: {output_path}")
        return output_path

def main():
    """Run complete import chain analysis."""
    print("🔍 Starting Import Chain Analysis...")
    
    analyzer = ImportChainAnalyzer()
    analyzer.analyze_graphics_modules()
    analyzer.generate_recommendations()
    
    # Print summary
    broken = len(analyzer.analysis_results["broken_imports"])
    working = len(analyzer.analysis_results["working_imports"])
    
    print(f"\n📊 Analysis Summary:")
    print(f"   ✅ Working imports: {working}")
    print(f"   ❌ Broken imports: {broken}")
    print(f"   📁 Modules analyzed: {len(analyzer.analysis_results['src_modules_analyzed'])}")
    
    if broken > 0:
        print(f"\n🚨 CRITICAL ISSUES FOUND:")
        for rec in analyzer.analysis_results["recommendations"]:
            print(f"   • {rec}")
    
    output_path = analyzer.save_results()
    print(f"\n💾 Complete analysis saved to: {output_path}")

if __name__ == "__main__":
    main()