"""
Core Panda3D utilities for basic node operations and transforms.

Essential functions extracted from graphics components for common Panda3D operations.
Split to maintain file size compliance.
"""

import logging
from typing import Optional, Any, Tuple

try:
    from panda3d.core import NodePath, Vec3, Point3
    PANDA3D_AVAILABLE = True
except ImportError:
    NodePath = None
    Vec3 = None  
    Point3 = None
    PANDA3D_AVAILABLE = False

logger = logging.getLogger(__name__)


def setup_node(node_path: Optional[Any], name: str = "node", 
               position: Tuple[float, float, float] = (0, 0, 0),
               scale: Tuple[float, float, float] = (1, 1, 1)) -> Optional[Any]:
    """Set up a Panda3D node with basic configuration."""
    if not PANDA3D_AVAILABLE or node_path is None:
        return None
    
    try:
        node_path.setName(name)
        node_path.setPos(*position)
        node_path.setScale(*scale)
        return node_path
    except Exception as e:
        logger.error(f"Error setting up node: {e}")
        return None


def apply_transform(node_path: Optional[Any], 
                   position: Optional[Tuple[float, float, float]] = None,
                   rotation: Optional[Tuple[float, float, float]] = None,
                   scale: Optional[Tuple[float, float, float]] = None) -> bool:
    """Apply transforms to a Panda3D node path."""
    if not PANDA3D_AVAILABLE or node_path is None:
        return False
    
    try:
        if position:
            node_path.setPos(*position)
        if rotation:
            node_path.setHpr(*rotation)
        if scale:
            node_path.setScale(*scale)
        return True
    except Exception as e:
        logger.error(f"Error applying transform: {e}")
        return False


def get_node_bounds(node_path: Optional[Any]) -> Optional[Tuple[Point3, Point3]]:
    """Get tight bounds of a node."""
    if not PANDA3D_AVAILABLE or node_path is None:
        return None
    
    try:
        bounds = node_path.getTightBounds()
        return bounds if bounds else None
    except Exception as e:
        logger.error(f"Error getting bounds: {e}")
        return None


def optimize_node_for_performance(node_path: Optional[Any]) -> bool:
    """Apply performance optimizations to a node."""
    if not PANDA3D_AVAILABLE or node_path is None:
        return False
    
    try:
        node_path.flattenStrong()
        return True
    except Exception as e:
        logger.error(f"Error optimizing node: {e}")
        return False
