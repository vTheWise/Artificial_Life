import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
robotId = p.loadURDF("body.urdf")
print('robotId::::', robotId)

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(100)
frontLegSensorValues = np.zeros(100)

for i in range(100):
    p.stepSimulation()
    #backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

    time.sleep(1/60)
p.disconnect()
#print('backLegSensorValues:::', backLegSensorValues)
print('frontLegSensorValues:::', frontLegSensorValues)
# with open('data/backLegSensorValues.npy', 'wb') as f:
#     np.save(f, backLegSensorValues)
with open('data/frontLegSensorValues.npy', 'wb') as f:
    np.save(f, frontLegSensorValues)