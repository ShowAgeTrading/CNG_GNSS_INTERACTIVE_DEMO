# Universal Code Template - CNG GNSS Interactive Demo
**Version:** 1.0  
**Created:** 2025-09-15  
**Author:** GitHub Copilot  
**Purpose:** Strict template enforcing modular, referenceable, and maintainable code structure  

---

## File Header Template (MANDATORY FOR ALL FILES)

```python
#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: [FILENAME].[EXTENSION]
Purpose: [BRIEF DESCRIPTION - MAX 80 CHARS]
Author: GitHub Copilot
Created: [YYYY-MM-DD]
Last Modified: [YYYY-MM-DD]
Version: [SEMANTIC VERSION]

Dependencies:
    - [PACKAGE_NAME] ([VERSION]) - [PURPOSE]
    - [LOCAL_MODULE] - [PURPOSE]

References:
    - Related Files: [LIST_OF_FILES]
    - External Links: [URLS_IF_ANY]
    - Design Docs: [PLANNING_FILES]

TODO/FIXME:
    - [ITEM_1] (Priority: High/Medium/Low)
    - [ITEM_2] (Priority: High/Medium/Low)

Line Count: [CURRENT_LINES]/200 (Soft Limit: 180)
"""
```

---

## Naming Conventions (STRICTLY ENFORCED)

### Files and Directories
- **Modules/Packages:** `snake_case` (e.g., `satellite_manager.py`)
- **Data Files:** `snake_case` (e.g., `satellite_config.json`)
- **Documentation:** `SCREAMING_SNAKE_CASE` (e.g., `PHASE_01_SETUP.md`)
- **Directories:** `snake_case` (e.g., `ui_components/`)

### Python Code
- **Classes:** `PascalCase` (e.g., `SatelliteRenderer`)
- **Functions/Methods:** `snake_case` (e.g., `update_satellite_position()`)
- **Variables:** `snake_case` (e.g., `current_time`)
- **Constants:** `SCREAMING_SNAKE_CASE` (e.g., `MAX_SATELLITES`)
- **Private Members:** Leading underscore (e.g., `_internal_state`)

### Special Prefixes
- **Event Names:** `on_` (e.g., `on_satellite_selected`)
- **Plugin Classes:** `Plugin` suffix (e.g., `NtripPlugin`)
- **Test Files:** `test_` prefix (e.g., `test_satellite_manager.py`)

---

## Code Structure Template

### Python Module Structure
```python
# 1. IMPORTS (Max 15 lines)
import standard_library_module
from third_party import PackageName
from .local_module import LocalClass

# 2. CONSTANTS (Max 10 lines)
MAX_FILE_LINES = 200
SOFT_WARNING_LINES = 180

# 3. TYPE HINTS & ENUMS (Max 15 lines)
from typing import Dict, List, Optional, Union
from enum import Enum

class StateEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# 4. GLOBAL VARIABLES (Max 5 lines - AVOID IF POSSIBLE)
_global_instance: Optional['ClassName'] = None

# 5. CLASSES (Max 120 lines total)
class MainClass:
    """
    Brief description of the class purpose.
    
    Attributes:
        attr_name (type): Description
        
    References:
        - Related Classes: [LIST]
        - Design Pattern: [PATTERN_NAME]
    """
    
    def __init__(self, param: str) -> None:
        """Initialize with validation and documentation."""
        pass
    
    def public_method(self) -> None:
        """
        Public method with clear purpose.
        
        Returns:
            type: Description
            
        Raises:
            ExceptionType: When this happens
        """
        pass
    
    def _private_method(self) -> None:
        """Private method for internal use only."""
        pass

# 6. FUNCTIONS (Max 30 lines total)
def utility_function(param: str) -> bool:
    """
    Standalone utility function.
    
    Args:
        param: Description
        
    Returns:
        bool: Description
    """
    pass

# 7. MAIN EXECUTION (Max 10 lines)
if __name__ == "__main__":
    main()
```

### Maximum Line Limits (STRICTLY ENFORCED)
- **File Total:** 200 lines (hard limit)
- **Soft Warning:** 180 lines
- **Function/Method:** 30 lines maximum
- **Class:** 120 lines maximum (split if larger)
- **Import Section:** 15 lines maximum

---

## Documentation Standards

### Docstring Template (Sphinx Style)
```python
def function_name(param1: str, param2: int = 0) -> Dict[str, Any]:
    """
    Brief description in one line.
    
    Longer description if needed, explaining the purpose,
    algorithm, or important implementation details.
    
    Args:
        param1 (str): Description of first parameter
        param2 (int, optional): Description with default. Defaults to 0.
        
    Returns:
        Dict[str, Any]: Description of return value structure
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is negative
        
    Example:
        >>> result = function_name("test", 5)
        >>> print(result["status"])
        'success'
        
    References:
        - :func:`related_function`
        - :class:`RelatedClass`
        - See Also: planning/phases/PHASE_XX.md
        
    TODO:
        - Add validation for param2 range
        - Optimize performance for large inputs
    """
```

---

## File Splitting Rules

### When to Split (Any of these triggers)
1. File reaches 180 lines (soft warning)
2. Class has more than 5 public methods
3. Module has more than 3 classes
4. Function exceeds 30 lines
5. Import section exceeds 15 lines

