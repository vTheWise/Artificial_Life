from solution import SOLUTION
import os
import constants as c


def RemoveOldFiles():
    for file in os.listdir("./data"):
        if file.startswith("fitness") or file.startswith("brain") or file.startswith("body"):
            os.system("rm ./data/{0}".format(file))

def RunSimulation():
    nextAvailableID = 0
    for i in range(c.numCreatures):
        sol = SOLUTION(nextAvailableID)
        nextAvailableID += 1
        sol.Start_Simulation('GUI')
        sol.Wait_For_Simulation_To_End()

if __name__ == "__main__":
    RemoveOldFiles()
    RunSimulation()


