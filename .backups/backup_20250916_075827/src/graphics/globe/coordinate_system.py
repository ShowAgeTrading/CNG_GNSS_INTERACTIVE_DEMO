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
        """
        Convert latitude/longitude/altitude to 3D Cartesian coordinates.
        
        Args:
            lat: Latitude in degrees [-90, 90]
            lon: Longitude in degrees [-180, 180]
            alt: Altitude in kilometers above sea level
            
        Returns:
            Vec3 with 3D Cartesian coordinates in kilometers
        """
        # Convert to radians
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        # Calculate radius including altitude
        radius = CoordinateSystem.EARTH_RADIUS_KM + alt
        
        # Convert to Cartesian coordinates
        # Panda3D uses Z-up coordinate system
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
        """
        Create transformation matrix for positioning objects on globe surface.
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees  
            alt: Altitude in kilometers
            
        Returns:
            Mat4 transformation matrix
        """
        # Get 3D position
        position = CoordinateSystem.lat_lon_to_cartesian(lat, lon, alt)
        
        # Create rotation to align with surface normal
        # This ensures objects "stand up" on the surface
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        # Create transform matrix
        transform = Mat4.identMat()
        
        # Apply rotation to align with surface
        transform = transform * Mat4.rotateMat(lon, Vec3(0, 0, 1))  # Longitude rotation
        transform = transform * Mat4.rotateMat(lat, Vec3(0, 1, 0))  # Latitude rotation
        
        # Apply translation
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
    def calculate_distance(lat1: float, lon1: float, 
                         lat2: float, lon2: float) -> float:
        """
        Calculate great circle distance between two points on Earth surface.
        
        Args:
            lat1, lon1: First point coordinates in degrees
            lat2, lon2: Second point coordinates in degrees
            
        Returns:
            Distance in kilometers
        """
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        
        c = 2 * math.asin(math.sqrt(a))
        
        return CoordinateSystem.EARTH_RADIUS_KM * c
    
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
        antipodal_lon = CoordinateSystem.normalize_longitude(lon + 180.0)
        
        return antipodal_lat, antipodal_lon