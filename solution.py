import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import random
import os

class SOLUTION:


    def __init__(self):
        self.weights = np.random.rand(3,2)
        self.weights = (2 * self.weights) - 1

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python3 simulate.py {0}".format(directOrGUI))
        f = open("data/fitness.txt", "r")
        self.fitness = float(f.read())
        f.close()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[c.x1 - 2, c.y1 + 2, c.z1], size=[c.length, c.width, c.height])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[c.length, c.width, c.height])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[1, 0, 1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[c.length, c.width, c.height])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2, 0, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[c.length, c.width, c.height])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        # Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        # Motor Neurons
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+3, weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,2)
        randomColumn = random.randint(0,1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

