import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import random
import os
import time

class SOLUTION:


    def __init__(self, ID):
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        self.weights = (2 * self.weights) - 1
        self.myID = ID
        self.fitness = []

    def Start_Simulation(self, directOrGUI):
        if self.myID == 0:
            self.Create_World()
        for idx in range(c.numRobots):
            self.Create_Body(idx)
            self.Create_Brain(idx)
        os.system("python3 simulate.py {0} {1} 2&>runLogs.txt &".format(directOrGUI, str(self.myID)))

    def Wait_For_Simulation_To_End(self):
        for idx in range(c.numRobots):
            while not os.path.exists("data/fitness{0}_{1}.txt".format(str(self.myID), str(idx))):
                time.sleep(0.01)
            f = open("data/fitness{0}_{1}.txt".format(str(self.myID), str(idx)), "r")
            self.fitness.append(float(f.read()))
            f.close()
            os.system("rm ./data/fitness{0}_{1}.txt".format(str(self.myID), str(idx)))

    def Create_World(self):
        pyrosim.Start_SDF("data/world.sdf")
        pyrosim.Send_Sphere(name="Head", pos=c.ball_pos, size=[0.75])
        pyrosim.End()

    def Create_Body(self, idx):
        #root
        if idx == 0:
            color_sensor_link = c.color_sensor_link_root
            color_nosensor_link = c.color_nosensor_link_root
            rgba_sensor_link = c.rgba_sensor_link_root
            rgba_nosensor_link = c.rgba_nosensor_link_root
        else: #non-root
            color_sensor_link = c.color_sensor_link
            color_nosensor_link = c.color_nosensor_link
            rgba_sensor_link = c.rgba_sensor_link
            rgba_nosensor_link = c.rgba_nosensor_link

        pyrosim.Start_URDF("data/body{0}.urdf".format(str(idx)))
        pyrosim.Send_Cube(name="Head", pos=[0+idx*4, 0, 3], size=[1, 1, 1], color=color_nosensor_link,
                          rgba=rgba_nosensor_link)
        pyrosim.Send_Joint(name="Head_LeftHand", parent="Head", child="LeftHand", type="revolute",
                                              position=[0+idx*4, -0.5, 3], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftHand", pos=[0, -0.5, 0], size=[0.2, 1,  0.2], color=color_nosensor_link,
                          rgba=rgba_nosensor_link)
        pyrosim.Send_Joint(name="Head_RightHand", parent="Head", child="RightHand", type="revolute",
                           position=[0+idx*4, 0.5, 3], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightHand", pos=[0, 0.5, 0], size=[0.2, 1, 0.2], color=color_nosensor_link,
                          rgba=rgba_nosensor_link)
        pyrosim.Send_Joint(name="Head_UpperLeftLeg", parent="Head", child="UpperLeftLeg", type="revolute",
                           position=[0+idx*4, -0.5, 2.5], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="UpperLeftLeg", pos=[0, 0, -0.5], size=[0.5, 0.5, 1], color=color_nosensor_link,
                          rgba=rgba_nosensor_link)
        pyrosim.Send_Joint(name="Head_UpperRightLeg", parent="Head", child="UpperRightLeg", type="revolute",
                           position=[0+idx*4, 0.5, 2.5], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="UpperRightLeg", pos=[0, 0, -0.5], size=[0.5, 0.5, 1], color=color_nosensor_link,
                          rgba=rgba_nosensor_link)
        pyrosim.Send_Joint(name="UpperLeftLeg_LowerLeftLeg", parent="UpperLeftLeg", child="LowerLeftLeg",
                           type="revolute",
                           position=[0, 0, -1.0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0, 0, -0.5], size=[0.5, 0.5, 1], color=color_sensor_link,
                          rgba=rgba_sensor_link)
        pyrosim.Send_Joint(name="UpperRightLeg_LowerRightLeg", parent="UpperRightLeg", child="LowerRightLeg",
                           type="revolute",
                           position=[0, 0, -1.0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerRightLeg", pos=[0, 0, -0.5], size=[0.5, 0.5, 1], color=color_sensor_link,
                          rgba=rgba_sensor_link)
        pyrosim.End()

    def Create_Brain(self, idx):
        pyrosim.Start_NeuralNetwork("data/brain{0}_{1}.nndf".format(self.myID, str(idx)))

        # Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name=0, linkName="LowerLeftLeg")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LowerRightLeg")

        # Motor Neurons
        pyrosim.Send_Motor_Neuron(name=2, jointName="UpperLeftLeg_LowerLeftLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="UpperRightLeg_LowerRightLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Head_LeftHand")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Head_RightHand")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Head_UpperLeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Head_UpperRightLeg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons,
                                     weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomColumn = random.randint(0,c.numMotorNeurons-1)
        self.weights[randomRow, randomColumn] = (random.random() * 2) - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID + 1


