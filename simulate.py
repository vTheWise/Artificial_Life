from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
new_world = sys.argv[3]
simulation = SIMULATION(directOrGUI, solutionID, new_world)
simulation.Run()
simulation.Get_Fitness()



