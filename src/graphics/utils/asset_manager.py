"""
Asset management utilities for path resolution, validation, and caching.

This module contains utilities extracted from texture_manager.py and globe_renderer.py
to provide centralized asset management across graphics components.
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class AssetManager:
    """Asset management utilities for graphics resources."""
    
    def __init__(self, asset_root: Optional[Path] = None):
        """Initialize asset manager."""
        self.asset_root = asset_root or Path("assets")
        self._cache: Dict[str, Any] = {}
        self._loading_queue: List[str] = []
        
        logger.debug(f"AssetManager initialized with root: {self.asset_root}")
    
    def resolve_path(self, relative_path: str) -> Path:
        """
        Resolve asset path from relative path.
        
        Args:
            relative_path: Path relative to asset root
            
        Returns:
            Full resolved path
        """
        return self.asset_root / relative_path
    
    def resolve_texture_path(self, texture_type: str, texture_file: str) -> Path:
        """
        Resolve path for texture assets.
        
        Args:
            texture_type: Type of texture (earth, models, etc.)
            texture_file: Filename or relative path to texture
            
        Returns:
            Full path to texture file
        """
        return self.asset_root / "textures" / texture_type / texture_file
    
    def resolve_model_path(self, model_category: str, model_file: str) -> Path:
        """
        Resolve path for model assets.
        
        Args:
            model_category: Category of model (earth, receivers, etc.)
            model_file: Filename or relative path to model
            
        Returns:
            Full path to model file
        """
        return self.asset_root / "models" / model_category / model_file
    
    def validate_asset(self, asset_path: Path) -> bool:
        """
        Validate that asset exists and is readable.
        
        Args:
            asset_path: Path to asset file
            
        Returns:
            True if asset exists and is accessible
        """
        try:
            if not asset_path.exists():
                logger.warning(f"Asset file not found: {asset_path}")
                return False
            
            if not asset_path.is_file():
                logger.warning(f"Asset path is not a file: {asset_path}")
                return False
            
            # Try to read first few bytes to check accessibility
            with open(asset_path, 'rb') as f:
                f.read(1)
            
            return True
        except Exception as e:
            logger.error(f"Asset validation failed for {asset_path}: {e}")
            return False
    
    def get_cached_asset(self, asset_key: str) -> Optional[Any]:
        """
        Get cached asset data.
        
        Args:
            asset_key: Unique key for cached asset
            
        Returns:
            Cached asset data or None if not found
        """
        return self._cache.get(asset_key)
    
    def cache_asset(self, asset_key: str, asset_data: Any) -> None:
        """
        Cache asset data for future use.
        
        Args:
            asset_key: Unique key for caching
            asset_data: Asset data to cache
        """
        self._cache[asset_key] = asset_data
        logger.debug(f"Cached asset: {asset_key}")
    
    def is_asset_cached(self, asset_key: str) -> bool:
        """
        Check if asset is already cached.
        
        Args:
            asset_key: Unique key to check
            
        Returns:
            True if asset is cached
        """
        return asset_key in self._cache
    
    def clear_cache(self) -> None:
        """Clear all cached assets."""
        cache_size = len(self._cache)
        self._cache.clear()
        logger.info(f"Cleared asset cache ({cache_size} items)")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache information
        """
        return {
            'cached_items': len(self._cache),
            'cache_keys': list(self._cache.keys()),
            'queue_size': len(self._loading_queue)
        }
    
    def add_to_loading_queue(self, asset_key: str) -> None:
        """Add asset to loading queue."""
        if asset_key not in self._loading_queue:
            self._loading_queue.append(asset_key)
    
    def remove_from_loading_queue(self, asset_key: str) -> None:
        """Remove asset from loading queue."""
        if asset_key in self._loading_queue:
            self._loading_queue.remove(asset_key)