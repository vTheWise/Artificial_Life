import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as np
import random

#region File Attributes
# set random seeds
random.seed(c.random_seed)
np.random.seed(c.numpy_seed)
#endregion File Attributes

class ROBOT:

    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.motors = dict()
        self.robotId = p.loadURDF("data/body{0}.urdf".format(str(self.solutionID)), flags=p.URDF_USE_SELF_COLLISION)
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK("data/brain{0}.nndf".format(str(self.solutionID)))
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system("rm ./data/brain{0}.nndf".format(str(self.solutionID)))
        os.system("rm ./data/body{0}.urdf".format(str(self.solutionID)))


    def Prepare_To_Sense(self):
        self.sensors = dict()
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, timeStep):
        for k, v in self.sensors.items():
            v.Get_Value(timeStep)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                motor = self.motors[jointName]
                motor.Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Update()

    def __dist(self, pos1, pos2):
        return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2)

    def Get_Fitness(self, ballId):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]

        ball_orientation = p.getBasePositionAndOrientation(ballId)
        ball_position = ball_orientation[0]

        # distance from the ball
        dist1 = self.__dist(ball_position, basePosition)

        with open('data/tmp{0}.txt'.format(str(self.solutionID)), 'w') as f:
            f.write(str(-1 * dist1))
            f.close()
        os.system("mv data/tmp{0}.txt data/fitness{0}.txt".format(str(self.solutionID)))

