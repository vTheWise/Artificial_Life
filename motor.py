import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np
import pybullet as p

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency = c.frequency_BackLeg if self.jointName == c.joint_backLeg else c.frequency_FrontLeg
        self.offset = c.phaseOffset
        self.motorValues = np.linspace(c.linspace_start, c.linspace_stop, c.forLoopIteratorCount)
        for ix in range(len(self.motorValues)):
            self.motorValues[ix] = self.amplitude * np.sin(
                self.frequency * self.motorValues[ix] + self.offset)

    def Set_Value(self, robotId, timeStep):
        pyrosim.Set_Motor_For_Joint(

            bodyIndex=robotId,

            jointName=self.jointName,

            controlMode=p.POSITION_CONTROL,

            targetPosition=self.motorValues[timeStep],

            maxForce=c.maxForce)

    def Save_Values(self):
        with open('data/motorValues.npy', 'wb') as f:
            np.save(f, self.motorValues)
