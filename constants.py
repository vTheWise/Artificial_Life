import numpy as np

amplitude = np.pi/4.0
frequency = 1
phaseOffset = 0
amplitude_BackLeg = np.pi/4.0
frequency_BackLeg = 10
phaseOffset_BackLeg = 0
amplitude_FrontLeg = np.pi/4.0
frequency_FrontLeg = 20
phaseOffset_FrontLeg = np.pi/2.0
forLoopIteratorCount = 10000
linspace_start = 0
linspace_stop = 2*np.pi
gravityX = 0
gravityY = 0
gravityZ = -9.8
maxForce = 20
sleepTime = 1/6400
numberOfGenerations = 5
populationSize = 5
motorJointRange = 0.3
color_sensor_link = "Green"
color_nosensor_link = "Blue"
rgba_sensor_link = "0 1.0 0 1.0"
rgba_nosensor_link = "0 0 1.0 1.0"