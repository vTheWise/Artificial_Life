import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import random
import os
import time

class SOLUTION:


    def __init__(self, ID=0):
        self.myID = ID
        # randomly generated number of links
        self.numLinks = random.randint(5, 15)
        self.numMotorNeurons = self.numLinks - 1
        '''
        numpy.random.randint: 
        Returns random integers from the “discrete uniform” distribution of the specified dtype in the “half-open” 
        interval [low, high). If high is None (the default), then results are from [0, low). I'll keep low = 2 and
        high = None, to get 0s and 1s. The size of the list = self.numLinks.
        '''
        # random list of sensor values (0s -> no sensor and 1s -> yes sensor)
        self.sensorVal = np.random.randint(2, size=self.numLinks)
        self.numSensorNeurons = np.sum(self.sensorVal)
        self.weights = (4 * np.random.rand(self.numSensorNeurons, self.numMotorNeurons)) - 1

    def Start_Simulation(self, directOrGUI):
        if self.myID == 0:
            self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py {0} {1} 2&>runLogs.txt &".format(directOrGUI, str(self.myID)))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("data/fitness{0}.txt".format(str(self.myID))):
            time.sleep(0.01)
        f = open("data/fitness{0}.txt".format(str(self.myID)), "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm ./data/fitness{0}.txt".format(str(self.myID)))

    def Create_World(self):
        #Empty world
        pyrosim.Start_SDF("data/world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("data/body.urdf")
        #root link
        xpos = 0
        ypos = 0
        zpos = 1
        xsize = random.random() * 0.5
        ysize = random.random() * 0.5
        zsize = random.random() * 0.5
        if self.sensorVal[0] == 0: # no sensor
            pyrosim.Send_Cube(name="Link0", pos=[xpos, ypos, 1], size=[xsize*2, ysize*2, zsize*2],
                              color=c.color_nosensor_link, rgba=c.rgba_nosensor_link)
        else:
            pyrosim.Send_Cube(name="Link0", pos=[xpos, ypos, 1], size=[xsize*2, ysize*2, zsize*2],
                              color=c.color_sensor_link, rgba=c.rgba_sensor_link)
        pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute",
                           position=[0, ysize, 1], jointAxis="1 0 0")

        # loop through numLinks to create the rest of the links
        for i in range(1, self.numLinks):
            # we already created the first joint, so let's skip that
            if i != 1:
                # add a joint between two links.
                # joint position is relative to previous joint
                pyrosim.Send_Joint(name="Link{0}_Link{1}".format(str(i-1), str(i)),
                                   parent="Link{0}".format(str(i-1)), child="Link{0}".format(str(i)),
                                   type="revolute", position=[0, ysize*2, 0], jointAxis="1 0 0")

            xsize = random.random() * 0.5
            ysize = random.random() * 0.5
            zsize = random.random() * 0.5
            if self.sensorVal[i] == 0: #no sensor
                pyrosim.Send_Cube(name="Link{0}".format(str(i)), pos=[0, ysize, 0],
                                  size=[xsize*2, ysize*2, zsize*2],
                                  color=c.color_nosensor_link, rgba=c.rgba_nosensor_link)
            else:
                pyrosim.Send_Cube(name="Link{0}".format(str(i)), pos=[0, ysize, 0],
                                  size=[xsize*2, ysize*2, zsize*2],
                                  color=c.color_sensor_link, rgba=c.rgba_sensor_link)
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("data/brain{0}.nndf".format(self.myID))

        # sensor neurons
        cntSensor = 0
        for i in range(self.numLinks):
            if self.sensorVal[i] == 1:
                pyrosim.Send_Sensor_Neuron(name="Sensor{0}".format(cntSensor), linkName="Link{0}".format(str(i)))
                cntSensor += 1

        # motor neurons
        for i in range(self.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name="Motor{0}".format(i), jointName="Link{0}_Link{1}".format(str(i), str(i+1)))

        # synapses
        for s in range(self.numSensorNeurons):
            for m in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName="Sensor{0}".format(s), targetNeuronName="Motor{0}".format(m),
                                     weight=self.weights[s][m])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons-1)
        randomColumn = random.randint(0,c.numMotorNeurons-1)
        self.weights[randomRow, randomColumn] = random.random() * 4 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID + 1


