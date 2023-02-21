#region Imports
import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import random
import os
import time
#endregion Imports

#region File Attributes
# random.seed(15)    # seed for random numbers
# np.random.seed(10)    # seed for numpy random numbers
#endregion File Attributes

class SOLUTION:

    def __init__(self, id=0):
        #region Class Variables
        self.myID = id
        self.currLink = 0
        self.maxNumLinks = random.randint(5, 15)
        self.probSensor = 0.5  # max probability threshold to determine whether a link has sensor
        self.probMotor = 0.7  # max probability threshold to determine whether a joint has motor
        self.sensors = []  # contains the IDs of the links having sensor
        self.motors = []  # contains tuples (l1:parent link, l2:child link)
        # max probability threshold to determine whether the next link will be created on the same face
        self.probExtend = 0.6
        # max probability threshold to determine whether the next link will be created in a different face
        self.probSwitchFace = 0.5
        '''
        self.probNextFace: a dictionary having key as a tuple that denotes the direction of the current link...
                            The values of the dictionary are lists containing probabilities of extending the next
                            link from the same face or choosing a new face... The probability of switching to the 
                            opposite face is 0
        '''
        self.probNextFace = {
            (1, 0, 0): [self.probExtend, 0, self.probSwitchFace, self.probSwitchFace, self.probSwitchFace, self.probSwitchFace],
            (-1, 0, 0): [0, self.probExtend, self.probSwitchFace, self.probSwitchFace, self.probSwitchFace, self.probSwitchFace],
            (0, 1, 0): [self.probSwitchFace, self.probSwitchFace, self.probExtend, 0, self.probSwitchFace, self.probSwitchFace],
            (0, -1, 0): [self.probSwitchFace, self.probSwitchFace, 0, self.probExtend, self.probSwitchFace, self.probSwitchFace],
            (0, 0, 1): [self.probSwitchFace, self.probSwitchFace, self.probSwitchFace, self.probSwitchFace, self.probExtend, 0]
        }
        #endregion Class Variables

        #region Create World, Body, and Brain
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        #endregion Create World, Body, and Brain

    def Start_Simulation(self, directOrGUI):
        os.system("python3 simulate.py {0} {1} 2&>runLogs.txt &".format(directOrGUI, str(self.myID)))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("data/fitness{0}.txt".format(str(self.myID))):
            time.sleep(0.01)
        f = open("data/fitness{0}.txt".format(str(self.myID)), "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm ./data/fitness{0}.txt".format(str(self.myID)))

    def Create_World(self):
        # empty world
        pyrosim.Start_SDF("data/world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("data/body.urdf")

        # root link
        dim = self.Get_Dimensions()
        # a link can have sensor only if a random number between [0, 1) is less than/equal to the threshold
        if random.random() < self.probSensor:
            color = c.color_sensor_link
            rgba = c.rgba_sensor_link
            self.sensors.append(self.currLink)
        else:
            color = c.color_nosensor_link
            rgba = c.rgba_nosensor_link
        pyrosim.Send_Cube(name="Link{0}".format(self.currLink), pos=[0, 0, 0.325], size=dim*2, color=color, rgba=rgba,
                          mass=np.prod(dim))
        self.currLink += 1

        # recursion for rest of the body
        self.Create_Body_Rec(parentLink=self.currLink - 1, jointPos=[0+dim[0], 0, 0.325],
                             currDirection=[1, 0, 0], height=0.325+dim[2])

        pyrosim.End()

    def Create_Body_Rec(self, parentLink, jointPos, currDirection, height):
        # base case for stopping recursion
        if self.currLink == self.maxNumLinks:
            return
        # check if the limb is underground
        if height < 0.325:
            return

        # create joint from the parentLink to a new link
        '''
        joint's axis direction based on current link direction:
        If the current direction is z (0,0,1), then the joint should enable motion in x-y plane.
        If the current direction is y (0,1,0), then the joint should enable motion in x-z plane.
        If the current direction is x (1,0,0), then the joint should enable motion in y-z plane.
        '''
        if currDirection == [0, 0, 1] or currDirection == [0, 0, -1]:
            axis = "0 0 1"
        elif currDirection == [0, 1, 0] or currDirection == [0, -1, 0]:
            axis = "0 1 0"
        else:
            axis = "1 0 0"
        pyrosim.Send_Joint(name="Link{0}_Link{1}".format(parentLink, self.currLink), parent="Link{0}".format(parentLink),
                           child="Link{0}".format(self.currLink), type="revolute", position=jointPos, jointAxis=axis)
        # a joint can have motor only if a random number between [0, 1) is less than/equal to the threshold
        if random.random() < self.probMotor:
            self.motors.append((parentLink, self.currLink))

        newDim = self.Get_Dimensions()
        linkPos = np.multiply(currDirection, newDim)
        if random.random() < self.probSensor:
            color = c.color_sensor_link
            rgba = c.rgba_sensor_link
            self.sensors.append(self.currLink)
        else:
            color = c.color_nosensor_link
            rgba = c.rgba_nosensor_link
        pyrosim.Send_Cube(name="Link{0}".format(self.currLink), pos=linkPos, size=newDim*2, color=color, rgba=rgba,
                          mass=np.prod(newDim))
        newParentLink = self.currLink
        self.currLink += 1

        # child recursive function
        self.Get_NewDirection_Rec(currDirection=currDirection, parentLink=newParentLink, dim=newDim,
                                lstProbNextFace=self.probNextFace[tuple(currDirection)], height=height)
    def Get_NewDirection_Rec(self, currDirection, parentLink, dim, lstProbNextFace, height):
        newDir = currDirection
        for idx in range(len(lstProbNextFace)):
            if (random.random() < lstProbNextFace[idx]):
                newDir = self.Get_Face_Directions(idx)
                newDir = currDirection if newDir == [0, 0, 0] else newDir
        jointPos = np.multiply(np.add(currDirection, newDir), dim)
        self.Create_Body_Rec(parentLink, jointPos, newDir, height+dim[2])

    def Get_Face_Directions(self, faceIdx):
        dir = [0, 0, 0]
        if faceIdx == 0:
            dir = [1, 0, 0]
        elif faceIdx == 1:
            dir = [-1, 0, 0]
        elif faceIdx == 2:
            dir = [0, 1, 0]
        elif faceIdx == 3:
            dir = [0, -1, 0]
        elif faceIdx == 4:
            dir = [0, 0, 1]
        # elif faceIdx == 5:
        #     dir = [0, 0, -1]
        return dir

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("data/brain{0}.nndf".format(self.myID))

        # random synapse weights
        self.weights = np.random.random((len(self.sensors), len(self.motors))) * 2 - 1

        # sensor neurons
        for i in self.sensors:
            pyrosim.Send_Sensor_Neuron(name="Sensor{0}".format(i), linkName="Link{0}".format(i))

        # motor neurons
        for m in self.motors:
            pyrosim.Send_Motor_Neuron(name="Motor{0}".format(m[0]),
                                      jointName="Link{0}_Link{1}".format(m[0], m[1]))

        print("motors::", len(self.motors))
        print("sensors::", len(self.sensors))
        print("Links::", self.currLink+1)
        # synapses
        i=0
        for s in self.sensors:
            j=0
            for m in self.motors:
                pyrosim.Send_Synapse(sourceNeuronName="Sensor{0}".format(s), targetNeuronName="Motor{0}".format(m[0]),
                                     weight=self.weights[i][j])
                j += 1
            i += 1

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, len(self.sensors) - 1)
        randomColumn = random.randint(0, len(self.motors) - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    '''
    Returns a random array of shape 3X1 with the values in the specified range
    '''
    def Get_Dimensions(self):
        return np.random.rand(3) * 0.2 + 0.125








