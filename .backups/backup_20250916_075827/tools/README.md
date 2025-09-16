# File Size Enforcement Tools

This directory contains **project-specific enforcement tools** that ONLY work in the GNSS Interactive Demo project. They will NOT interfere with your other Python projects.

## 🔒 PROJECT-SPECIFIC SAFETY

**These tools are designed to ONLY activate in this specific project:**
- Checks for project-specific marker files before activating
- Only monitors files within the project structure (`src/`, `planning/`)
- Will not affect your other Python files or projects
- Git hooks only install/work in this repository

## Tools Overview

### `file_size_monitor.py` - Main Monitoring Tool
**Purpose:** Scan and monitor file sizes ONLY in GNSS project structure
**Safety Features:**
- ✅ Only monitors `src/**/*.py` (not all Python files)
- ✅ Only monitors `planning/**/*.md` 
- ✅ Ignores files outside project structure
- ✅ Requires project marker files to activate

**Usage:**
```bash
# Generate detailed report (project-specific only)
python tools/file_size_monitor.py --report

# Quick compliance check
python tools/file_size_monitor.py --check

# Enforce limits (only for this project)
python tools/file_size_monitor.py --enforce
```

### `pre_commit_hook.py` - Git Integration
**Purpose:** Prevent commits that violate file size limits IN THIS PROJECT ONLY
**Safety Features:**
- ✅ Checks project markers before enforcing
- ✅ Only blocks commits in GNSS project
- ✅ Shows clear message when disabled in other projects

### `install_hooks.py` - Hook Installation
**Purpose:** Install git hooks ONLY for this project
**Safety Features:**
- ✅ Refuses to install if not in GNSS project
- ✅ Hook script includes project detection
- ✅ Clear messaging about project-specific nature

**Usage:**
```bash
# Install enforcement hooks (project-specific only)
python tools/install_hooks.py install

# Check if hooks are installed
python tools/install_hooks.py check

# Remove hooks
python tools/install_hooks.py uninstall
```

## File Size Limits Enforced (GNSS Project Only)

| File Type | Limit | Project-Specific Paths |
|-----------|-------|------------------------|
| Source Code | 200 lines | `src/**/*.py` only |
| Planning Docs | 500 lines | `planning/**/*.md` only |
| Template Files | 500 lines | `planning/templates/**/*.md` only |
| Config Files | 100 lines | Root `*.json`, `*.yaml` only |

## Project Detection

The tools check for these marker files to confirm this is the GNSS project:
- `planning/templates/UNIVERSAL_CODE_TEMPLATE.md`
- `planning/MASTER_IMPLEMENTATION_PLAN.md`
- `tools/file_size_monitor.py`

**If these don't exist, the tools will NOT activate.**

## Your Other Projects Are Safe

**What happens in other projects:**
- ✅ Monitoring tools show: "File size monitoring disabled - not in GNSS project"
- ✅ Git hooks show: "File size enforcement disabled - not in GNSS project"  
- ✅ No limits applied to any files
- ✅ No interference with your normal development

## Example Safe Behavior

**In another Python project:**
```bash
cd /your/other/project
python /path/to/tools/file_size_monitor.py --check
# Output: "⚠️  File size monitoring disabled - not in GNSS Interactive Demo project"
# Exit code: 0 (success, no interference)
```

**In GNSS project:**
```bash
cd /CNG_GNSS_INTERACTIVE_DEMO
python tools/file_size_monitor.py --check
# Output: Actual compliance checking with project-specific limits
```

This ensures **zero interference** with your other Python development work while providing strict enforcement only where needed.