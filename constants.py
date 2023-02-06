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
forLoopIteratorCount = 3000
linspace_start = 0
linspace_stop = 2*np.pi
gravityX = 0
gravityY = 0
gravityZ = -9.8
maxForce = 100
sleepTime = 1/6400
numberOfGenerations = 10
populationSize = 10
numSensorNeurons = 2
numMotorNeurons = 6
motorJointRange = 0.1
numRobots = 3

color_sensor_link = "Green"
color_sensor_link_root = color_sensor_link
color_nosensor_link = "Blue"
color_nosensor_link_root = color_nosensor_link

rgba_sensor_link = "0 0.5 0 1.0"
rgba_sensor_link_root = rgba_sensor_link
rgba_nosensor_link = "0 0 1.0 1.0"
rgba_nosensor_link_root = rgba_nosensor_link

ball_pos = [-numRobots*2, numRobots*2, 3]

fitnessFunction = 'roboSwarm_ToTheBall'
'''
roboSwarm_WalkAway
roboSwarm_ToTheBall
'''
if fitnessFunction == 'roboSwarm_WalkAway':
    color_sensor_link_root = "Yellow"
    color_nosensor_link_root = "Pink"
    rgba_sensor_link_root = "1.0 1.0 0 1.0"
    rgba_nosensor_link_root = "1.0 0 1.0 1.0"