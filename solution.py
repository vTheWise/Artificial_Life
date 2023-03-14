#region Imports
import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim
import random
import os
import time
from link import LINK
from joint import JOINT
#endregion Imports

#region File Attributes
# set random seeds
random.seed(c.random_seed)
np.random.seed(c.numpy_seed)
#endregion File Attributes

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        self.parentID = -1
        if self.myID == 0:
            self.Create_World()

    def Start_Simulation(self, directOrGUI, bodyCreated=False):
        if not bodyCreated:
            self.min_limbs = 2
            self.max_limbs = 10
            self.num_limbs = random.randint(self.min_limbs, self.max_limbs)
            self.numMotorNeurons = self.num_limbs - 1 # equals the number of joints
            self.probSensor = 0.5
            self.isSensorArray = random.choices([0, 1], weights=[1 - self.probSensor, self.probSensor], k=self.num_limbs)
            self.numSensorNeurons = np.sum(self.isSensorArray)

            # when there's no sensor, randomly add a sensor
            if self.numSensorNeurons == 0:
                rIdx = random.randint(0, len(self.isSensorArray) - 1)
                self.isSensorArray[rIdx] = 1
                self.numSensorNeurons += 1

            # set limits for link dimensions
            self.maxCubeDim = 1
            self.minCubeDim = 0.2

            # initialize brain weights
            self.weights = (2 * np.random.rand(self.numSensorNeurons, self.numMotorNeurons)) - 1

            # probability of adding and removing a sensor
            self.addSensorProb = 0.5
            self.removeSensorProb = 0.5

            # probability of adding or removing link
            self.addLinkProb = 0.5
            self.removeLinkProb = 1 - self.addLinkProb

            # probability of mutating body and brain
            '''
            inductive bias: evolution should evolve the body of the creatures more often in the initial stages, 
            and then at later stages, once the body is optimized, then brain evolution should take over
            '''
            self.mutateBodyProb = 1
            self.mutateBrainProb = 0.1

        self.Create_Body(bodyCreated)
        self.Create_Brain()
        os.system("python3 simulate.py {0} {1} 2&>runLogs.txt &".format(directOrGUI, str(self.myID)))


    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("data/fitness{0}.txt".format(str(self.myID))):
            time.sleep(0.01)
        f = open("data/fitness{0}.txt".format(str(self.myID)), "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm ./data/fitness{0}.txt".format(str(self.myID)))
        return self.fitness

    def Create_World(self):
        pyrosim.Start_SDF("data/world.sdf")
        ball_pos = c.ball_pos
        for i in range(10):
            pyrosim.Send_Sphere(name="Ball{0}".format(str(i)), pos=ball_pos, size=[1])
            ball_pos = np.add(ball_pos, [-3, 0, 0])

        if c.generate_stairs:
            delta_y, delta_z = 1.5, 0.2
            init_y = c.stair_pos
            mass = 50.0
            pyrosim.Send_Cube(name="Box1", pos=[-5, init_y + delta_y * 0.5, delta_z / 2.0], size=[50, delta_y, delta_z],
                              mass=mass)
            pyrosim.Send_Cube(name="Box2", pos=[-5, init_y + delta_y * 1.5,  (delta_z * 2) / 2.0],
                              size=[50, delta_y, delta_z * 2], mass=mass)
            pyrosim.Send_Cube(name="Box3", pos=[-5, init_y + delta_y * 2.5, (delta_z * 3) / 2.0],
                              size=[50, delta_y,  delta_z * 3], mass=mass)
            pyrosim.Send_Cube(name="Box4", pos=[-5, init_y + delta_y * 3.5, (delta_z * 4) / 2.0],
                              size=[50, delta_y,  delta_z * 4], mass=mass)
            pyrosim.Send_Cube(name="Box5", pos=[-5, init_y + delta_y * 4.5,  (delta_z * 5) / 2.0],
                              size=[50, delta_y, delta_z * 5], mass=mass)
        pyrosim.End()

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    def getJointPos(self, parent_idx, face):
        jointX, jointY, jointZ = 0, 0, 0
        if face == "xp":
            jointX = self.links[parent_idx].relPos[0] + self.links[parent_idx].dim[0] / 2
            jointY = self.links[parent_idx].relPos[1] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[1] / 2
            jointZ = self.links[parent_idx].relPos[2] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[2] / 2

        elif face == "xn":
            jointX = self.links[parent_idx].relPos[0] - self.links[parent_idx].dim[0] / 2
            jointY = self.links[parent_idx].relPos[1] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[1] / 2
            jointZ = self.links[parent_idx].relPos[2] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[2] / 2

        elif face == "yp":
            jointY = self.links[parent_idx].relPos[1] + self.links[parent_idx].dim[1] / 2
            jointX = self.links[parent_idx].relPos[0] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[0] / 2
            jointZ = self.links[parent_idx].relPos[2] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[2] / 2

        elif face == "yn":
            jointY = self.links[parent_idx].relPos[1] - self.links[parent_idx].dim[1] / 2
            jointX = self.links[parent_idx].relPos[0] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[0] / 2
            jointZ = self.links[parent_idx].relPos[2] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[2] / 2

        elif face == "zp":
            jointZ = self.links[parent_idx].relPos[2] + self.links[parent_idx].dim[2] / 2
            jointX = self.links[parent_idx].relPos[0] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[0] / 2
            jointY = self.links[parent_idx].relPos[1] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[1] / 2

        elif face == "zn":
            jointZ = self.links[parent_idx].relPos[2] - self.links[parent_idx].dim[2] / 2
            jointX = self.links[parent_idx].relPos[0] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[0] / 2
            jointY = self.links[parent_idx].relPos[1] + (random.random() * 2 - 1) * \
                     self.links[parent_idx].dim[1] / 2

        return [jointX, jointY, jointZ]

    def addJoint(self, idx):
        parent_idx = random.randint(0, len(self.links) - 1)
        face = random.choice(["xp", "yp", "zp", "xn", "yn", "zn"])
        self.links[parent_idx].face.append(face)

        jointPos = self.getJointPos(parent_idx, face)
        axis = "0 0 0"
        if face == "xp" or face == "xn":
            axis = "1 0 0"  # move in y-z plane
        elif face == "yp" or face == "yn":
            axis = "0 1 0"  # move in x-z plane
        elif face == "zp" or face == "zn":
            axis = "0 0 1"  # move in x-y plane

        joint = JOINT(str(parent_idx) + '_' + str(idx), jointPos, axis)
        joint.jointGlobalPos[0] += self.links[parent_idx].globalPos[0] + joint.jointPos[0]
        joint.jointGlobalPos[1] += self.links[parent_idx].globalPos[1] + joint.jointPos[1]
        joint.jointGlobalPos[2] += self.links[parent_idx].globalPos[2] + joint.jointPos[2]

        return joint, parent_idx, face

    def addLink(self, idx, joint, face, parent_idx):
        size_x = random.uniform(self.minCubeDim, self.maxCubeDim)
        size_y = random.uniform(self.minCubeDim, self.maxCubeDim)
        size_z = random.uniform(self.minCubeDim, self.maxCubeDim)
        pos = self.getCubePos([size_x, size_y, size_z], face)

        cube = LINK(str(idx), self.links[parent_idx], [size_x, size_y, size_z], pos)
        cube.globalPos[0] = cube.relPos[0] + joint.jointGlobalPos[0]
        cube.globalPos[1] = cube.relPos[1] + joint.jointGlobalPos[1]
        cube.globalPos[2] = cube.relPos[2] + joint.jointGlobalPos[2]

        return cube

    def getCubePos(self, dim, face):
        cubeX, cubeY, cubeZ = 0, 0, 0
        if face == "xp":
            cubeX, cubeY, cubeZ = dim[0] / 2, 0, 0

        elif face == "xn":
            cubeX, cubeY, cubeZ = -dim[0] / 2, 0, 0

        elif face == "yp":
            cubeX, cubeY, cubeZ = 0, dim[1] / 2, 0

        elif face == "yn":
            cubeX, cubeY, cubeZ = 0, -dim[1] / 2, 0

        elif face == "zp":
            cubeX, cubeY, cubeZ = 0, 0, dim[2] / 2

        elif face == "zn":
            cubeX, cubeY, cubeZ = 0, 0, -dim[2] / 2

        return [cubeX, cubeY, cubeZ]

    def isIntersecting(self, cube):
        isOverlap = False
        for link in self.links:
            if self.isIntersectingWithLink(cube, link):
                isOverlap = True
                break
        return isOverlap

    def isIntersectingWithLink(self, cube, link):
        cubeDim = cube.dim
        linkDim = link.dim
        cubePos = cube.globalPos
        linkPos = link.globalPos

        x_intersect = self.checkAxisIntersection(cubePos[0] - cubeDim[0] / 2, cubePos[0] + cubeDim[0] / 2,
                                          linkPos[0] - linkDim[0] / 2, linkPos[0] + linkDim[0] / 2)

        y_intersect = self.checkAxisIntersection(cubePos[1] - cubeDim[1] / 2, cubePos[1] + cubeDim[1] / 2,
                                          linkPos[1] - linkDim[1] / 2, linkPos[1] + linkDim[1] / 2)

        z_intersect = self.checkAxisIntersection(cubePos[2] - cubeDim[2] / 2, cubePos[2] + cubeDim[2] / 2,
                                          linkPos[2] - linkDim[2] / 2, linkPos[2] + linkDim[2] / 2)

        return x_intersect and y_intersect and z_intersect

    def checkAxisIntersection(self, min1, max1, min2, max2):
        return (min2 <= max1 and min2 >= min1) or (max2 <= max1 and max2 >= min1) or (
                    min1 <= max2 and min1 >= min2) or (max1 <= max2 and max1 >= min2)

    def getMinZ(self):
        minZ = float('inf')
        for l in self.links:
            if l.globalPos[2] - l.dim[2] / 2 < minZ:
                minZ = l.globalPos[2] - l.dim[2] / 2
        return minZ

    def Create_Body(self, bodyCreated):
        pyrosim.Start_URDF("data/body{0}.urdf".format(self.myID))
        if not bodyCreated:     # create new body

            self.links = []
            self.joints = []

            for i in range(self.num_limbs):
                if i == 0:
                    size_x = random.uniform(self.minCubeDim, self.maxCubeDim)
                    size_y = random.uniform(self.minCubeDim, self.maxCubeDim)
                    size_z = random.uniform(self.minCubeDim, self.maxCubeDim)
                    cube = LINK(str(i), None, [size_x, size_y, size_z], [0, 0, 0])
                    cube.globalPos = [0, 0, 0]
                    if self.isSensorArray[i]:
                        cube.setColor(c.color_sensor_link, c.rgba_sensor_link)
                    self.links.append(cube)
                else:
                    joint, parent_idx, face = self.addJoint(i)
                    cube = self.addLink(i, joint, face, parent_idx)

                    while self.isIntersecting(cube):
                        joint, parent_idx, face = self.addJoint(i)
                        cube = self.addLink(i, joint, face, parent_idx)
                    if self.isSensorArray[i]:
                        cube.setColor(c.color_sensor_link, c.rgba_sensor_link)
                    self.links.append(cube)
                    self.joints.append(joint)

            minZ = self.getMinZ()
            offset = self.maxCubeDim - minZ if minZ < self.maxCubeDim else 0

            for i in range(self.num_limbs - 1):
                self.joints[i].jointGlobalPos[2] += offset

            for i in range(self.num_limbs):
                self.links[i].globalPos[2] += offset

            self.links[0].relPos[2] += offset

            for i in range(self.num_limbs - 1):
                if self.joints[i].parentLink == "0":
                    self.joints[i].jointPos[2] += offset
            for i in range(self.num_limbs):
                cube = self.links[i]
                pyrosim.Send_Cube(name=cube.linkName, pos=cube.relPos, size=cube.dim, mass=cube.mass, color=cube.color,
                                  rgba=cube.rgba)

            for i in range(self.numMotorNeurons):
                joint = self.joints[i]
                pyrosim.Send_Joint(name=joint.jointName, parent=joint.parentLink, child=joint.childLink, type=joint.type,
                                   position=joint.jointPos, jointAxis=joint.jointAxis)

            pyrosim.End()

        else:   # update existing body
            for idx in range(len(self.isSensorArray)):
                if self.isSensorArray[idx]:
                    self.links[idx].setColor(c.color_sensor_link, c.rgba_sensor_link)
                else:
                    self.links[idx].setColor(c.color_nosensor_link, c.rgba_nosensor_link)
            for i in range(self.num_limbs):
                cube = self.links[i]
                pyrosim.Send_Cube(name=cube.linkName, pos=cube.relPos, size=cube.dim, mass=cube.mass, color=cube.color,
                                  rgba=cube.rgba)

            for i in range(self.numMotorNeurons):
                joint = self.joints[i]
                pyrosim.Send_Joint(name=joint.jointName, parent=joint.parentLink, child=joint.childLink, type=joint.type,
                                   position=joint.jointPos, jointAxis=joint.jointAxis)

            pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("data/brain{0}.nndf".format(self.myID))

        # sensor neurons
        neuronId = 0
        for idx, link in enumerate(self.links):
            if self.isSensorArray[idx] == 1:
                pyrosim.Send_Sensor_Neuron(name=neuronId, linkName=link.linkName)
                neuronId += 1

        # motor neurons
        for idx, joint in enumerate(self.joints):
            pyrosim.Send_Motor_Neuron(name=idx + self.numSensorNeurons,
                                      jointName=joint.parentLink + "_" + joint.childLink)

        for currentRow in range(self.numSensorNeurons):
            for currentCol in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentCol + self.numSensorNeurons,
                                     weight=self.weights[currentRow][currentCol])

        pyrosim.End()

    def Mutate(self):

        if random.random() < self.mutateBodyProb:

            if random.random() < self.addLinkProb and self.num_limbs < self.max_limbs:
                self.mutateBody()

            if random.random() < self.addSensorProb:
                self.addSensor()

            elif random.random() < self.removeSensorProb:
                self.removeSensor()

        if random.random() < self.mutateBrainProb:
            row = random.randint(0, self.weights.shape[0] - 1)
            col = random.randint(0, self.weights.shape[1] - 1)
            self.weights[row][col] = random.random() * 2 - 1

        if self.mutateBodyProb > 0.3 and random.random() < 0.5:
            self.mutateBodyProb -= 0.1
        if self.mutateBrainProb < 0.8 and random.random() < 0.5:
            self.mutateBrainProb += 0.1

    def addSensor(self):
        noSensorIdx = []
        for i in range(len(self.isSensorArray)):
            if self.isSensorArray[i] == 0:
                noSensorIdx.append(i)
        if len(noSensorIdx) == 0:
            return False
        rIdx = random.choices(noSensorIdx)[0]

        self.isSensorArray[rIdx] = 1

        newWeights = np.random.rand(self.numSensorNeurons + 1, self.numMotorNeurons)
        newWeights[:self.numSensorNeurons, :] = self.weights
        newWeights[self.numSensorNeurons:] = np.random.rand(1, self.numMotorNeurons)
        self.weights = newWeights
        self.numSensorNeurons += 1
        return True

    def removeSensor(self):
        pos = 0
        sensorInfo = dict()
        for i in range(len(self.isSensorArray)):
            if self.isSensorArray[i] == 1:
                sensorInfo.update({pos: i})
                pos += 1

        if len(sensorInfo) == 1:      # don't remove if there's only one sensor
            return False

        rIdx = random.choices(list(sensorInfo.keys()))[0]

        self.isSensorArray[sensorInfo[rIdx]] = 0

        self.weights = np.delete(self.weights, rIdx, 0)
        self.numSensorNeurons -= 1
        return True

    def mutateBody(self):
        existingLinks = []
        for link in self.links:
            existingLinks.append(int(link.linkName))
        maxLink = max(existingLinks)
        self.num_limbs += 1
        newLink = maxLink + 1
        joint, parent_idx, face = self.addJoint(newLink)
        cube = self.addLink(newLink, joint, face, parent_idx)

        while self.isIntersecting(cube):
            joint, parent_idx, face = self.addJoint(newLink)
            cube = self.addLink(newLink, joint, face, parent_idx)

        newWeights = np.random.rand(self.numSensorNeurons, self.numMotorNeurons + 1)
        newWeights[:, :self.numMotorNeurons] = self.weights
        newWeights[:, self.numMotorNeurons:] = np.random.rand(self.numSensorNeurons, 1)
        self.weights = newWeights
        self.numMotorNeurons += 1

        self.isSensorArray.append(random.randint(0, 1))
        if self.isSensorArray[-1]:
            cube.setColor(c.color_sensor_link, c.rgba_sensor_link)
            newWeights = np.random.rand(self.numSensorNeurons + 1, self.numMotorNeurons)
            newWeights[:self.numSensorNeurons, :] = self.weights
            newWeights[self.numSensorNeurons:] = np.random.rand(1, self.numMotorNeurons)
            self.weights = newWeights
            self.numSensorNeurons += 1
        self.links.append(cube)
        self.joints.append(joint)

    def removeLink(self):
        parentJointLinks = []
        for joint in self.joints:
            parentJointLinks.append(joint.parentLink)
        for idx, link in enumerate(self.links):
            if link.linkName not in parentJointLinks:        # safe to remove
                self.links.remove(link)
                self.num_limbs -= 1
                sensor_idx = self.isSensorArray.pop(int(link.linkName))
                self.numSensorNeurons = self.numSensorNeurons - 1 if link.color == c.color_sensor_link \
                    else self.numSensorNeurons
                # remove corresponding joints
                for joint in self.joints:
                    if joint.childLink == link.linkName:
                        self.joints.remove(joint)
                        self.numMotorNeurons -= 1
                self.weights = np.delete(self.weights, idx-1, 1)
                if link.color == c.color_sensor_link:
                    sensor_pos = sum(self.isSensorArray[:sensor_idx])
                    self.weights = np.delete(self.weights, sensor_pos, 0)
                break