### How to Split
1. **Large Classes:** Split by responsibility into multiple classes
2. **Many Functions:** Group related functions into separate modules
3. **Long Functions:** Extract helper functions or break into steps
4. **Many Imports:** Create a separate `dependencies.py` module

### Split Documentation
```python
# In original file header:
"""
Split History:
    - 2025-09-15: Extracted HelperClass to helper_module.py
    - 2025-09-16: Moved utility functions to utils.py
"""

# In new file header:
"""
Split From: original_module.py (2025-09-15)
Reason: Class exceeded 120 lines, extracted helper functionality
"""
```

---

## Error Handling Template

```python
# Standard exception pattern
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    # Handle gracefully or re-raise with context
    raise RuntimeError(f"Failed to complete operation: {e}") from e
except Exception as e:
    logger.critical(f"Unexpected error: {e}")
    # Log and re-raise for debugging
    raise

# Validation pattern
def validate_input(value: Any) -> None:
    """Validate input with clear error messages."""
    if not isinstance(value, expected_type):
        raise TypeError(f"Expected {expected_type}, got {type(value)}")
    if not meets_criteria(value):
        raise ValueError(f"Value {value} does not meet criteria")
```

---

## Hot-Reload Compliance

### Plugin Interface Template
```python
class PluginInterface:
    """Base interface for hot-reloadable plugins."""
    
    def __init__(self) -> None:
        self.name: str = ""
        self.version: str = "1.0.0"
        self.dependencies: List[str] = []
    
    def load(self) -> bool:
        """Called when plugin is loaded/reloaded."""
        pass
    
    def unload(self) -> bool:
        """Called before plugin is unloaded/reloaded."""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Return plugin metadata."""
        return {
            "name": self.name,
            "version": self.version,
            "dependencies": self.dependencies
        }
```

### Hot-Reload Markers
```python
# Mark classes/functions for hot-reload
__hot_reload__ = True

# Mark state that should persist across reloads
__persistent_state__ = ["user_preferences", "active_sessions"]
```

---

## Reference System

### Cross-File References
```python
# In docstrings and comments:
# See: core/event_bus.py::EventBus.publish()
# Related: ui/controls.py::BaseControl
# Config: data/satellite_config.json
# Design: planning/phases/PHASE_03_GRAPHICS.md
# Test: tests/test_satellite_manager.py::test_orbit_calculation
```

### Dependency Documentation
```python
# At top of file in header
"""
Dependencies:
    External:
        - panda3d (1.10.13) - 3D graphics engine
        - numpy (1.24.0) - Mathematical operations
    Internal:
        - core.event_bus - Event communication
        - graphics.materials - Texture management
    Data:
        - data/satellite_constellations.json - Orbital parameters
    Assets:
        - assets/models/satellite.obj - 3D model
"""
```

---

## Testing Template

### Test File Structure
```python
#!/usr/bin/env python3
"""
Test File: test_[MODULE_NAME].py
Purpose: Unit tests for [MODULE_NAME] functionality
Created: [DATE]
Coverage Target: 90%+

Test Categories:
    - Unit Tests: Individual function/method testing
    - Integration Tests: Module interaction testing
    - Edge Cases: Boundary and error conditions
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from module_under_test import ClassUnderTest

class TestClassName(unittest.TestCase):
    """Test suite for ClassName functionality."""
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.test_instance = ClassUnderTest()
    
    def tearDown(self) -> None:
        """Clean up after each test method."""
        pass
    
    def test_basic_functionality(self) -> None:
        """Test basic functionality with valid inputs."""
        # Arrange
        input_data = "test_input"
        expected_result = "expected_output"
        
        # Act
        result = self.test_instance.method(input_data)
        
        # Assert
        self.assertEqual(result, expected_result)
    
    def test_edge_case_empty_input(self) -> None:
        """Test behavior with empty input."""
        with self.assertRaises(ValueError):
            self.test_instance.method("")
    
    @patch('module_under_test.external_dependency')
    def test_with_mock(self, mock_dependency) -> None:
        """Test with mocked external dependency."""
        mock_dependency.return_value = "mocked_result"
        result = self.test_instance.method_with_dependency()
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
```

---

## Enforcement Rules

### Automated Checks (To Be Implemented)
1. **Line Count Check:** Fail if file > 200 lines
2. **Function Length Check:** Fail if function > 30 lines  
3. **Naming Convention Check:** Fail if names don't match patterns
4. **Required Header Check:** Fail if header template missing
5. **Reference Check:** Warn if cross-references are broken

### Manual Review Checklist
- [ ] File header complete and accurate
- [ ] All functions have docstrings
- [ ] Cross-references are valid
- [ ] TODO/FIXME items are documented
- [ ] Error handling is appropriate
- [ ] Code follows naming conventions
- [ ] Line limits are respected
- [ ] Dependencies are documented

---

## Template File Exception

**Note:** This template file is exempt from the 200-line limit and follows the 500-line limit for planning documents, as it serves as the master reference for all code structure.

**Template Compliance:** This template file follows all applicable rules defined within it.  
**Last Updated:** 2025-09-15  
**Version:** 1.0  
**Actual Line Count:** 410/500 (Template files use 500-line limit)