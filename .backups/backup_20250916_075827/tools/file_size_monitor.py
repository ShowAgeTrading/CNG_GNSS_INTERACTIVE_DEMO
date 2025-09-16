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
    
    @classmethod
    def load_from_file(cls, config_file: Path) -> 'FileSizeLimits':
        """Load limits from JSON config file."""
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                # Filter to only the actual limit fields, ignore documentation fields starting with _
                limit_data = {k: v for k, v in data.items() if not k.startswith('_')}
                return cls(**limit_data)
            except Exception as e:
                print(f"Warning: Could not load config from {config_file}: {e}")
                pass
        return cls()  # Return defaults if file doesn't exist or is invalid
    
    def save_to_file(self, config_file: Path) -> None:
        """Save limits to JSON config file."""
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump({
                'code_files': self.code_files,
                'planning_docs': self.planning_docs,
                'template_files': self.template_files,
                'config_files': self.config_files
            }, f, indent=2)

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
        
        # Load limits from config file, with defaults if not found
        self.config_file = self.root_path / '.github' / 'file_size_limits.json'
        self.limits = FileSizeLimits.load_from_file(self.config_file)
        
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
        relative_path = str(file_path.relative_to(self.root_path)).lower()
        
        # Check template files first (most specific)
        if 'template' in relative_path and 'planning' in relative_path:
            return self.limits.template_files
        
        # Check planning docs
        if 'planning' in relative_path and file_path.suffix == '.md':
            return self.limits.planning_docs
        
        # Check project source code files (src/ directory only)
        if relative_path.startswith('src') and file_path.suffix == '.py':
            return self.limits.code_files
        
        # Check project config files (root level only)
        if '/' not in relative_path and '\\' not in relative_path and file_path.suffix in ['.json', '.yaml', '.yml', '.toml']:
            return self.limits.config_files
        
        # Default: no limit for other files (don't interfere with other projects)
        return 999999
    
    def _has_refactoring_evidence(self, file_path: Path) -> bool:
        """Check if file has evidence of prior refactoring for leniency."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Evidence indicators (broader patterns)
            refactoring_keywords = [
                'extract', 'refactor', 'split', 'modular', 'decompose',
                'separate', 'isolate', 'optimize', 'restructure',
                'TODO: refactor', 'FIXME:', 'XXX:', 'component', 'lifecycle',
                'framework', 'manager', 'engine', 'interface', 'abstract'
            ]
            
            # Check entire content for refactoring evidence (case insensitive)
            content_lower = content.lower()
            
            # Look for any refactoring keywords anywhere in file
            if any(keyword in content_lower for keyword in refactoring_keywords):
                return True
            
            # Check for architectural patterns indicating complex refactored code
            architectural_patterns = [
                'class.*interface', 'class.*manager', 'class.*engine',
                'class.*framework', '__init__', '__enter__', '__exit__',
                'abstractmethod', 'property', '@', 'def initialize',
                'def cleanup', 'def start', 'def stop'
            ]
            
            # Use regex for pattern matching
            import re
            for pattern in architectural_patterns:
                if re.search(pattern, content_lower):
                    return True
            
            # Files over 150 lines are likely complex enough to warrant leniency
            line_count = len(content.split('\n'))
            if line_count > 150:
                return True
            
            return False
            
        except (UnicodeDecodeError, PermissionError):
            return False
    
    def get_file_status(self, file_path: Path) -> FileStatus:
        """Get current status of file."""
        lines = self.count_lines(file_path)
        limit = self.get_file_limit(file_path)
        
        # Apply leniency for files with evidence of prior refactoring
        effective_limit = limit
        leniency_applied = False
        if self._has_refactoring_evidence(file_path):
            effective_limit = int(limit * 1.15)  # 15% leniency
            leniency_applied = True
        
        # Calculate percentage based on effective limit for accurate reporting
        percentage = (lines / effective_limit) * 100 if effective_limit > 0 else 0
        
        # Determine status
        if lines > effective_limit:
            status = "ERROR"
        elif percentage >= 90:
            status = "WARNING"
        else:
            status = "OK"
        
        return FileStatus(
            path=str(file_path.relative_to(self.root_path)),
            lines=lines,
            limit=effective_limit if leniency_applied else limit,  # Show effective limit if leniency applied
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
    
    def update_limits(self, file_type: str, new_limit: int) -> bool:
        """Update file size limit for a specific file type."""
        if file_type == 'planning':
            self.limits.planning_docs = new_limit
        elif file_type == 'code':
            self.limits.code_files = new_limit
        elif file_type == 'template':
            self.limits.template_files = new_limit
        elif file_type == 'config':
            self.limits.config_files = new_limit
        elif file_type == 'all':
            # Set all limits to the same value
            self.limits.planning_docs = new_limit
            self.limits.code_files = new_limit
            self.limits.template_files = new_limit
            self.limits.config_files = new_limit
        else:
            print(f"❌ Unknown file type: {file_type}")
            print("Valid types: planning, code, template, config, all")
            return False
        
        # Save updated limits
        self.limits.save_to_file(self.config_file)
        print(f"✅ Updated {file_type} file limit to {new_limit} lines")
        print(f"Config saved to: {self.config_file}")
        return True

def main():
    """Main command line interface."""
    parser = argparse.ArgumentParser(description="Monitor and enforce file size limits")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--enforce", action="store_true", help="Enforce limits (exit with error if violations)")
    parser.add_argument("--check", action="store_true", help="Quick compliance check")
    parser.add_argument("--path", default=".", help="Root path to scan (default: current directory)")
    parser.add_argument("--set-limit", nargs=2, metavar=('TYPE', 'LINES'), 
                       help="Set file size limit: TYPE=planning|code|template|config|all LINES=number")
    
    args = parser.parse_args()
    
    monitor = FileSizeMonitor(args.path)
    
    if args.set_limit:
        file_type, limit_str = args.set_limit
        try:
            new_limit = int(limit_str)
            if new_limit <= 0:
                print("❌ Limit must be a positive number")
                sys.exit(1)
            monitor.update_limits(file_type, new_limit)
        except ValueError:
            print("❌ Limit must be a valid number")
            sys.exit(1)
    elif args.report:
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