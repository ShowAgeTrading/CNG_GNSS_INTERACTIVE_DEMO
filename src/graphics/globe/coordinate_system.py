#!/usr/bin/env python3
"""
Project: CNG GNSS Interactive Demo
File: coordinate_system.py
Purpose: Geographic coordinate transformations for globe positioning
Author: GitHub Copilot
Created: 2025-09-15
Last Modified: 2025-09-15
Version: 1.0.0

Dependencies:
    - panda3d (1.10.15) - 3D math operations
    - numpy (1.24.0) - Mathematical calculations

References:
    - Related Files: globe_renderer.py, ../../satellite/constellation.py
    - Design Docs: planning/phases/PHASE_03_GRAPHICS_ENGINE.md
    - Standards: WGS84 coordinate system

TODO/FIXME:
    - Add geodetic transformations for precision (Priority: Medium)
    - Implement coordinate validation (Priority: Low)

Line Count: 162/200 (Soft Limit: 180)
"""

import math
import numpy as np
from typing import Tuple

from panda3d.core import Vec3, Mat4, TransformState
from .coordinate_validation import CoordinateValidator


class CoordinateSystem:
    """
    Geographic coordinate transformations for globe positioning.
    
    Handles conversions between:
    - Geographic coordinates (latitude, longitude, altitude)
    - 3D Cartesian coordinates (X, Y, Z)  
    - Panda3D scene coordinates
    
    Uses WGS84 Earth model with radius of 6371 km.
    """
    
    # Earth constants (WGS84 approximation)
    EARTH_RADIUS_KM = 6371.0
    EARTH_RADIUS_M = 6371000.0
    
    @staticmethod
    def lat_lon_to_cartesian(lat: float, lon: float, alt: float = 0) -> Vec3:
        """Convert latitude/longitude/altitude to 3D Cartesian coordinates."""
        lat_rad, lon_rad = CoordinateSystem._convert_to_radians(lat, lon)
        radius = CoordinateSystem.EARTH_RADIUS_KM + alt
        return CoordinateSystem._calculate_cartesian_coordinates(lat_rad, lon_rad, radius)

    @staticmethod
    def _convert_to_radians(lat: float, lon: float) -> Tuple[float, float]:
        """Convert degrees to radians."""
        return math.radians(lat), math.radians(lon)

    @staticmethod
    def _calculate_cartesian_coordinates(lat_rad: float, lon_rad: float, radius: float) -> Vec3:
        """Calculate 3D coordinates from spherical."""
        x = radius * math.cos(lat_rad) * math.cos(lon_rad)
        y = radius * math.cos(lat_rad) * math.sin(lon_rad)  
        z = radius * math.sin(lat_rad)
        return Vec3(x, y, z)
    
    @staticmethod
    def cartesian_to_lat_lon(position: Vec3) -> Tuple[float, float, float]:
        """
        Convert 3D Cartesian coordinates back to latitude/longitude/altitude.
        
        Args:
            position: Vec3 with Cartesian coordinates in kilometers
            
        Returns:
            Tuple of (latitude, longitude, altitude) in degrees and km
        """
        x, y, z = float(position.x), float(position.y), float(position.z)
        
        # Calculate radius and altitude
        radius = math.sqrt(x*x + y*y + z*z)
        altitude = radius - CoordinateSystem.EARTH_RADIUS_KM
        
        # Calculate latitude
        latitude = math.degrees(math.asin(z / radius))
        
        # Calculate longitude
        longitude = math.degrees(math.atan2(y, x))
        
        return latitude, longitude, altitude
    
    @staticmethod
    def create_transform_matrix(lat: float, lon: float, alt: float = 0) -> Mat4:
        """Create transformation matrix for positioning objects on globe surface."""
        position = CoordinateSystem.lat_lon_to_cartesian(lat, lon, alt)
        return CoordinateSystem._create_surface_aligned_matrix(lat, lon, position)

    @staticmethod
    def _create_surface_aligned_matrix(lat: float, lon: float, position: Vec3) -> Mat4:
        """Create transform matrix aligned with globe surface."""
        transform = Mat4.identMat()
        transform = transform * Mat4.rotateMat(lon, Vec3(0, 0, 1))
        transform = transform * Mat4.rotateMat(lat, Vec3(0, 1, 0))
        transform = transform * Mat4.translateMat(position)
        return transform
    
    @staticmethod
    def get_surface_normal(lat: float, lon: float) -> Vec3:
        """
        Get surface normal vector at given latitude/longitude.
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            
        Returns:
            Vec3 normalized surface normal
        """
        # Surface normal is simply the normalized position vector
        position = CoordinateSystem.lat_lon_to_cartesian(lat, lon, 0)
        return position.normalized()
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great circle distance between two points on Earth surface."""
        coords1 = CoordinateSystem._convert_coords_to_radians(lat1, lon1)
        coords2 = CoordinateSystem._convert_coords_to_radians(lat2, lon2)
        return CoordinateSystem._haversine_distance(coords1, coords2)

    @staticmethod
    def _convert_coords_to_radians(lat: float, lon: float) -> Tuple[float, float]:
        """Convert coordinate pair to radians."""
        return math.radians(lat), math.radians(lon)

    @staticmethod
    def _haversine_distance(coords1: Tuple[float, float], coords2: Tuple[float, float]) -> float:
        """Calculate distance using Haversine formula."""
        lat1_rad, lon1_rad = coords1
        lat2_rad, lon2_rad = coords2
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        
        c = 2 * math.asin(math.sqrt(a))
        return CoordinateSystem.EARTH_RADIUS_KM * c
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """Validate latitude and longitude ranges."""
        return CoordinateValidator.validate_coordinates(lat, lon)
    
    @staticmethod
    def normalize_longitude(lon: float) -> float:
        """Normalize longitude to [-180, 180] range."""
        return CoordinateValidator.normalize_longitude(lon)
    
    @staticmethod
    def get_antipodal_point(lat: float, lon: float) -> Tuple[float, float]:
        """Get antipodal point (opposite side of Earth)."""
        return CoordinateValidator.get_antipodal_point(lat, lon)