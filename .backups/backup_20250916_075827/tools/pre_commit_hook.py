#!/usr/bin/env python3
"""
Git Pre-Commit Hook for File Size Enforcement
Prevents commits that violate file size limits
PROJECT SPECIFIC: Only active in GNSS Interactive Demo project
"""

import subprocess
import sys
from pathlib import Path
from file_size_monitor import FileSizeMonitor

def is_gnss_project():
    """Check if we're in the GNSS Interactive Demo project."""
    project_markers = [
        Path("planning/templates/UNIVERSAL_CODE_TEMPLATE.md"),
        Path("planning/MASTER_IMPLEMENTATION_PLAN.md"),
        Path("tools/file_size_monitor.py")
    ]
    return all(marker.exists() for marker in project_markers)

def get_staged_files():
    """Get list of staged files for commit."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        return [line.strip() for line in result.stdout.split('\n') if line.strip()]
    except subprocess.CalledProcessError:
        return []

def check_staged_files():
    """Check if staged files comply with size limits - PROJECT SPECIFIC ONLY."""
    
    # SAFETY CHECK: Only enforce in GNSS project
    if not is_gnss_project():
        print("ℹ️  File size enforcement disabled - not in GNSS Interactive Demo project")
        return True
    
    staged_files = get_staged_files()
    if not staged_files:
        return True
    
    try:
        monitor = FileSizeMonitor()
    except ValueError as e:
        # Not in the right project
        print(f"ℹ️  {e}")
        return True
    
    violations = []
    
    for file_path in staged_files:
        path = Path(file_path)
        if path.exists() and path.is_file():
            status = monitor.get_file_status(path)
            if status.status == "ERROR":
                violations.append(status)
    
    if violations:
        print("🚨 COMMIT BLOCKED - FILE SIZE VIOLATIONS DETECTED!")
        print("(GNSS Interactive Demo project only)")
        print("=" * 50)
        print("The following staged files exceed size limits:")
        print()
        
        for violation in violations:
            print(f"❌ {violation.path}")
            print(f"   Lines: {violation.lines}/{violation.limit}")
            print(f"   Over by: {violation.lines - violation.limit} lines")
            print()
        
        print("REQUIRED ACTIONS:")
        print("1. Split large files into smaller components")
        print("2. Extract functions into separate modules")
        print("3. Re-stage files after splitting")
        print()
        print("Commit blocked until violations are resolved.")
        return False
    
    return True

def main():
    """Main pre-commit hook execution."""
    if not check_staged_files():
        sys.exit(1)
    
    print("✅ File size compliance verified - commit allowed")
    sys.exit(0)

if __name__ == "__main__":
    main()