import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os

class ROBOT:

    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.motors = dict()
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK("brain{0}.nndf".format(str(self.solutionID)))
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system("rm brain{0}.nndf".format(str(self.solutionID)))


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

    def Act(self, timeStep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                motor = self.motors[jointName]
                motor.Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId,0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        with open('data/tmp{0}.txt'.format(str(self.solutionID)), 'w') as f:
            f.write(str(xCoordinateOfLinkZero))
            f.close()
        os.system("mv data/tmp{0}.txt data/fitness{0}.txt".format(str(self.solutionID)))

