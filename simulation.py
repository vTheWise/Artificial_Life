from world import WORLD
from robot import ROBOT
import constants as c
import pybullet as p
import pybullet_data
import time

class SIMULATION:

    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        try:
            if directOrGUI == 'DIRECT':
                self.physicsClient = p.connect(p.DIRECT)
            elif directOrGUI == 'GUI':
                self.physicsClient = p.connect(p.GUI)
                p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
            else:
                raise ValueError('Incorrect Mode!! Please choose "DIRECT" or "GUI".')
        except Exception as error:
            print(error)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.gravityX, c.gravityY, c.gravityZ)
        self.world = WORLD(self.physicsClient)
        self.robot = ROBOT(solutionID)

    def __del__(self):
        p.disconnect()

    def Run(self):
        for t in range(c.forLoopIteratorCount):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act()
            if self.directOrGUI == 'GUI':
                time.sleep(c.sleepTime)

    def Get_Fitness(self):
        self.robot.Get_Fitness(self.world.ballId[0])

