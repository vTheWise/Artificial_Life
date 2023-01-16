import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import matplotlib.pylab as plab

amplitude_BackLeg = np.pi/4.0
frequency_BackLeg = 5
phaseOffset_BackLeg = 0
amplitude_FrontLeg = np.pi/4.0
frequency_FrontLeg = 5
phaseOffset_FrontLeg = np.pi/2.0

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
robotId = p.loadURDF("body.urdf")
print('robotId::::', robotId)

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)
targetAngles_BackLeg = np.linspace(0, 2*np.pi, 1000)
targetAngles_FrontLeg = np.linspace(0, 2*np.pi, 1000)
#targetAngles = np.interp(targetAngles, (targetAngles.min(), targetAngles.max()), (-np.pi/4.0, np.pi/4.0))
for ix in range(len(targetAngles_BackLeg)):
    targetAngles_BackLeg[ix] = amplitude_BackLeg * np.sin(frequency_BackLeg * targetAngles_BackLeg[ix] + phaseOffset_BackLeg)
for ix in range(len(targetAngles_FrontLeg)):
    targetAngles_FrontLeg[ix] = amplitude_FrontLeg * np.sin(frequency_FrontLeg * targetAngles_FrontLeg[ix] + phaseOffset_FrontLeg)
# with open('data/targetAnglesFrontLeg.npy', 'wb') as f:
#     np.save(f, targetAngles_FrontLeg)
# with open('data/targetAnglesBackLeg.npy', 'wb') as f:
#     np.save(f, targetAngles_BackLeg)

for i in range(1000):
    p.stepSimulation()
    #backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName="Torso_BackLeg",

        controlMode=p.POSITION_CONTROL,

        targetPosition=targetAngles_BackLeg[i],

        maxForce=50)
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName="Torso_FrontLeg",

        controlMode=p.POSITION_CONTROL,

        targetPosition=targetAngles_FrontLeg[i],

        maxForce=50)

    time.sleep(1/1200)
p.disconnect()
#print('backLegSensorValues:::', backLegSensorValues)
print('frontLegSensorValues:::', frontLegSensorValues)
# with open('data/backLegSensorValues.npy', 'wb') as f:
#     np.save(f, backLegSensorValues)
with open('data/frontLegSensorValues.npy', 'wb') as f:
    np.save(f, frontLegSensorValues)