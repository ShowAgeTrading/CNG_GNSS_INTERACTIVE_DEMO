#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: component_interface.py
Purpose: Base interface for all application components
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - abc - Abstract base class
    - typing - Type hints

References:
    - Related Files: app_framework.py
    - Design Docs: planning/phases/PHASE_02_CORE_ARCHITECTURE.md

Line Count: 35/200 (Soft Limit: 180)
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app_framework import Application

class ComponentInterface(ABC):
    """Base interface for all application components."""
    
    @abstractmethod
    def initialize(self, app: 'Application') -> bool:
        """Initialize component with app reference."""
        pass
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update component each frame."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Cleanup component resources."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Component name for identification."""
        pass