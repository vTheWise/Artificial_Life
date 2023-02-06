from world import WORLD
from robot import ROBOT
import constants as c
import pybullet as p
import pybullet_data
import time
import os
import numpy as np

class SIMULATION:

    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        try:
            if directOrGUI == 'DIRECT':
                self.physicsClient = p.connect(p.DIRECT)
            elif directOrGUI == 'GUI':
                self.physicsClient = p.connect(p.GUI)
            else:
                raise ValueError('Incorrect Mode!! Please choose "DIRECT" or "GUI".')
        except Exception as error:
            print(error)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.gravityX, c.gravityY, c.gravityZ)
        self.world = WORLD(self.physicsClient)
        self.robot = dict()
        for idx in range(c.numRobots):
            self.robot[idx] = ROBOT(solutionID, idx)

    def __del__(self):
        p.disconnect()

    def Run(self):
        for t in range(c.forLoopIteratorCount):
            p.stepSimulation()
            for idx in range(c.numRobots):
                self.robot[idx].Sense(t)
                self.robot[idx].Think()
                self.robot[idx].Act()
            if self.directOrGUI == 'GUI':
                time.sleep(c.sleepTime)

    def Get_Fitness(self):
        for idx in range(c.numRobots):
            position = (self.robot[idx].Get_Fitness())
            dist = (self.__dist(c.ball_pos, position))
            with open('data/tmp{0}_{1}.txt'.format(str(self.robot[0].solutionID), str(idx)), 'w') as f:
                f.write(str(dist))
                f.close()
            os.system("mv data/tmp{0}_{1}.txt data/fitness{0}_{1}.txt".format(str(self.robot[0].solutionID), str(idx)))

    def __dist(self, pos1, pos2):
        return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

