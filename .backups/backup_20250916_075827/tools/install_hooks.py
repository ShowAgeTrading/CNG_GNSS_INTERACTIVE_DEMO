#!/usr/bin/env python3
"""
Install Git Hooks for File Size Enforcement
Sets up pre-commit hooks to enforce file size limits
"""

import os
import sys
import shutil
from pathlib import Path

def find_git_hooks_dir():
    """Find the git hooks directory."""
    # Try to find .git directory
    current_dir = Path.cwd()
    
    while current_dir.parent != current_dir:
        git_dir = current_dir / '.git'
        if git_dir.exists():
            if git_dir.is_dir():
                return git_dir / 'hooks'
            else:
                # Handle git worktrees or submodules
                with open(git_dir, 'r') as f:
                    content = f.read().strip()
                    if content.startswith('gitdir:'):
                        git_path = content[8:].strip()
                        return Path(git_path) / 'hooks'
        current_dir = current_dir.parent
    
    return None

def install_pre_commit_hook():
    """Install the pre-commit hook - PROJECT SPECIFIC ONLY."""
    
    # SAFETY CHECK: Only install in GNSS project
    project_markers = [
        Path("planning/templates/UNIVERSAL_CODE_TEMPLATE.md"),
        Path("planning/MASTER_IMPLEMENTATION_PLAN.md")
    ]
    
    if not all(marker.exists() for marker in project_markers):
        print("❌ Error: File size enforcement only available for GNSS Interactive Demo project")
        print("   This prevents interference with other Python projects.")
        return False
    
    hooks_dir = find_git_hooks_dir()
    
    if not hooks_dir:
        print("❌ Error: Not in a git repository")
        return False
    
    if not hooks_dir.exists():
        hooks_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the pre-commit hook script
    hook_script = hooks_dir / 'pre-commit'
    
    # Hook script content that calls our Python script
    hook_content = f"""#!/bin/sh
# File Size Enforcement Pre-Commit Hook
# PROJECT SPECIFIC: GNSS Interactive Demo only
cd "{Path.cwd()}"
python tools/pre_commit_hook.py
"""
    
    # Write the hook script
    with open(hook_script, 'w') as f:
        f.write(hook_content)
    
    # Make it executable (on Unix-like systems)
    if hasattr(os, 'chmod'):
        os.chmod(hook_script, 0o755)
    
    print(f"✅ Pre-commit hook installed: {hook_script}")
    print("ℹ️  This hook only enforces limits in GNSS Interactive Demo project")
    print("ℹ️  Your other Python projects will not be affected")
    return True

def uninstall_pre_commit_hook():
    """Remove the pre-commit hook."""
    hooks_dir = find_git_hooks_dir()
    
    if not hooks_dir:
        print("❌ Error: Not in a git repository")
        return False
    
    hook_script = hooks_dir / 'pre-commit'
    
    if hook_script.exists():
        hook_script.unlink()
        print(f"✅ Pre-commit hook removed: {hook_script}")
        return True
    else:
        print("ℹ️  No pre-commit hook found to remove")
        return True

def check_installation():
    """Check if hooks are properly installed."""
    hooks_dir = find_git_hooks_dir()
    
    if not hooks_dir:
        print("❌ Not in a git repository")
        return False
    
    hook_script = hooks_dir / 'pre-commit'
    
    if hook_script.exists():
        print(f"✅ Pre-commit hook is installed: {hook_script}")
        
        # Check if it's our hook
        with open(hook_script, 'r') as f:
            content = f.read()
            if 'file_size_monitor' in content or 'pre_commit_hook.py' in content:
                print("✅ Hook appears to be our file size enforcement hook")
                return True
            else:
                print("⚠️  Warning: Pre-commit hook exists but is not our file size hook")
                return False
    else:
        print("❌ No pre-commit hook installed")
        return False

def main():
    """Main installer interface."""
    if len(sys.argv) < 2:
        print("Git Hook Installer for File Size Enforcement")
        print("Usage:")
        print("  python install_hooks.py install   - Install pre-commit hook")
        print("  python install_hooks.py uninstall - Remove pre-commit hook")
        print("  python install_hooks.py check     - Check installation status")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'install':
        if install_pre_commit_hook():
            print()
            print("🎉 File size enforcement is now active!")
            print("Commits will be blocked if files exceed size limits.")
            print()
            print("To test the installation:")
            print("  python tools/file_size_monitor.py --check")
        else:
            sys.exit(1)
    
    elif command == 'uninstall':
        if uninstall_pre_commit_hook():
            print("File size enforcement hooks removed.")
        else:
            sys.exit(1)
    
    elif command == 'check':
        if not check_installation():
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        print("Use: install, uninstall, or check")
        sys.exit(1)

if __name__ == "__main__":
    main()