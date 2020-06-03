# Smooth Ride

Smooth ride is a road smoothness data logging pipeline.

Pipeline:
-accelerometers collect vibration data while driving to csv files
  -training data: road conditions (good, fair, poor) are marked while driving
-gps logger records coodinates to csv files
-gps and accelerometer is cleansed and joined 
