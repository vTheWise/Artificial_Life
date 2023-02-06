import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:

    def __init__(self, solutionID, robotNumber):
        self.solutionID = solutionID
        self.motors = dict()
        self.robotId = p.loadURDF("data/body{0}.urdf".format(robotNumber))
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK("data/brain{0}_{1}.nndf".format(str(self.solutionID), str(robotNumber)))
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system("rm ./data/brain{0}_{1}.nndf".format(str(self.solutionID), str(robotNumber)))


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

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        return basePosition


