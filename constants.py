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
maxForce = 50
sleepTime = 1/6400
joint_backLeg = "Torso_BackLeg"
joint_frontLeg = "Torso_FrontLeg"
length = 1
width = 1
height = 1
x1 = 0
y1 = 0
z1 = 0.5
numberOfGenerations = 10