#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: coordinate_validation.py
Purpose: Coordinate validation and normalization utilities
Author: GitHub Copilot
Created: 2025-09-16
Version: 1.0.0

Line Count: Target <80 lines
"""

from typing import Tuple


class CoordinateValidator:
    """Utilities for validating and normalizing geographic coordinates."""
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """
        Validate latitude and longitude ranges.
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            
        Returns:
            True if coordinates are valid
        """
        return (-90.0 <= lat <= 90.0) and (-180.0 <= lon <= 180.0)
    
    @staticmethod
    def normalize_longitude(lon: float) -> float:
        """
        Normalize longitude to [-180, 180] range.
        
        Args:
            lon: Longitude in degrees
            
        Returns:
            Normalized longitude
        """
        while lon > 180.0:
            lon -= 360.0
        while lon < -180.0:
            lon += 360.0
        return lon
    
    @staticmethod
    def get_antipodal_point(lat: float, lon: float) -> Tuple[float, float]:
        """
        Get antipodal point (opposite side of Earth).
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            
        Returns:
            Tuple of (antipodal_lat, antipodal_lon) in degrees
        """
        antipodal_lat = -lat
        antipodal_lon = CoordinateValidator.normalize_longitude(lon + 180.0)
        
        return antipodal_lat, antipodal_lon
    
    @staticmethod
    def validate_altitude(altitude: float, max_altitude: float = 1000.0) -> bool:
        """
        Validate altitude range.
        
        Args:
            altitude: Altitude in kilometers
            max_altitude: Maximum allowed altitude
            
        Returns:
            True if altitude is valid
        """
        return -11.0 <= altitude <= max_altitude  # Dead Sea to max satellite altitude