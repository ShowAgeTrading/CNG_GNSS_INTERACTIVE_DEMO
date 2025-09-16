# File Size Compliance Refactoring Memo
**Created:** September 15, 2025  
**Branch:** feature/file-size-compliance-refactor  
**Status:** Implementation Phase

## Purpose
Refactor oversized graphics files to meet 229-line code limit while maintaining functionality.

## Current Violations (158 lines total over limit)
- `src\graphics\graphics_manager.py`: 294/229 lines (65 over)
- `src\graphics\globe\globe_renderer.py`: 310/229 lines (81 over) 
- `src\graphics\globe\texture_manager.py`: 239/229 lines (10 over)
- `src\graphics\globe\coordinate_system.py`: 231/229 lines (2 over)

## Risks
- **HIGH:** Breaking graphics initialization chain
- **MEDIUM:** Import path changes affecting other modules  
- **LOW:** Performance impact from additional module imports

## Checkpoint Commits
1. ✅ **Create memo and branch** - Document plan
2. ⏳ **Extract material_manager.py** - Reduce globe_renderer by 80 lines
3. ⏳ **Extract model_loader.py** - Reduce globe_renderer by remaining excess
4. ⏳ **Extract subsystem_factory.py** - Reduce graphics_manager by 65 lines
5. ⏳ **Trim documentation** - Fix texture_manager, coordinate_system
6. ⏳ **Integration testing** - Verify all systems work
7. ⏳ **Documentation updates** - Update import references

## Rollback Steps
1. `git checkout master`
2. `git branch -D feature/file-size-compliance-refactor` 
3. Verify with `python tools/file_size_monitor.py --check`

## Test Commands (Run after each checkpoint)
```powershell
# File compliance check
python tools/file_size_monitor.py --check

# Import verification  
python -c "from src.graphics.graphics_manager import GraphicsManager; print('Import OK')"

# Integration test
python -m pytest tests/integration/test_phase2_integration.py
```

## Success Criteria
- [ ] All files under 229-line limit
- [ ] All existing tests pass
- [ ] Graphics system initializes without errors
- [ ] No broken import paths

## Implementation Notes
- Working in activated venv with Panda3D 1.10.15
- Target: Remove 158 lines total across 4 files
- Priority: globe_renderer.py (81 lines) → graphics_manager.py (65 lines) → small fixes