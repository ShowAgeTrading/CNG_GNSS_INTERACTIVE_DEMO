#!/usr/bin/env python3
"""
File Size Monitor and Enforcement Tool
Monitors file sizes and enforces limits defined in UNIVERSAL_CODE_TEMPLATE.md
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple
from dataclasses import dataclass
import json
import argparse

@dataclass
class FileSizeLimits:
    """File size limits by file type."""
    code_files: int = 200
    planning_docs: int = 500
    template_files: int = 500
    config_files: int = 100

class FileStatus(NamedTuple):
    """File status information."""
    path: str
    lines: int
    limit: int
    percentage: float
    status: str  # OK, WARNING, ERROR

class FileSizeMonitor:
    """Monitor and enforce file size limits - PROJECT SPECIFIC ONLY."""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        
        # SAFETY CHECK: Only work in this specific project
        if not self._is_gnss_project():
            raise ValueError("File size monitoring only enabled for GNSS Interactive Demo project")
        
        self.limits = FileSizeLimits()
        
        # File type patterns - ONLY for this project structure
        self.file_patterns = {
            'code_files': ['src/**/*.py'],  # Only src/ directory Python files
            'planning_docs': ['planning/**/*.md'],  # Only planning docs
            'template_files': ['**/templates/**/*.md'],  # Only template files
            'config_files': ['*.json', '*.yaml', '*.yml', '*.toml']  # Only root config files
        }
    
    def _is_gnss_project(self) -> bool:
        """Verify this is the GNSS Interactive Demo project."""
        project_markers = [
            self.root_path / "planning" / "templates" / "UNIVERSAL_CODE_TEMPLATE.md",
            self.root_path / "planning" / "MASTER_IMPLEMENTATION_PLAN.md"
        ]
        
        # Must have project-specific files to activate
        return all(marker.exists() for marker in project_markers)
    
    def scan_directory(self, directory: Path = None) -> List[FileStatus]:
        """Scan directory for files and check sizes - PROJECT SPECIFIC ONLY."""
        if directory is None:
            directory = self.root_path
        
        # Double-check we're in the right project
        if not self._is_gnss_project():
            print("⚠️  File size monitoring disabled - not in GNSS Interactive Demo project")
            return []
        
        results = []
        
        # Scan all relevant files
        for pattern_type, patterns in self.file_patterns.items():
            for pattern in patterns:
                for file_path in directory.glob(pattern):
                    if file_path.is_file():
                        results.append(self.get_file_status(file_path))
        
        return results
    
    def count_lines(self, file_path: Path) -> int:
        """Count actual lines in file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return len(f.readlines())
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return 0
    
    def get_file_limit(self, file_path: Path) -> int:
        """Get appropriate limit for file type - PROJECT SPECIFIC RULES ONLY."""
        file_str = str(file_path).lower()
        
        # Only apply limits to files within this project structure
        if not str(file_path).startswith(str(self.root_path)):
            return 999999  # No limits for files outside project
        
        # Check template files first (most specific)
        if 'template' in file_str and 'planning' in file_str:
            return self.limits.template_files
        
        # Check planning docs
        if 'planning' in file_str and file_path.suffix == '.md':
            return self.limits.planning_docs
        
        # Check project source code files (src/ directory only)
        if 'src' in file_str and file_path.suffix == '.py':
            return self.limits.code_files
        
        # Check project config files (root level only)
        if file_path.parent == self.root_path and file_path.suffix in ['.json', '.yaml', '.yml', '.toml']:
            return self.limits.config_files
        
        # Default: no limit for other files (don't interfere with other projects)
        return 999999
    
    def get_file_status(self, file_path: Path) -> FileStatus:
        """Get current status of file."""
        lines = self.count_lines(file_path)
        limit = self.get_file_limit(file_path)
        percentage = (lines / limit) * 100 if limit > 0 else 0
        
        # Determine status
        if lines > limit:
            status = "ERROR"
        elif percentage >= 90:
            status = "WARNING"
        else:
            status = "OK"
        
        return FileStatus(
            path=str(file_path.relative_to(self.root_path)),
            lines=lines,
            limit=limit,
            percentage=percentage,
            status=status
        )
    
    def scan_directory(self, directory: Path = None) -> List[FileStatus]:
        """Scan directory for files and check sizes."""
        if directory is None:
            directory = self.root_path
        
        results = []
        
        # Scan all relevant files
        for pattern_type, patterns in self.file_patterns.items():
            for pattern in patterns:
                for file_path in directory.glob(pattern):
                    if file_path.is_file():
                        results.append(self.get_file_status(file_path))
        
        return results
    
    def check_compliance(self) -> bool:
        """Check if all files comply with size limits."""
        results = self.scan_directory()
        errors = [r for r in results if r.status == "ERROR"]
        return len(errors) == 0
    
    def generate_report(self) -> str:
        """Generate detailed size report."""
        results = self.scan_directory()
        
        # Separate by status
        errors = [r for r in results if r.status == "ERROR"]
        warnings = [r for r in results if r.status == "WARNING"]
        ok_files = [r for r in results if r.status == "OK"]
        
        report = []
        report.append("=" * 60)
        report.append("FILE SIZE COMPLIANCE REPORT")
        report.append("=" * 60)
        report.append(f"Total files scanned: {len(results)}")
        report.append(f"Compliant files: {len(ok_files)}")
        report.append(f"Warning files: {len(warnings)}")
        report.append(f"Over-limit files: {len(errors)}")
        report.append("")
        
        if errors:
            report.append("🚨 FILES EXCEEDING LIMITS:")
            report.append("-" * 40)
            for file_status in errors:
                report.append(f"  {file_status.path}")
                report.append(f"    Lines: {file_status.lines}/{file_status.limit} ({file_status.percentage:.1f}%)")
                report.append(f"    OVER LIMIT BY: {file_status.lines - file_status.limit} lines")
                report.append("")
        
        if warnings:
            report.append("⚠️  FILES APPROACHING LIMITS (90%+):")
            report.append("-" * 40)
            for file_status in warnings:
                report.append(f"  {file_status.path}")
                report.append(f"    Lines: {file_status.lines}/{file_status.limit} ({file_status.percentage:.1f}%)")
                report.append("")
        
        report.append("✅ COMPLIANT FILES:")
        report.append("-" * 40)
        for file_status in ok_files:
            report.append(f"  {file_status.path}: {file_status.lines}/{file_status.limit} lines ({file_status.percentage:.1f}%)")
        
        return "\n".join(report)
    
    def enforce_limits(self) -> bool:
        """Enforce limits - return False if any violations found."""
        results = self.scan_directory()
        errors = [r for r in results if r.status == "ERROR"]
        
        if errors:
            print("🚨 FILE SIZE VIOLATIONS DETECTED!")
            print("The following files exceed their limits:")
            print()
            
            for file_status in errors:
                print(f"❌ {file_status.path}")
                print(f"   Current: {file_status.lines} lines")
                print(f"   Limit: {file_status.limit} lines")
                print(f"   Over by: {file_status.lines - file_status.limit} lines")
                print()
            
            print("ENFORCEMENT ACTION REQUIRED:")
            print("- Split large files into smaller components")
            print("- Extract reusable functions into separate modules")
            print("- Consider if functionality should be distributed")
            print()
            return False
        
        warnings = [r for r in results if r.status == "WARNING"]
        if warnings:
            print("⚠️  WARNING: Files approaching limits:")
            for file_status in warnings:
                print(f"   {file_status.path}: {file_status.lines}/{file_status.limit} lines ({file_status.percentage:.1f}%)")
            print()
        
        return True

def main():
    """Main command line interface."""
    parser = argparse.ArgumentParser(description="Monitor and enforce file size limits")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--enforce", action="store_true", help="Enforce limits (exit with error if violations)")
    parser.add_argument("--check", action="store_true", help="Quick compliance check")
    parser.add_argument("--path", default=".", help="Root path to scan (default: current directory)")
    
    args = parser.parse_args()
    
    monitor = FileSizeMonitor(args.path)
    
    if args.report:
        print(monitor.generate_report())
    elif args.enforce:
        if not monitor.enforce_limits():
            sys.exit(1)
        else:
            print("✅ All files comply with size limits!")
    elif args.check:
        if monitor.check_compliance():
            print("✅ All files within limits")
        else:
            print("❌ Some files exceed limits")
            sys.exit(1)
    else:
        # Default: show report
        print(monitor.generate_report())

if __name__ == "__main__":
    main()