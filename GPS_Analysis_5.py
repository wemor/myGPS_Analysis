# GPS Data Analysis with Python
# Part 5: Plotting Elevation, Climb Rate, and Velocity
# Author: Werner Moretti
# Date: 2021-09-26
# Update: 2021-09-26
# Version: 1.0
# Description: This script reads a GPX file, extracts the elevation, climb rate, and velocity data, and plots the data.
# The elevation profile is plotted with the original and smoothed elevation data.
# The climb rate is plotted with the original and smoothed climb rate data.
# The velocity is plotted with the original and smoothed velocity data.
# The script uses the gpxpy library to parse the GPX file and the geopy library to calculate the distance between two points.
# The script also uses numpy and matplotlib to perform calculations and plot the data.

import gpxpy
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from geopy.distance import geodesic

# Function to calculate velocity
def calculate_velocity(points):
    velocities = []
    times = []
    for i in range(1, len(points)):
        point1 = points[i-1]
        point2 = points[i]
        
        # Calculate distance in meters
        coords_1 = (point1.latitude, point1.longitude)
        coords_2 = (point2.latitude, point2.longitude)
        distance = geodesic(coords_1, coords_2).meters
        
        # Calculate time difference in seconds
        time_diff = (point2.time - point1.time).total_seconds()
        
        # Calculate velocity in m/s
        if time_diff > 0:
            velocity = distance / time_diff
            velocities.append(velocity)
            times.append((point2.time - points[0].time).total_seconds() / 60)  # Time in minutes since start
    
    return np.array(times), np.array(velocities)

# Function to calculate climb rate
def calculate_climb_rate(points):
    climb_rates = []
    times = []
    for i in range(1, len(points)):
        point1 = points[i-1]
        point2 = points[i]
        
        # Calculate altitude difference in meters
        altitude_diff = point2.elevation - point1.elevation
        
        # Calculate time difference in seconds
        time_diff = (point2.time - point1.time).total_seconds()
        
        # Calculate climb rate in m/s
        if time_diff > 0:
            climb_rate = altitude_diff / time_diff
            climb_rates.append(climb_rate)
            times.append((point2.time - points[0].time).total_seconds() / 60)  # Time in minutes since start
    
    return np.array(times), np.array(climb_rates)

# Function to smooth data using a moving average
def smooth_data(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

# Open the GPX file
FileName = "C:/Users/wmore/OneDrive/Engineering/06-Prog_Eng/python/PycharmProjects/GPS_Analysis/Mountainbiking-Stans.gpx"
with open(FileName, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Extract track metadata (name, type, and time)
track_name = gpx.tracks[0].name
track_type = gpx.tracks[0].type
track_time = gpx.tracks[0].segments[0].points[0].time
track_date = track_time.date()

# Extract points from the first segment of the first track
points = gpx.tracks[0].segments[0].points

# Calculate elevation profile
elevations = [point.elevation for point in points]
elevation_times = [(point.time - points[0].time).total_seconds() / 60 for point in points]  # Time in minutes since start

# Calculate velocity and time
times, velocities = calculate_velocity(points)

# Calculate climb rate and time
climb_times, climb_rates = calculate_climb_rate(points)

# Smooth the data using a simple moving average
window_size = 5
smoothed_climb_rates = smooth_data(climb_rates, window_size)
smoothed_velocities = smooth_data(velocities, window_size)
smoothed_elevations = smooth_data(elevations, window_size)

# Plot elevation, climb rate, and velocity
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# Plot elevation profile
axs[0].plot(elevation_times, elevations, label='Original Elevation', alpha=0.5, color='green')
axs[0].plot(elevation_times[:len(smoothed_elevations)], smoothed_elevations, label='Smoothed Elevation', color='orange')
axs[0].set_title(f'Elevation Profile for {track_name} ({track_type}) on {track_date}')
axs[0].set_xlabel('Time (minutes)')
axs[0].set_ylabel('Elevation (m)')
axs[0].legend()
axs[0].grid(True)

# Plot climb rate
axs[1].plot(climb_times, climb_rates, label='Original Climb Rate', alpha=0.5, color='green')
axs[1].plot(climb_times[:len(smoothed_climb_rates)], smoothed_climb_rates, label='Smoothed Climb Rate', color='orange')
axs[1].set_title(f'Climb Rate for {track_name} ({track_type}) on {track_date}')
axs[1].set_xlabel('Time (minutes)')
axs[1].set_ylabel('Climb Rate (m/s)')
axs[1].legend()
axs[1].grid(True)

# Plot velocity
axs[2].plot(times, velocities, label='Original Velocity', alpha=0.5, color='blue')
axs[2].plot(times[:len(smoothed_velocities)], smoothed_velocities, label='Smoothed Velocity', color='red')
axs[2].set_title(f'Velocity for {track_name} ({track_type}) on {track_date}')
axs[2].set_xlabel('Time (minutes)')
axs[2].set_ylabel('Velocity (m/s)')
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()