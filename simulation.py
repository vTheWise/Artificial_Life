from world import WORLD
from robot import ROBOT
import constants as c
import pybullet as p
import pybullet_data
import time

class SIMULATION:

    def __init__(self, directOrGUI):
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
        self.robot = ROBOT()

    def __del__(self):
        p.disconnect()

    def Run(self):
        for t in range(c.forLoopIteratorCount):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            time.sleep(c.sleepTime)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
